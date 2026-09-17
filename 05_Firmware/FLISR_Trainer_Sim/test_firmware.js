/* Tests for firmware.js, the FLISR_Trainer.ino port.
 * Run:  python build_sim.py   (writes sim_config.json)
 *       node --test test_firmware.js
 *
 * Expectations come from two places:
 *   - hand traces of FLISR_Trainer.ino (exact serial text, pixel counts, timing)
 *   - model() copied verbatim from the FLISR Trainer Plan Set artifact, which
 *     the sketch says it mirrors exactly, as an independent reference
 */
'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const path = require('node:path');
const fs = require('node:fs');
const FW = require('./firmware.js');

const CFG = JSON.parse(fs.readFileSync(path.join(__dirname, 'sim_config.json'), 'utf8'));
const D = CFG.defines;
const BTN = [D.PIN_BTN_FAULT_Z1, D.PIN_BTN_FAULT_Z2, D.PIN_BTN_FAULT_Z3, D.PIN_BTN_FAULT_Z4,
             D.PIN_BTN_FAULT_Z5, D.PIN_BTN_FAULT_Z6, D.PIN_BTN_FAULT_DER, D.PIN_BTN_RESET];
const DEV_PIN = [D.PIN_DEV_SUB_A_BKR, D.PIN_DEV_DEV_A1, D.PIN_DEV_DEV_A2, D.PIN_DEV_TIE,
                 D.PIN_DEV_DEV_B2, D.PIN_DEV_DEV_B1, D.PIN_DEV_SUB_B_BKR, D.PIN_DEV_DER_PCC];
const hex = c => c.map(v => v.toString(16).padStart(2, '0')).join('');

function bench(overrides) {
  const cfg = JSON.parse(JSON.stringify(CFG));
  Object.assign(cfg.defines, overrides || {});
  const b = { text: '', writes: [], frame: null, frames: 0 };
  b.board = FW.createBoard(cfg, {
    onSerial: s => { b.text += s; b.writes.push({ t: b.board.now, s }); },
    onShow: (leds, n, scale, power) => { b.frame = { leds: leds.slice(0, n * 3), scale, power, t: b.board.now }; b.frames++; }
  });
  b.run = ms => b.board.runUntil(b.board.now + ms);
  b.press = (pin, holdMs = 100, gapMs = 150) => {
    const t = b.board.now;
    b.board.setContact(pin, true, t);
    b.board.setContact(pin, false, t + holdMs);
    b.board.runUntil(t + holdMs + gapMs);
  };
  b.states = () => [...b.text.matchAll(/STEP 0(\d)  (\w+)\r\n  fault   : (.*)\r\n  zones   : (.*)\r\n  devices : (.*)\r\n/g)]
    .map(m => ({ step: +m[1], name: m[2], fault: m[3],
                 zones: Object.fromEntries(m[4].trim().split(' ').map(p => p.split('='))),
                 devs: Object.fromEntries(m[5].trim().split(' ').map(p => p.split('='))) }));
  b.colorCounts = () => {
    const out = {};
    for (let i = 0; i < b.frame.leds.length; i += 3) {
      const k = hex([b.frame.leds[i], b.frame.leds[i + 1], b.frame.leds[i + 2]]);
      out[k] = (out[k] || 0) + 1;
    }
    return out;
  };
  return b;
}
const A = hex(D.COLOR_SRC_A), B = hex(D.COLOR_SRC_B), R = hex(D.COLOR_FAULT), K = hex(D.COLOR_DEAD);

