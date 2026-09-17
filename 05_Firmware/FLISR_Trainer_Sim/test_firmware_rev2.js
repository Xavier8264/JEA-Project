/* Tests for firmware_rev2.js, the FLISR_Trainer_REV2.ino port.
 * Run:  python build_sim.py --sketch FLISR_Trainer_REV2
 *       node --test test_firmware_rev2.js
 * Also needs sim_config.json (REV0) as it stands; do not rebuild it.
 *
 * Copied from test_firmware_rev1.js. REV1 and REV2 share their logic, so the
 * tests are the same; the REV2 config, strip positions and banner differ.
 *
 * Two independent references:
 *   - REV0 (firmware.js, already tested) driven with the same button presses
 *     on the REV2 strip. Outside the animations REV2 must match it frame for
 *     frame.
 *   - A breadth-first search over an explicit pixel graph built from the run
 *     table. The sketch computes distances a different way (node distances
 *     plus position along a piece); the two must agree on every pixel.
 */
'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const REV0 = require('./firmware.js');
const REV2 = require('./firmware_rev2.js');      /* the port under test */

const load = f => JSON.parse(fs.readFileSync(path.join(__dirname, f), 'utf8'));
const CFG2 = load('sim_config_rev2.json');
/* REV0's own config with the REV2 strip swapped in, so REV0 lights the same
 * 352 pixels. Every other define the two sketches share must be identical. */
const CFG0 = load('sim_config.json');
for (const [k, v] of Object.entries(CFG0.defines))
  if (k !== 'NUM_LEDS' && k in CFG2.defines)
    assert.deepEqual(CFG2.defines[k], v, `REV0 and REV2 disagree on ${k}`);
CFG0.defines.NUM_LEDS = CFG2.defines.NUM_LEDS;
for (const t of Object.keys(CFG0.tables)) CFG0.tables[t] = CFG2.tables[t];
const D = CFG2.defines, T = CFG2.tables;
const BTN = [D.PIN_BTN_FAULT_Z1, D.PIN_BTN_FAULT_Z2, D.PIN_BTN_FAULT_Z3, D.PIN_BTN_FAULT_Z4,
             D.PIN_BTN_FAULT_Z5, D.PIN_BTN_FAULT_Z6, D.PIN_BTN_FAULT_DER, D.PIN_BTN_RESET];
const RED = D.COLOR_FAULT, A = D.COLOR_SRC_A, B = D.COLOR_SRC_B, K = D.COLOR_DEAD;
const STEP = D.ANIM_STEP_MS;

function bench(FW, cfg, overrides, tableOverrides) {
  cfg = JSON.parse(JSON.stringify(cfg));
  Object.assign(cfg.defines, overrides || {});
  Object.assign(cfg.tables, tableOverrides || {});
  const b = { text: '', writes: [], frame: null };
  b.board = FW.createBoard(cfg, {
    onSerial: s => { b.text += s; b.writes.push({ t: b.board.now, s }); },
    onShow: (leds, n) => { b.frame = { leds: leds.slice(0, n * 3), t: b.board.now }; }
  });
  const pairs = s => Object.fromEntries(s.trim().split(' ').map(p => p.split('=')));
  b.states = () => [...b.text.matchAll(/STEP 0(\d)  (\w+)\r\n  fault   : (.*)\r\n  zones   : (.*)\r\n  devices : (.*)\r\n/g)]
    .map(m => ({ step: +m[1], zones: pairs(m[4]), devices: pairs(m[5]) }));
  b.stepTimes = () => b.writes.filter(w => w.s === 'STEP 0').map(w => w.t);
  return b;
}

/* ---- device status pixels ---------------------------------------------
 * Strip positions typed in by hand from the block [2] comment table, so a
 * slip in DEV_SEG / DEV_PX or in stripIndex() cannot also fool the test.   */
