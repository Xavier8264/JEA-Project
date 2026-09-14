/* Tests for firmware_rev1.js, the FLISR_Trainer_REV1.ino port.
 * Run:  python build_sim.py && python build_sim.py --sketch FLISR_Trainer_REV1
 *       node --test test_firmware_rev1.js
 *
 * Two independent references:
 *   - REV0 (firmware.js, already tested) driven with the same button presses.
 *     Outside the animations REV1 must match it frame for frame.
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
const REV1 = require('./firmware_rev1.js');

const load = f => JSON.parse(fs.readFileSync(path.join(__dirname, f), 'utf8'));
const CFG0 = load('sim_config.json'), CFG1 = load('sim_config_rev1.json');
const D = CFG1.defines, T = CFG1.tables;
const BTN = [D.PIN_BTN_FAULT_Z1, D.PIN_BTN_FAULT_Z2, D.PIN_BTN_FAULT_Z3, D.PIN_BTN_FAULT_Z4,
             D.PIN_BTN_FAULT_Z5, D.PIN_BTN_FAULT_Z6, D.PIN_BTN_FAULT_DER, D.PIN_BTN_RESET];
const RED = D.COLOR_FAULT, A = D.COLOR_SRC_A, B = D.COLOR_SRC_B, K = D.COLOR_DEAD;
const STEP = D.ANIM_STEP_MS;

function bench(FW, cfg, overrides) {
  cfg = JSON.parse(JSON.stringify(cfg));
  Object.assign(cfg.defines, overrides || {});
  const b = { text: '', writes: [], frame: null };
  b.board = FW.createBoard(cfg, {
    onSerial: s => { b.text += s; b.writes.push({ t: b.board.now, s }); },
    onShow: (leds, n) => { b.frame = { leds: leds.slice(0, n * 3), t: b.board.now }; }
  });
  b.states = () => [...b.text.matchAll(/STEP 0(\d)  (\w+)\r\n  fault   : (.*)\r\n  zones   : (.*)\r\n  devices : (.*)\r\n/g)]
    .map(m => ({ step: +m[1], zones: Object.fromEntries(m[4].trim().split(' ').map(p => p.split('='))) }));
  b.stepTimes = () => b.writes.filter(w => w.s === 'STEP 0').map(w => w.t);
  return b;
}

/* two boards, same inputs, same clock */
function pair(overrides) {
  const p = { r0: bench(REV0, CFG0, overrides), r1: bench(REV1, CFG1, overrides) };
  p.until = t => { p.r0.board.runUntil(t); p.r1.board.runUntil(t); };
  p.run = ms => p.until(p.r1.board.now + ms);
  p.press = (pin, holdMs = 60) => {
    const t = p.r1.board.now;
    for (const b of [p.r0, p.r1]) { b.board.setContact(pin, true, t); b.board.setContact(pin, false, t + holdMs); }
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
function assertFrame(p, expectFn, label) {
  const f0 = p.r0.frame, f1 = p.r1.frame;
  assert.equal(f1.t, f0.t, `${label}: both boards rendered at the same ms`);
  for (let g = 0; g < NUM; g++) {
    const want = expectFn(g, px(f0, g), f1.t);
    assert.deepEqual(px(f1, g), want, `${label}: px ${g} at ${f1.t} ms (run idx ${pxRun[g]} pixel ${pxOff[g]})`);
  }
}
const FAULT_NAMES = ['Z1', 'Z2', 'Z3', 'Z4', 'Z5', 'Z6', 'DER'];

/* ======================================================================= */

test('boot: banner says REV1, then output and the NORMAL frame match REV0', () => {
  const p = pair();
  p.until(300);
  assert.ok(p.r1.text.startsWith('\n=== JEA Tabletop FLISR Trainer REV1 ===\r\n'));
  assert.equal(p.r1.text.replace(' REV1 ===', ' ==='), p.r0.text);
  assertFrame(p, (g, r0) => r0, 'NORMAL');
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
    const start = p.r1.stepTimes()[1];
    const st1 = p.r1.states()[1].zones;
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
    for (let t = p.r1.board.now + 1; t <= waveEnd + 800; t += 20) { p.until(t); assertFrame(p, faultRule, '01'); }

    /* 02 LOCKOUT: same picture */
    p.press(BTN[f]);
    for (let n = 0; n < 10; n++) { p.run(37); assertFrame(p, faultRule, '02'); }

    /* 03 ISOLATE: no animation, identical to REV0 */
    p.press(BTN[f]);
    for (let n = 0; n < 10; n++) { p.run(37); assertFrame(p, (g, r0) => r0, '03'); }

    /* 04 RESTORE: the new source color fills out from the tie, if the tie closes */
    p.press(BTN[f]);
    const rstart = p.r1.stepTimes()[4];
    const restored = restoredMask(p.r1.states()[4].zones);
    let rlast = 0, rdist = null;
    if (restored) {
      rdist = bfs(atNode.get(D.TIE_NODE).map(g => [g, 1]), restored);
      for (let g = 0; g < NUM; g++) if (restored & (1 << zoneOf(g))) {
        assert.ok(Number.isFinite(rdist[g]), `restored px ${g} is reachable from the tie`);
        rlast = Math.max(rlast, rdist[g]);
      }
    }
    const restoreRule = (g, r0, t) => {
      if (!restored || !(restored & (1 << zoneOf(g)))) return r0;
      const front = Math.floor((t - rstart) / STEP);
      return (front >= rlast || rdist[g] <= front) ? r0 : K;
    };
    for (let t = p.r1.board.now + 1; t <= rstart + rlast * STEP + 400; t += 20) { p.until(t); assertFrame(p, restoreRule, '04'); }

    assert.equal(p.r1.text.replace(' REV1 ===', ' ==='), p.r0.text, 'serial output identical to REV0');
    if (f === 0 || f === 1 || f === 4 || f === 5) assert.ok(restored, 'this fault restores load across the tie');
    else assert.equal(restored, 0, 'no stranded load, tie stays open');
  });
}

test('auto-advance waits for each animation, then STEP_INTERVAL_MS', () => {
  const b = bench(REV1, CFG1);
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
  const start = p.r1.stepTimes()[1];
  const lost = lostMask(p.r1.states()[1].zones);
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
  assertFrame(p, (g, r0) => r0, '03 right after');
});

test('a different fault button mid-wave starts a new wave from normal colors', () => {
  const p = pair({ AUTO_ADVANCE: 0 });
  p.until(300);
  p.press(BTN[0]);
  p.run(15 * STEP);
  p.press(BTN[5]);                                 /* Z6 */
  const start = p.r1.stepTimes()[2];
  const lost = lostMask(p.r1.states()[2].zones);
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