/* ---- model() from the FLISR Trainer Plan Set artifact, verbatim ---------- */
const CHAIN = ["SUB_A_BKR","DEV_A1","DEV_A2","TIE","DEV_B2","DEV_B1","SUB_B_BKR"];
function model(f, st){
  const zone = {}, dev = {};
  for (let k=1;k<=6;k++) zone["Z"+k] = k<=3 ? "A" : "B";
  CHAIN.forEach(d => dev[d] = d==="TIE" ? "open" : "closed");
  dev.DER_PCC = "closed";
  if (st === 0) return {zone, dev, faulted:null};

  const aSide = f <= 3;
  const trip = aSide ? f-1 : f;          // source-side boundary device
  const far  = aSide ? f   : f-1;        // far-side boundary device
  const strand = aSide ? range(f,3) : range(4,f);   // zones that lose their source

  strand.forEach(k => zone["Z"+k] = "dead");
  zone["Z"+f] = "fault";
  dev[CHAIN[trip]] = st>=2 ? "lockout" : "tripped";
  if (st>=3) dev[CHAIN[far]] = "open";
  if (st>=4){
    const restored = aSide ? range(f+1,3) : range(4,f-1);
    if (restored.length){
      dev.TIE = "closed";
      restored.forEach(k => zone["Z"+k] = aSide ? "B" : "A");
    }
  }
  if (zone.Z5 === "dead" || zone.Z5 === "fault") dev.DER_PCC = "tripped";
  return {zone, dev, faulted:f};
}
function range(a,b){ const o=[]; for(let i=a;i<=b;i++) o.push(i); return o; }
/* ------------------------------------------------------------------------- */

test('boot prints the banner, the table check and STEP 00 exactly', () => {
  const b = bench();
  b.run(300);
  assert.equal(b.text,
    '\n=== JEA Tabletop FLISR Trainer ===\r\n' +
    'segment table total : 337\r\n' +
    'NUM_LEDS            : 337\r\n' +
    '[OK] segment table matches NUM_LEDS\r\n' +
    '\r\n' +
    'STEP 00  NORMAL\r\n' +
    '  fault   : none\r\n' +
    '  zones   : Z1=A Z2=A Z3=A Z4=B Z5=B Z6=B DER=B\r\n' +
    '  devices : SUB_A_BKR=CLOSED DEV_A1=CLOSED DEV_A2=CLOSED TIE=OPEN DEV_B2=CLOSED DEV_B1=CLOSED SUB_B_BKR=CLOSED DER_PCC=CLOSED \r\n');
  assert.equal(b.writes[0].t, 200, 'banner prints after delay(200)');
});

test('NORMAL frame: 161 px Source A, 73 px Source B, 103 px dark (all under-board)', () => {
  const b = bench();
  b.run(300);
  assert.deepEqual(b.colorCounts(), { [A]: 161, [B]: 73, [K]: 103 });
  assert.equal(b.frame.scale, D.BRIGHTNESS, 'power limiter does not engage');
});

for (let f = 1; f <= 6; f++) {
  test(`Z${f}: steps 01-04 by pressing the same button match the plan set model()`, () => {
    const b = bench();
    b.run(300);
    for (let n = 0; n < 4; n++) b.press(BTN[f - 1]);
    const st = b.states();
    assert.equal(st.length, 5);
    st.forEach((s, i) => {
      const m = model(f, i);
      assert.equal(s.step, i);
      assert.equal(s.fault, i === 0 ? 'none' : `Z${f}`);
      for (let k = 1; k <= 6; k++) {
        const want = { A: 'A', B: 'B', dead: 'dead', fault: 'FLT' }[m.zone['Z' + k]];
        assert.equal(s.zones['Z' + k], want, `step ${i} Z${k}`);
      }
      for (const d of [...CHAIN, 'DER_PCC'])
        assert.equal(s.devs[d === 'TIE' ? 'TIE' : d], m.dev[d].toUpperCase(), `step ${i} ${d}`);
    });
    /* one more press at RESTORE does nothing */
    const before = b.text.length;
    b.press(BTN[f - 1]);
    assert.equal(b.text.length, before);
  });
}

test('DER fault: PCC trips then locks out, feeder untouched, branch shows FLT', () => {
  const b = bench();
  b.run(300);
  for (let n = 0; n < 4; n++) b.press(BTN[6]);
  const st = b.states().slice(1);
  assert.deepEqual(st.map(s => s.devs.DER_PCC), ['TRIPPED', 'LOCKOUT', 'LOCKOUT', 'LOCKOUT']);
  st.forEach(s => {
    assert.equal(s.fault, 'DER branch');
    assert.deepEqual(s.zones, { Z1: 'A', Z2: 'A', Z3: 'A', Z4: 'B', Z5: 'B', Z6: 'B', DER: 'FLT' });
  });
  /* at ISOLATE and RESTORE the 11 DER-tail pixels hold solid red */
  assert.deepEqual(b.colorCounts(), { [A]: 161, [B]: 62, [R]: 11, [K]: 103 });
});