const DEV_NAMES = ['SUB_A_BKR', 'DEV_A1', 'DEV_A2', 'TIE', 'DEV_B2', 'DEV_B1', 'SUB_B_BKR', 'DER_PCC'];
const DEV_STRIP = [4, 50, 102, 227, 253, 313, 278, 340];
const devAt = new Map(DEV_STRIP.map((g, d) => [g, DEV_NAMES[d]]));
const OPEN = D.COLOR_DEV_OPEN, CLOSED = D.COLOR_DEV_CLOSED;

/* What a status pixel should show at ms t, from the device states the
 * board printed on the serial line up to t. */
function deviceColor(b, name, t) {
  if (!b.stCache || b.stCache.len !== b.text.length)
    b.stCache = { len: b.text.length, times: b.stepTimes(), st: b.states() };
  const { times, st } = b.stCache;
  let k = -1;
  for (let j = 0; j < times.length; j++) if (times[j] <= t) k = j;
  assert.ok(k >= 0, `a state was printed before ${t} ms`);
  switch (st[k].devices[name]) {
    case 'CLOSED':  return CLOSED;
    case 'OPEN':    return OPEN;
    case 'TRIPPED': return (Math.floor(t / D.DEV_TRIP_BLINK_MS) & 1) ? OPEN : K;
    case 'LOCKOUT': return (Math.floor(t / D.DEV_LOCK_BLINK_MS) & 1) ? OPEN : K;
  }
  throw new Error(`unknown state for ${name}: ${st[k].devices[name]}`);
}

/* two boards, same inputs, same clock */
function pair(overrides) {
  const p = { r0: bench(REV0, CFG0, overrides), r2: bench(REV2, CFG2, overrides) };
  p.until = t => { p.r0.board.runUntil(t); p.r2.board.runUntil(t); };
  p.run = ms => p.until(p.r2.board.now + ms);
  p.press = (pin, holdMs = 60) => {
    const t = p.r2.board.now;
    for (const b of [p.r0, p.r2]) { b.board.setContact(pin, true, t); b.board.setContact(pin, false, t + holdMs); }
    p.until(t + 41);                      /* the press registers at t + 40 */
  };
  return p;
}

/* ---- pixel graph oracle ------------------------------------------------ */
const NUM = D.NUM_LEDS;
const runStart = [], pxRun = [], pxOff = [];
{ let n = 0; T.SEG_LEN.forEach((len, s) => { runStart[s] = n; for (let i = 0; i < len; i++) { pxRun.push(s); pxOff.push(i); } n += len; }); }
function zoneOf(g) {
  const s = pxRun[g], i = pxOff[g];
  if (!T.SEG_OVER[s]) return D.ZN_HID;
  const sp = T.SEG_SPLIT[s];
  return (sp && i >= sp) ? T.SEG_ZONE2[s] : T.SEG_ZONE[s];
}
const adj = Array.from({ length: NUM }, () => new Set());
const atNode = new Map();
const touch = (node, g) => { if (!atNode.has(node)) atNode.set(node, []); atNode.get(node).push(g); };
T.SEG_LEN.forEach((len, s) => {
  if (!T.SEG_OVER[s] || !len) return;
  for (let i = 0; i + 1 < len; i++) { adj[runStart[s] + i].add(runStart[s] + i + 1); adj[runStart[s] + i + 1].add(runStart[s] + i); }
  touch(T.SEG_FROM[s], runStart[s]);
  touch(T.SEG_TO[s], runStart[s] + len - 1);
});
for (let t = 0; t < D.NUM_TAPS; t++) {
  const g = runStart[T.TAP_SEG[t]] + T.TAP_PX[t];
  touch(T.TAP_NODE[t], g - 1); touch(T.TAP_NODE[t], g);
}
atNode.forEach(list => list.forEach(a => list.forEach(b => { if (a !== b) adj[a].add(b); })));

function bfs(sources, mask) {
  const dist = new Array(NUM).fill(Infinity), q = [];
  for (const [g, d] of sources) if (mask & (1 << zoneOf(g))) { dist[g] = d; q.push(g); }
  for (let h = 0; h < q.length; h++) {
    const g = q[h];
    for (const n of adj[g]) if ((mask & (1 << zoneOf(n))) && dist[n] > dist[g] + 1) { dist[n] = dist[g] + 1; q.push(n); }
  }
  return dist;
}