test('Z5 RESTORE frame: Z4 backfed from A, Z5 solid red, DER branch dark', () => {
  const b = bench();
  b.run(300);
  for (let n = 0; n < 4; n++) b.press(BTN[4]);
  b.run(40);
  assert.deepEqual(b.colorCounts(), { [A]: 177, [B]: 27, [R]: 19, [K]: 114 });
});

test('auto-advance: 01 -> 02 -> 03 -> 04 exactly STEP_INTERVAL_MS apart, then stops', () => {
  const b = bench();
  b.run(300);
  b.press(BTN[2], 100, 0);
  b.run(D.STEP_INTERVAL_MS * 5);
  const t = b.writes.filter(w => /^STEP 0$/.test(w.s)).map(w => w.t).slice(1);
  assert.equal(t.length, 4);
  assert.deepEqual([t[1] - t[0], t[2] - t[1], t[3] - t[2]], [D.STEP_INTERVAL_MS, D.STEP_INTERVAL_MS, D.STEP_INTERVAL_MS]);
});

test('debounce: a 40 ms contact is ignored, a 41 ms contact is a press', () => {
  const b = bench();
  b.run(300);
  b.press(BTN[0], 40, 200);
  assert.equal(b.states().length, 1);
  const closedAt = b.board.now;
  b.press(BTN[0], 41, 200);
  assert.equal(b.states().length, 2);
  const w = b.writes.filter(x => x.s === 'STEP 0').pop();
  assert.equal(w.t - closedAt, 40, 'recognized 40 ms after the contact closed');
});

test('two buttons in the same pass: only the lower index is handled, the other is swallowed', () => {
  const b = bench();
  b.run(300);
  const t = b.board.now;
  b.board.setContact(BTN[1], true, t); b.board.setContact(BTN[4], true, t);
  b.board.setContact(BTN[1], false, t + 100); b.board.setContact(BTN[4], false, t + 100);
  b.run(400);
  const st = b.states();
  assert.equal(st.length, 2);
  assert.equal(st[1].fault, 'Z2');
});

test('a different fault button abandons the current fault, RESET returns to 00', () => {
  const b = bench();
  b.run(300);
  b.press(BTN[0]); b.press(BTN[0]);
  b.press(BTN[3]);
  b.press(BTN[7]);
  assert.deepEqual(b.states().map(s => `${s.step}:${s.fault}`), ['0:none', '1:Z1', '2:Z1', '1:Z4', '0:none']);
});

test('fault blink: faulted pixels alternate every FAULT_BLINK_MS at steps 01-02', () => {
  const b = bench();
  b.run(300);
  b.press(BTN[2], 100, 0);                       /* Z3, 89 px */
  /* sample 30 ms into each window; lit when floor(millis / 350) is odd */
  const got = [], want = [];
  for (let t = Math.ceil((b.board.now + 1) / 350) * 350 + 30; got.length < 4; t += 350) {
    b.board.runUntil(t);
    got.push(b.colorCounts()[R] || 0);
    want.push((Math.floor(b.frame.t / 350) & 1) ? 89 : 0);
    assert.equal(Math.floor(b.frame.t / 350), Math.floor((t - 30) / 350), 'frame is from this window');
  }
  assert.deepEqual(got, want);
  assert.ok(got.includes(89) && got.includes(0));
});

test('device LED pins: CLOSED solid, TRIPPED slow blink, LOCKOUT fast blink, OPEN off', () => {
  const b = bench();
  b.run(300);
  const lvl = p => b.board.pinLevel(p);
  assert.equal(lvl(DEV_PIN[0]), 1);
  assert.equal(lvl(DEV_PIN[3]), 0, 'TIE is open');

  b.press(BTN[0], 100, 0);                        /* Z1 01: SUB_A_BKR TRIPPED */
  const at = t => { b.board.runUntil(t + 1); return lvl(DEV_PIN[0]); };
  const base = Math.ceil(b.board.now / 1000) * 1000;
  assert.deepEqual([at(base + 100), at(base + 600), at(base + 1100)], [0, 1, 0]);

  b.press(BTN[0], 100, 0);                        /* 02: LOCKOUT */
  const base2 = Math.ceil(b.board.now / 300) * 300;
  assert.deepEqual([at(base2 + 20), at(base2 + 170), at(base2 + 320)], [0, 1, 0]);

  b.press(BTN[0], 100, 50);                       /* 03: DEV_A1 OPEN */
  assert.equal(lvl(DEV_PIN[1]), 0);
});

test('FastLED power limiter matches power_mgt.cpp.hpp for a full-white frame', () => {
  let got = null;
  const fl = FW.makeFastLED((leds, n, scale, p) => { got = { scale, p }; });
  const leds = new Uint8Array(337 * 3).fill(255);
  fl.addLeds('WS2812B', 10, 'GRB', leds, 337);
  fl.setBrightness(80);
  fl.setMaxPowerInVoltsAndMilliamps(5, 4000);
  fl.show();
  /* 125 + (85935*80>>8) + (85935*55>>8) + (85935*75>>8) + 5*337 = 72302 mW,
     at brightness 80: 72302*81>>8 = 22876 > 20000 -> 80*20000/22876 = 69   */
  assert.equal(got.p.total_mW, 72302);
  assert.equal(got.p.requested_mW, 22876);
  assert.equal(got.scale, 69);
});

test('hsv2rgb_rainbow matches FastLED reference hues', () => {
  assert.deepEqual(FW.hsv2rgb_rainbow(0, 255, 255), [255, 0, 0]);
  assert.deepEqual(FW.hsv2rgb_rainbow(32, 255, 255), [171, 85, 0]);
  assert.deepEqual(FW.hsv2rgb_rainbow(96, 255, 255), [0, 255, 0]);
  assert.deepEqual(FW.hsv2rgb_rainbow(160, 255, 255), [0, 0, 255]);
});

test('SEGMENT_TEST_MODE 1: walks 30 runs (J1 skipped) at SEGMENT_TEST_MS, then STEP 00', () => {
  const b = bench({ SEGMENT_TEST_MODE: 1 });
  b.run(200 + 30 * D.SEGMENT_TEST_MS + 5);
  const segs = [...b.text.matchAll(/segment (\d+)  px (\d+) \.\. (\d+)  len (\d+)\r\n/g)].map(m => m.slice(1).map(Number));
  assert.equal(segs.length, 30);
  assert.deepEqual(segs[0], [1, 0, 16, 17]);
  assert.deepEqual(segs[24], [26, 287, 293, 7]);
  assert.deepEqual(segs[29], [31, 324, 336, 13]);
  assert.equal(b.states().length, 1);
  assert.equal(b.writes.find(w => w.s === 'STEP 0').t, 200 + 30 * D.SEGMENT_TEST_MS);
});

test('DEVICE_LED_MODE 2: green = CLOSED, red = OPEN', () => {
  const over = { DEVICE_LED_MODE: 2 };
  const names = ['SUB_A_BKR', 'DEV_A1', 'DEV_A2', 'TIE', 'DEV_B2', 'DEV_B1', 'SUB_B_BKR', 'DER_PCC'];
  names.forEach((n, i) => { over['PIN_DEVG_' + n] = 22 + 2 * i; over['PIN_DEVR_' + n] = 23 + 2 * i; });
  const b = bench(over);
  b.run(300);
  assert.deepEqual([b.board.pinLevel(28), b.board.pinLevel(29)], [0, 1], 'TIE open: green off, red on');
  assert.deepEqual([b.board.pinLevel(24), b.board.pinLevel(25)], [1, 0], 'DEV_A1 closed');
});