const zoneCode = z => (z === 'DER' ? D.ZN_DER : +z.slice(1));
function lostMask(zones) {                         /* zones read from the serial state */
  let m = 0;
  for (const [z, v] of Object.entries(zones)) if (v === 'dead' || v === 'FLT') m |= 1 << zoneCode(z);
  return m;
}
function faultMask(zones) {
  let m = 0;
  for (const [z, v] of Object.entries(zones)) if (v === 'FLT') m |= 1 << zoneCode(z);
  return m;
}
function restoredMask(zones) {
  let m = 0;
  for (let k = 1; k <= 6; k++) if ((k <= 3 && zones['Z' + k] === 'B') || (k >= 4 && zones['Z' + k] === 'A')) m |= 1 << k;
  if ((m & (1 << 5)) && zones.DER === 'A') m |= 1 << D.ZN_DER;
  return m;
}

const px = (f, g) => [f.leds[g * 3], f.leds[g * 3 + 1], f.leds[g * 3 + 2]];
/* Every line pixel must match expectFn. The 8 device status pixels must show
 * their device instead, whatever the line under them is doing. */
function assertFrame(p, expectFn, label) {
  const f0 = p.r0.frame, f1 = p.r2.frame;
  assert.equal(f1.t, f0.t, `${label}: both boards rendered at the same ms`);
  for (let g = 0; g < NUM; g++) {
    const want = devAt.has(g) ? deviceColor(p.r2, devAt.get(g), f1.t) : expectFn(g, px(f0, g), f1.t);
    assert.deepEqual(px(f1, g), want, `${label}: px ${g} at ${f1.t} ms (run idx ${pxRun[g]} pixel ${pxOff[g]})`);
  }
}
const FAULT_NAMES = ['Z1', 'Z2', 'Z3', 'Z4', 'Z5', 'Z6', 'DER'];

/* ======================================================================= */

test('boot: banner says REV2, then output and the NORMAL frame match REV0', () => {
  const p = pair();
  p.until(300);
  assert.ok(p.r2.text.startsWith('\n=== JEA Tabletop FLISR Trainer REV2 ===\r\n'));
  assert.ok(p.r2.text.includes('segment table total : 352\r\nNUM_LEDS            : 352\r\n[OK]'));
  assert.equal(p.r2.text.replace(' REV2 ===', ' ==='), p.r0.text);
  assertFrame(p, (g, r0) => r0, 'NORMAL');
});

test('NORMAL: 7 status pixels closed, the TIE pixel open, every other pixel as REV0', () => {
  const p = pair();
  p.until(300);
  const f = p.r2.frame;
  DEV_STRIP.forEach((g, d) => assert.deepEqual(px(f, g), d === 3 ? OPEN : CLOSED, DEV_NAMES[d]));
  for (let g = 0; g < NUM; g++) if (!devAt.has(g)) assert.deepEqual(px(f, g), px(p.r0.frame, g), `px ${g}`);
  assert.notDeepEqual(OPEN, CLOSED);
  for (const c of [A, B, RED, K]) { assert.notDeepEqual(OPEN, c); assert.notDeepEqual(CLOSED, c); }
});

test('status pixels are on visible runs, one per device, where the table says', () => {
  assert.equal(D.NUM_DEVICES, 8);
  for (let d = 0; d < 8; d++) {
    assert.equal(runStart[T.DEV_SEG[d]] + T.DEV_PX[d], DEV_STRIP[d], DEV_NAMES[d]);
    assert.equal(T.SEG_OVER[T.DEV_SEG[d]], 1, `${DEV_NAMES[d]} is on a visible run`);
    assert.ok(T.DEV_PX[d] < T.SEG_LEN[T.DEV_SEG[d]], `${DEV_NAMES[d]} is inside its run`);
  }
  assert.equal(new Set(DEV_STRIP).size, 8);
});

test('FAULT Z1 status pixels: trip blinks slow, lockout fast, far side open, tie closes', () => {
  const b = bench(REV2, CFG2, { AUTO_ADVANCE: 0 });
  b.board.runUntil(300);
  const press = pin => { const t = b.board.now; b.board.setContact(pin, true, t); b.board.setContact(pin, false, t + 60); b.board.runUntil(t + 41); };
  const at = g => px(b.frame, g);
  const sample = (g, ms) => {                  /* the pixel on every frame for ms */
    const seen = [], from = b.board.now + 1, to = b.board.now + ms;
    let lastT = b.frame.t;
    for (let t = from; t <= to; t++) {
      b.board.runUntil(t);
      if (b.frame.t === lastT) continue;
      lastT = b.frame.t;
      seen.push({ t: lastT, on: at(g)[0] === OPEN[0] && at(g)[1] === OPEN[1] && at(g)[2] === OPEN[2], c: at(g) });
    }
    assert.ok(seen.length >= Math.floor(ms / D.FRAME_INTERVAL_MS) - 1, `sampled ${seen.length} frames in ${ms} ms`);
    return seen;
  };
  const SUB_A = DEV_STRIP[0], A1 = DEV_STRIP[1], TIE = DEV_STRIP[3];

  press(BTN[0]);                                   /* 01: SUB_A_BKR tripped */
  let seen = sample(SUB_A, 2000);
  for (const s of seen) {
    assert.deepEqual(s.c, s.on ? OPEN : K, `tripped pixel is amber or dark at ${s.t}`);
    assert.equal(s.on, (Math.floor(s.t / 500) & 1) === 1, `slow blink phase at ${s.t}`);
  }
  assert.ok(seen.some(s => s.on) && seen.some(s => !s.on));
  assert.deepEqual(at(A1), CLOSED, 'DEV_A1 still closed at 01');

  press(BTN[0]);                                   /* 02: lockout */
  seen = sample(SUB_A, 1000);
  for (const s of seen) assert.equal(s.on, (Math.floor(s.t / 150) & 1) === 1, `fast blink phase at ${s.t}`);

  press(BTN[0]);                                   /* 03: DEV_A1 opens */
  b.board.runUntil(b.board.now + 200);             /* past the release debounce */
  assert.equal(b.states().at(-1).step, 3);
  assert.deepEqual(at(A1), OPEN, 'DEV_A1 open at 03');
  assert.deepEqual(at(TIE), OPEN, 'TIE still open at 03');

  press(BTN[0]);                                   /* 04: tie closes */
  b.board.runUntil(b.board.now + 200);
  assert.equal(b.states().at(-1).step, 4);
  assert.deepEqual(at(TIE), CLOSED, 'TIE closed at 04');
  assert.deepEqual(at(A1), OPEN, 'DEV_A1 still open at 04');
});

test('FAULT DER: only the DER_PCC status pixel changes', () => {
  const b = bench(REV2, CFG2, { AUTO_ADVANCE: 0 });
  b.board.runUntil(300);
  const t = b.board.now;
  b.board.setContact(BTN[6], true, t); b.board.setContact(BTN[6], false, t + 60);
  b.board.runUntil(t + 1500);
  const f = b.frame;
  DEV_STRIP.forEach((g, d) => {
    if (d === 7) assert.deepEqual(px(f, g), (Math.floor(f.t / 500) & 1) ? OPEN : K, 'DER_PCC tripped, slow blink');
    else assert.deepEqual(px(f, g), d === 3 ? OPEN : CLOSED, DEV_NAMES[d]);
  });
});

test('a bad DEV_SEG / DEV_PX entry is reported at boot, and the good ones still work', () => {
  const b = bench(REV2, CFG2, {}, { DEV_PX: [4, 2, 7, 6, 0, 0, 0, 13], DEV_SEG: [0, 3, 7, 16, 20, 2, 22, 30] });
  b.board.runUntil(300);
  assert.match(b.text, /\[!\] DEV_B1: DEV_SEG \/ DEV_PX is not a pixel on a visible run\. See block \[2\]\.\r\n/, 'hidden run');
  assert.match(b.text, /\[!\] DER_PCC: DEV_SEG \/ DEV_PX is not a pixel on a visible run\. See block \[2\]\.\r\n/, 'past the run end');
  assert.equal((b.text.match(/\[!\]/g) || []).length, 2, 'only the two bad entries');
  assert.deepEqual(px(b.frame, DEV_STRIP[1]), CLOSED);
  const good = bench(REV2, CFG2);
  good.board.runUntil(300);
  assert.ok(!good.text.includes('[!]'), 'the real table prints no warning');
});

test('every fault location sits in the zone it names', () => {
  const want = [1, 2, 3, 4, 5, 6, D.ZN_DER];
  for (let f = 0; f < 7; f++) assert.equal(zoneOf(runStart[T.FAULT_SEG[f]] + T.FAULT_PX[f]), want[f], FAULT_NAMES[f]);
});

for (let f = 0; f < 7; f++) {
  test(`FAULT ${FAULT_NAMES[f]}: wave, hold, isolate and restore frames match the oracle and REV0`, () => {
    const p = pair({ AUTO_ADVANCE: 0 });
    p.until(300);

    /* 01 FAULT: red spreads from the fault pixel through everything that lost power */
    p.press(BTN[f]);
    const start = p.r2.stepTimes()[1];
    const st1 = p.r2.states()[1].zones;
    const lost = lostMask(st1), faulted = faultMask(st1);
    const src = runStart[T.FAULT_SEG[f]] + T.FAULT_PX[f];
    const dist = bfs([[src, 0]], lost);
    let last = 0;
    for (let g = 0; g < NUM; g++) if (lost & (1 << zoneOf(g))) {
      assert.ok(Number.isFinite(dist[g]), `px ${g} in a zone that lost power is reachable`);
      last = Math.max(last, dist[g]);
    }
    const waveEnd = start + last * STEP;
    const faultRule = (g, r0, t) => {
      const zn = zoneOf(g);
      if (!(lost & (1 << zn))) return r0;
      const front = Math.floor((t - start) / STEP);
      if (front < last) return dist[g] <= front ? RED : (zn <= 3 ? A : B);
      return (faulted & (1 << zn)) ? r0 : RED;       /* after: faulted blinks as REV0, rest red */
    };
    for (let t = p.r2.board.now + 1; t <= waveEnd + 800; t += 20) { p.until(t); assertFrame(p, faultRule, '01'); }

    /* 02 LOCKOUT: same picture */
    p.press(BTN[f]);
    for (let n = 0; n < 10; n++) { p.run(37); assertFrame(p, faultRule, '02'); }

    /* 03 ISOLATE: no animation. Everything that lost power holds solid red,
     * where REV0 turns the zones that only lost power dark. */
    p.press(BTN[f]);
    const isolateRule = (g, r0) => (lost & (1 << zoneOf(g))) ? RED : r0;
    for (let n = 0; n < 10; n++) { p.run(37); assertFrame(p, isolateRule, '03'); }

    /* 04 RESTORE: the new source color fills out from the tie, if the tie closes */
    p.press(BTN[f]);
    const rstart = p.r2.stepTimes()[4];
    const restored = restoredMask(p.r2.states()[4].zones);
    let rlast = 0, rdist = null;
    if (restored) {
      rdist = bfs(atNode.get(D.TIE_NODE).map(g => [g, 1]), restored);
      for (let g = 0; g < NUM; g++) if (restored & (1 << zoneOf(g))) {
        assert.ok(Number.isFinite(rdist[g]), `restored px ${g} is reachable from the tie`);
        rlast = Math.max(rlast, rdist[g]);
      }
    }
    /* the fill eats the red; anything still without power stays red */
    const lost4 = lostMask(p.r2.states()[4].zones);
    const restoreRule = (g, r0, t) => {
      const zn = zoneOf(g);
      if (restored & (1 << zn)) {
        const front = Math.floor((t - rstart) / STEP);
        return (front >= rlast || rdist[g] <= front) ? r0 : RED;
      }
      return (lost4 & (1 << zn)) ? RED : r0;
    };
    for (let t = p.r2.board.now + 1; t <= rstart + rlast * STEP + 400; t += 20) { p.until(t); assertFrame(p, restoreRule, '04'); }

    assert.equal(p.r2.text.replace(' REV2 ===', ' ==='), p.r0.text, 'serial output identical to REV0');
    if (f === 0 || f === 1 || f === 4 || f === 5) assert.ok(restored, 'this fault restores load across the tie');
    else assert.equal(restored, 0, 'no stranded load, tie stays open');
  });
}

test('auto-advance waits for each animation, then STEP_INTERVAL_MS', () => {
  const b = bench(REV2, CFG2);
  b.board.runUntil(300);
  const t0 = b.board.now;
  b.board.setContact(BTN[0], true, t0); b.board.setContact(BTN[0], false, t0 + 60);
  b.board.runUntil(t0 + 30000);
  const st = b.states(), times = b.stepTimes();
  assert.deepEqual(st.map(s => s.step), [0, 1, 2, 3, 4]);
  const lost = lostMask(st[1].zones);
  const dist = bfs([[runStart[T.FAULT_SEG[0]] + T.FAULT_PX[0], 0]], lost);
  const last = Math.max(...dist.filter((d, g) => lost & (1 << zoneOf(g))));
  assert.equal(times[2] - times[1], last * STEP + D.STEP_INTERVAL_MS, '02 after the wave plus the interval');
  assert.equal(times[3] - times[2], D.STEP_INTERVAL_MS, '03, no animation at 02');
  assert.equal(times[4] - times[3], D.STEP_INTERVAL_MS, '04, no animation at 03');
});

test('pressing on to 02 mid-wave keeps the wave going; 03 mid-wave cuts to the isolate frame', () => {
  const p = pair({ AUTO_ADVANCE: 0 });
  p.until(300);
  p.press(BTN[0]);                                 /* Z1: the longest wave */
  const start = p.r2.stepTimes()[1];
  const lost = lostMask(p.r2.states()[1].zones);
  const dist = bfs([[runStart[T.FAULT_SEG[0]] + T.FAULT_PX[0], 0]], lost);
  p.until(start + 20 * STEP);
  p.press(BTN[0]);                                 /* 02 */
  for (let n = 0; n < 5; n++) {
    p.run(30);
    assertFrame(p, (g, r0, t) => {
      const zn = zoneOf(g);
      if (!(lost & (1 << zn))) return r0;
      return dist[g] <= Math.floor((t - start) / STEP) ? RED : (zn <= 3 ? A : B);
    }, '02 mid-wave');
  }
  p.press(BTN[0]);                                 /* 03 */
  p.run(25);
  assertFrame(p, (g, r0) => (lost & (1 << zoneOf(g))) ? RED : r0, '03 right after');
});

test('a different fault button mid-wave starts a new wave from normal colors', () => {
  const p = pair({ AUTO_ADVANCE: 0 });
  p.until(300);
  p.press(BTN[0]);
  p.run(15 * STEP);
  p.press(BTN[5]);                                 /* Z6 */
  const start = p.r2.stepTimes()[2];
  const lost = lostMask(p.r2.states()[2].zones);
  const dist = bfs([[runStart[T.FAULT_SEG[5]] + T.FAULT_PX[5], 0]], lost);
  p.run(25);
  assertFrame(p, (g, r0, t) => {
    const zn = zoneOf(g);
    if (!(lost & (1 << zn))) return r0;
    return dist[g] <= Math.floor((t - start) / STEP) ? RED : (zn <= 3 ? A : B);
  }, 'Z6 after Z1');
});

test('RESET mid-wave returns to the NORMAL frame at once', () => {
  const p = pair({ AUTO_ADVANCE: 0 });
  p.until(300);
  p.press(BTN[2]);
  p.run(10 * STEP);
  p.press(BTN[7]);
  p.run(25);
  assertFrame(p, (g, r0) => r0, 'after RESET');
});
