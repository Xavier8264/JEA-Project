/* ===========================================================================
 * FLISR_Trainer_REV2 firmware port
 * ---------------------------------------------------------------------------
 * A line-for-line JavaScript port of the LOGIC section of
 * FLISR_Trainer_REV2/FLISR_Trainer_REV2.ino, meaning everything below the line
 * "NOTHING BELOW HERE NEEDS EDITING". Function names, statement order and
 * integer widths follow the sketch so the two can be read side by side.
 *
 * REV2's logic section is REV1's with one change, the boot banner. REV2's
 * differences are all in the config tables, which come from `cfg`.
 *
 * Nothing configurable is typed in here. Pins, colors, timing, and the
 * segment table come from `cfg`, which build_sim.py extracts from the .ino
 * itself. If the logic section of the .ino changes, build_sim.py refuses to
 * build until this port is updated and PORTED_LOGIC_SHA256 below is bumped.
 *
 * Library behavior the sketch depends on is ported from the installed
 * FastLED 3.10.5 source (power_mgt.cpp.hpp, hsv2rgb.cpp.hpp, scale8.h).
 *
 * Runs in the browser (window.FLISR) and in Node (module.exports).
 * =========================================================================== */
(function (root) {
'use strict';

const PORTED_LOGIC_SHA256 = '1bb43e0321657ddbce6d245b26fbfd68cf16c76f9cdd821da2647adc8a50bc43';

const u8  = v => v & 0xFF;
const u16 = v => v & 0xFFFF;
const u32 = v => v >>> 0;

const LOW = 0, HIGH = 1;
const INPUT = 0, OUTPUT = 1, INPUT_PULLUP = 2;

/* ---------------------------------------------------------------------------
 * FastLED pieces the sketch touches
 * ------------------------------------------------------------------------- */

/* scale8, FASTLED_SCALE8_FIXED == 1 (fastled_config.h) */
function scale8(i, scale) { return ((i * (1 + scale)) >> 8) & 0xFF; }

/* scale32by8, FASTLED_SCALE8_FIXED == 1 */
function scale32by8(i, scale) {
  if (scale === 0) return 0;
  return Math.floor((i * (1 + scale)) / 256) >>> 0;
}

/* hsv2rgb_rainbow with Y1=1, Y2=0, G2=0, Gscale=0. CRGB = CHSV routes here
 * (fl/gfx/crgb_extra.cpp.hpp). The sketch only ever passes sat=255, val=255,
 * so the desaturate and dim tails are not ported and are guarded instead.  */
function hsv2rgb_rainbow(hue, sat, val) {
  if (sat !== 255 || val !== 255)
    throw new Error('hsv2rgb_rainbow: only sat=255 val=255 is ported');
  const offset8 = ((hue & 0x1F) << 3) & 0xFF;
  const third = scale8(offset8, 85);                 /* 256 / 3 */
  let r, g, b;
  if (!(hue & 0x80)) {
    if (!(hue & 0x40)) {
      if (!(hue & 0x20)) { r = 255 - third; g = third;      b = 0; }
      else               { r = 171;         g = 85 + third; b = 0; }
    } else {
      if (!(hue & 0x20)) {
        const twothirds = scale8(offset8, 170);         /* 512 / 3 */
        r = 171 - twothirds; g = 170 + third; b = 0;
      } else             { r = 0; g = 255 - third; b = third; }
    }
  } else {
    if (!(hue & 0x40)) {
      if (!(hue & 0x20)) {
        const twothirds = scale8(offset8, 170);
        r = 0; g = 171 - twothirds; b = 85 + twothirds;
      } else             { r = third; g = 0; b = 255 - third; }
    } else {
      if (!(hue & 0x20)) { r = 85 + third;  g = 0; b = 171 - third; }
      else               { r = 170 + third; g = 0; b = 85 - third; }
    }
  }
  return [u8(r), u8(g), u8(b)];
}

/* CFastLED as used by the sketch: one controller, brightness, and the
 * setMaxPowerInVoltsAndMilliamps() limiter. show() hands the frame to the
 * board along with the scale FastLED would actually clock out.            */
function makeFastLED(onShow) {
  let leds = null, numLeds = 0, brightness = 255, maxPower_mW = 0, correction = null;
  return {
    addLeds(type, dataPin, order, buffer, n) {
      leds = buffer; numLeds = n;
      const ctl = { type, dataPin, order, setCorrection(c) { correction = c; return ctl; } };
      return ctl;
    },
    setBrightness(b) { brightness = u8(b); },
    setMaxPowerInVoltsAndMilliamps(volts, milliamps) { maxPower_mW = u32(u8(volts) * milliamps); },
    show() {
      let scale = brightness, requested_mW = 0, total_mW = 0;
      if (maxPower_mW) {
        /* calculate_max_brightness_for_power_mW(target, max_mW), 2-arg form */
        let r = 0, g = 0, b = 0;
        for (let i = 0; i < numLeds; i++) { r += leds[i * 3]; g += leds[i * 3 + 1]; b += leds[i * 3 + 2]; }
        r = u32(r * 80) >>> 8;  g = u32(g * 55) >>> 8;  b = u32(b * 75) >>> 8;
        total_mW = 125 /* gMCU_mW */ + r + g + b + 5 * numLeds;
        requested_mW = scale32by8(total_mW, scale);
        if (!(requested_mW < maxPower_mW))
          scale = u8(Math.floor((scale * maxPower_mW) / requested_mW));
      }
      onShow(leds, numLeds, scale, { requested_mW, total_mW, maxPower_mW, brightness, correction });
    }
  };
}

function fill_solid(leds, n, rgb) {
  for (let i = 0; i < n; i++) { leds[i * 3] = rgb[0]; leds[i * 3 + 1] = rgb[1]; leds[i * 3 + 2] = rgb[2]; }
}

/* Arduino Print: print(x) writes x, numbers in decimal. F() is identity. */
function makeSerial(write) {
  const s = v => (typeof v === 'number' ? String(Math.trunc(v)) : String(v));
  return {
    begin() {},
    print(v)       { write(s(v)); },
    println(v)     { write((v === undefined ? '' : s(v)) + '\r\n'); }
  };
}
const F = s => s;

/* ===========================================================================
 * The sketch
 * =========================================================================== */
function createFirmware(cfg, hal) {
  const D = cfg.defines, T = cfg.tables;
  const { millis, pinMode, digitalRead, pgm_read_byte } = hal;
  const Serial = hal.Serial, FastLED = hal.FastLED;
  const NUM_LEDS = D.NUM_LEDS, NUM_SEGMENTS = D.NUM_SEGMENTS;
  const BLACK = [0, 0, 0];

  /* ---- device chain ---------------------------------------------------- */
  const DEV_SUB_A_BKR = 0, DEV_A1 = 1, DEV_A2 = 2, DEV_TIE = 3, DEV_B2 = 4,
        DEV_B1 = 5, DEV_SUB_B_BKR = 6, DEV_DER_PCC = 7;
  const NUM_DEVICES = D.NUM_DEVICES;                 /* block [2] */

  /* ---- states ---------------------------------------------------------- */
  const ZS_A = 0, ZS_B = 1, ZS_DEAD = 2, ZS_FAULT = 3;
  const DS_CLOSED = 0, DS_OPEN = 1, DS_TRIPPED = 2, DS_LOCKOUT = 3;

  /* ---- steps ----------------------------------------------------------- */
  const ST_NORMAL = 0, ST_FAULT = 1, ST_LOCKOUT = 2, ST_ISOLATE = 3, ST_RESTORE = 4, ST_LAST = 4;

  /* ---- fault selection ------------------------------------------------- */
  const FAULT_NONE = 0, FAULT_DER = 7;

  /* ---- buttons --------------------------------------------------------- */
  const NUM_BUTTONS = 8, BTN_DER_IDX = 6, BTN_RESET_IDX = 7;

  /* ---- animations (REV1) ----------------------------------------------- */
  const ANIM_NONE = 0, ANIM_FAULT = 1, ANIM_RESTORE = 2;
  const NUM_POINTS = D.NUM_NODES + NUM_SEGMENTS;
  const DIST_NONE = 255, SRC_IS_TIE = 255;

  const BTN_PIN = [
    D.PIN_BTN_FAULT_Z1, D.PIN_BTN_FAULT_Z2, D.PIN_BTN_FAULT_Z3, D.PIN_BTN_FAULT_Z4,
    D.PIN_BTN_FAULT_Z5, D.PIN_BTN_FAULT_Z6, D.PIN_BTN_FAULT_DER, D.PIN_BTN_RESET
  ];

  /* ---- runtime state (globals are zero-initialized, as in C) ----------- */
  const leds = new Uint8Array(NUM_LEDS * 3);

  let faultSel = FAULT_NONE;
  let stepNow  = ST_NORMAL;

  const zoneState = new Uint8Array(7);          /* index 1..6 used, 0 unused */
  const devState  = new Uint8Array(NUM_DEVICES);
  let derFaulted = false;

  let stepStartedAt = 0;
  const btnStable    = new Array(NUM_BUTTONS).fill(false);
  const btnLast      = new Array(NUM_BUTTONS).fill(false);
  const btnChangedAt = new Uint32Array(NUM_BUTTONS);

  /* REV1 animation state */
  let animKind      = ANIM_NONE;
  let animActive    = false;
  let animStartedAt = 0;
  let animLast      = 0;
  let animZones     = 0;
  let faultZones    = 0;
  let animSrcSeg    = SRC_IS_TIE;
  let animSrcPx     = 0;
  const pointDist   = new Uint8Array(NUM_POINTS);

  const setLed = (i, rgb) => { leds[i * 3] = rgb[0]; leds[i * 3 + 1] = rgb[1]; leds[i * 3 + 2] = rgb[2]; };

  /* ======================================================================
   * FLISR MODEL
   * ==================================================================== */
  function computeModel() {
    for (let k = 1; k <= 6; k++) zoneState[k] = (k <= 3) ? ZS_A : ZS_B;
    for (let d = 0; d < NUM_DEVICES; d++) devState[d] = DS_CLOSED;
    devState[DEV_TIE] = DS_OPEN;
    derFaulted = false;

    if (stepNow === ST_NORMAL || faultSel === FAULT_NONE) return;

    if (faultSel === FAULT_DER) {
      derFaulted = true;
      devState[DEV_DER_PCC] = (stepNow >= ST_LOCKOUT) ? DS_LOCKOUT : DS_TRIPPED;
      return;
    }

    const f       = faultSel;
    const aSide   = (f <= 3);
    const trip    = aSide ? u8(f - 1) : f;
    const farSide = aSide ? f : u8(f - 1);

    if (aSide) { for (let k = f; k <= 3; k++) zoneState[k] = ZS_DEAD; }
    else       { for (let k = 4; k <= f; k++) zoneState[k] = ZS_DEAD; }
    zoneState[f] = ZS_FAULT;

    devState[trip] = (stepNow >= ST_LOCKOUT) ? DS_LOCKOUT : DS_TRIPPED;

    if (stepNow >= ST_ISOLATE) devState[farSide] = DS_OPEN;

    if (stepNow >= ST_RESTORE) {
      const lo = aSide ? u8(f + 1) : 4;
      const hi = aSide ? 3 : u8(f - 1);
      if (lo <= hi) {
        devState[DEV_TIE] = DS_CLOSED;
        for (let k = lo; k <= hi; k++) zoneState[k] = aSide ? ZS_B : ZS_A;
      }
    }

    if (zoneState[5] === ZS_DEAD || zoneState[5] === ZS_FAULT)
      devState[DEV_DER_PCC] = DS_TRIPPED;
  }

  function derDisplayState() {
    if (derFaulted)                          return ZS_FAULT;
    if (devState[DEV_DER_PCC] !== DS_CLOSED) return ZS_DEAD;
    return zoneState[5];
  }

  /* ======================================================================
   * LINE WALKING (REV1)
   * ==================================================================== */
  /* Piece k of run s: fills p {lo, hi, a, b}. False when none. */
  function getPiece(s, k, p) {
    const len = pgm_read_byte(T.SEG_LEN, s);
    if (len === 0) return false;

    const cutPx = [0, 0], cutPt = [0, 0];
    let n = 0;
    const split = pgm_read_byte(T.SEG_SPLIT, s);
    if (split) { cutPx[n] = split; cutPt[n] = u8(D.NUM_NODES + s); n++; }
    for (let t = 0; t < D.NUM_TAPS && n < 2; t++) {
      if (pgm_read_byte(T.TAP_SEG, t) !== s) continue;
      cutPx[n] = pgm_read_byte(T.TAP_PX, t);
      cutPt[n] = pgm_read_byte(T.TAP_NODE, t);
      n++;
    }
    if (n === 2 && cutPx[1] < cutPx[0]) {
      let x = cutPx[0]; cutPx[0] = cutPx[1]; cutPx[1] = x;
      x = cutPt[0]; cutPt[0] = cutPt[1]; cutPt[1] = x;
    }
    if (k > n) return false;

    p.lo = (k === 0) ? 0 : cutPx[k - 1];
    p.hi = (k === n) ? u8(len - 1) : u8(cutPx[k] - 1);
    p.a  = (k === 0) ? pgm_read_byte(T.SEG_FROM, s) : cutPt[k - 1];
    p.b  = (k === n) ? pgm_read_byte(T.SEG_TO, s)   : cutPt[k];
    return true;
  }

  function zoneOfPixel(s, i) {
    if (!pgm_read_byte(T.SEG_OVER, s)) return D.ZN_HID;
    const split = pgm_read_byte(T.SEG_SPLIT, s);
    return (split && i >= split) ? pgm_read_byte(T.SEG_ZONE2, s)
                                 : pgm_read_byte(T.SEG_ZONE, s);
  }

  function addSteps(d, n) {
    const v = u16(d + n);
    return (v >= DIST_NONE) ? u8(DIST_NONE - 1) : u8(v);
  }

  function distInPiece(s, i, p) {
    if (s === animSrcSeg && animSrcPx >= p.lo && animSrcPx <= p.hi)
      return (i > animSrcPx) ? u8(i - animSrcPx) : u8(animSrcPx - i);

    let d = DIST_NONE;
    if (pointDist[p.a] !== DIST_NONE) d = addSteps(pointDist[p.a], i - p.lo + 1);
    if (pointDist[p.b] !== DIST_NONE) {
      const e = addSteps(pointDist[p.b], p.hi - i + 1);
      if (e < d) d = e;
    }
    return d;
  }

  function computeDistances() {
    for (let q = 0; q < NUM_POINTS; q++) pointDist[q] = DIST_NONE;

    const p = {};
    if (animSrcSeg === SRC_IS_TIE) {
      pointDist[D.TIE_NODE] = 0;
    } else {
      for (let k = 0; getPiece(animSrcSeg, k, p); k++) {
        if (animSrcPx < p.lo || animSrcPx > p.hi) continue;
        pointDist[p.a] = u8(animSrcPx - p.lo);
        pointDist[p.b] = u8(p.hi - animSrcPx);
      }
    }

    let changed = true;
    for (let pass = 0; changed && pass < NUM_POINTS; pass++) {
      changed = false;
      for (let s = 0; s < NUM_SEGMENTS; s++) {
        if (!pgm_read_byte(T.SEG_OVER, s)) continue;
        for (let k = 0; getPiece(s, k, p); k++) {
          if (!(animZones & (1 << zoneOfPixel(s, p.lo)))) continue;
          const n = u8(p.hi - p.lo + 1);
          if (pointDist[p.a] !== DIST_NONE && addSteps(pointDist[p.a], n) < pointDist[p.b]) {
            pointDist[p.b] = addSteps(pointDist[p.a], n); changed = true;
          }
          if (pointDist[p.b] !== DIST_NONE && addSteps(pointDist[p.b], n) < pointDist[p.a]) {
            pointDist[p.a] = addSteps(pointDist[p.b], n); changed = true;
          }
        }
      }
    }
  }

  function animFront() {
    const steps = Math.floor(u32(millis() - animStartedAt) / D.ANIM_STEP_MS);
    return (steps > 0xFFFF) ? 0xFFFF : steps;
  }

  function startAnimation() {
    if (stepNow === ST_LOCKOUT) return;

    animKind   = ANIM_NONE;
    animActive = false;
    animZones  = 0;
    faultZones = 0;

    if (stepNow === ST_FAULT) {
      for (let k = 1; k <= 6; k++) {
        if (zoneState[k] === ZS_DEAD || zoneState[k] === ZS_FAULT) animZones |= (1 << k);
        if (zoneState[k] === ZS_FAULT) faultZones |= (1 << k);
      }
      const der = derDisplayState();
      if (der === ZS_DEAD || der === ZS_FAULT) animZones |= (1 << D.ZN_DER);
      if (der === ZS_FAULT) faultZones |= (1 << D.ZN_DER);

      animSrcSeg = pgm_read_byte(T.FAULT_SEG, faultSel - 1);
      animSrcPx  = pgm_read_byte(T.FAULT_PX, faultSel - 1);
      animKind   = ANIM_FAULT;
    }
    else if (stepNow === ST_RESTORE && devState[DEV_TIE] === DS_CLOSED) {
      for (let k = 1; k <= 6; k++) {
        if ((k <= 3 && zoneState[k] === ZS_B) || (k >= 4 && zoneState[k] === ZS_A))
          animZones |= (1 << k);
      }
      if ((animZones & (1 << 5)) && derDisplayState() === ZS_A) animZones |= (1 << D.ZN_DER);

      animSrcSeg = SRC_IS_TIE;
      animKind   = ANIM_RESTORE;
    }
    if (animKind === ANIM_NONE) return;

    computeDistances();

    animLast = 0;
    const p = {};
    for (let s = 0; s < NUM_SEGMENTS; s++) {
      if (!pgm_read_byte(T.SEG_OVER, s)) continue;
      for (let k = 0; getPiece(s, k, p); k++) {
        if (!(animZones & (1 << zoneOfPixel(s, p.lo)))) continue;
        for (let i = p.lo; i <= p.hi; i++) {
          const d = distInPiece(s, i, p);
          if (d !== DIST_NONE && d > animLast) animLast = d;
        }
      }
    }

    animStartedAt = millis();
    animActive = true;
  }

  /* ======================================================================
   * RENDER
   * ==================================================================== */
  function colorForState(s, blinkOn) {
    switch (s) {
      case ZS_A:     return D.COLOR_SRC_A;
      case ZS_B:     return D.COLOR_SRC_B;
      case ZS_FAULT: return blinkOn ? D.COLOR_FAULT : D.COLOR_DEAD;
      default:       return D.COLOR_FAULT;
    }
  }

  function colorForZone(zn, blinkOn) {
    if (zn === D.ZN_HID)  return D.COLOR_DEAD;
    if (zn === D.ZN_BUSA) return D.COLOR_SRC_A;
    if (zn === D.ZN_DER)  return colorForState(derDisplayState(), blinkOn);
    return colorForState(zoneState[zn], blinkOn);
  }

  function colorForPixel(zn, s, i, p, front, blinkOn) {
    if (zn === D.ZN_HID || zn === D.ZN_BUSA || !(animZones & (1 << zn)))
      return colorForZone(zn, blinkOn);

    if (animKind === ANIM_FAULT) {
      if (animActive) {
        if (distInPiece(s, i, p) <= front) return D.COLOR_FAULT;
        return (zn <= D.ZN_Z3) ? D.COLOR_SRC_A : D.COLOR_SRC_B;
      }
      if (!(faultZones & (1 << zn))) return D.COLOR_FAULT;
      return colorForZone(zn, blinkOn);
    }

    if (animKind === ANIM_RESTORE && animActive && distInPiece(s, i, p) > front)
      return D.COLOR_FAULT;

    return colorForZone(zn, blinkOn);
  }

  function colorForDevice(d, slowOn, fastOn) {
    switch (devState[d]) {
      case DS_CLOSED:  return D.COLOR_DEV_CLOSED;
      case DS_OPEN:    return D.COLOR_DEV_OPEN;
      case DS_TRIPPED: return slowOn ? D.COLOR_DEV_OPEN : D.COLOR_DEAD;
      default:         return fastOn ? D.COLOR_DEV_OPEN : D.COLOR_DEAD;
    }
  }

  function stripIndex(s, i) {
    let idx = i;
    for (let k = 0; k < s && k < NUM_SEGMENTS; k++) idx = u16(idx + pgm_read_byte(T.SEG_LEN, k));
    return idx;
  }

  function render() {
    const blinking = (stepNow === ST_FAULT || stepNow === ST_LOCKOUT);
    const blinkOn  = blinking ? ((Math.floor(millis() / D.FAULT_BLINK_MS) & 1) !== 0) : true;
    const slowOn   = (Math.floor(millis() / D.DEV_TRIP_BLINK_MS) & 1) !== 0;
    const fastOn   = (Math.floor(millis() / D.DEV_LOCK_BLINK_MS) & 1) !== 0;
    const front = animFront();

    let idx = 0;
    for (let s = 0; s < NUM_SEGMENTS; s++) {
      const len   = pgm_read_byte(T.SEG_LEN, s);
      const over  = pgm_read_byte(T.SEG_OVER, s);
      const split = pgm_read_byte(T.SEG_SPLIT, s);
      const zHead = pgm_read_byte(T.SEG_ZONE, s);
      const zTail = pgm_read_byte(T.SEG_ZONE2, s);

      const p = {};
      let pk = 0;
      getPiece(s, 0, p);

      for (let i = 0; i < len; i = u8(i + 1)) {
        if (idx >= NUM_LEDS) break;
        if (i > p.hi) getPiece(s, ++pk, p);
        let zn = (split && i >= split) ? zTail : zHead;
        if (!over) zn = D.ZN_HID;
        setLed(idx, colorForPixel(zn, s, i, p, front, blinkOn)); idx = u16(idx + 1);
      }
    }
    while (idx < NUM_LEDS) { setLed(idx, D.COLOR_DEAD); idx = u16(idx + 1); }

    for (let d = 0; d < NUM_DEVICES; d++) {
      const at = stripIndex(pgm_read_byte(T.DEV_SEG, d), pgm_read_byte(T.DEV_PX, d));
      if (at < NUM_LEDS) setLed(at, colorForDevice(d, slowOn, fastOn));
    }

    FastLED.show();
  }

  /* ======================================================================
   * SERIAL NARRATION
   * ==================================================================== */
  function printDeviceName(d) {
    switch (d) {
      case DEV_SUB_A_BKR: Serial.print(F('SUB_A_BKR')); break;
      case DEV_A1:        Serial.print(F('DEV_A1'));    break;
      case DEV_A2:        Serial.print(F('DEV_A2'));    break;
      case DEV_TIE:       Serial.print(F('TIE'));       break;
      case DEV_B2:        Serial.print(F('DEV_B2'));    break;
      case DEV_B1:        Serial.print(F('DEV_B1'));    break;
      case DEV_SUB_B_BKR: Serial.print(F('SUB_B_BKR')); break;
      default:            Serial.print(F('DER_PCC'));   break;
    }
  }

  function printZState(z) {
    switch (z) {
      case ZS_A:     Serial.print(F('A'));    break;
      case ZS_B:     Serial.print(F('B'));    break;
      case ZS_FAULT: Serial.print(F('FLT'));  break;
      default:       Serial.print(F('dead')); break;
    }
  }

  function printState() {
    Serial.println();
    Serial.print(F('STEP 0'));
    Serial.print(stepNow);
    Serial.print(F('  '));
    switch (stepNow) {
      case ST_NORMAL:  Serial.println(F('NORMAL'));  break;
      case ST_FAULT:   Serial.println(F('FAULT'));   break;
      case ST_LOCKOUT: Serial.println(F('LOCKOUT')); break;
      case ST_ISOLATE: Serial.println(F('ISOLATE')); break;
      default:         Serial.println(F('RESTORE')); break;
    }

    Serial.print(F('  fault   : '));
    if      (faultSel === FAULT_NONE) Serial.println(F('none'));
    else if (faultSel === FAULT_DER)  Serial.println(F('DER branch'));
    else  { Serial.print(F('Z')); Serial.println(faultSel); }

    Serial.print(F('  zones   : '));
    for (let k = 1; k <= 6; k++) {
      Serial.print(F('Z')); Serial.print(k); Serial.print(F('='));
      printZState(zoneState[k]);
      Serial.print(F(' '));
    }
    Serial.print(F('DER='));
    printZState(derDisplayState());
    Serial.println();

    Serial.print(F('  devices : '));
    for (let d = 0; d < NUM_DEVICES; d++) {
      printDeviceName(d);
      Serial.print(F('='));
      switch (devState[d]) {
        case DS_CLOSED:  Serial.print(F('CLOSED'));  break;
        case DS_OPEN:    Serial.print(F('OPEN'));    break;
        case DS_TRIPPED: Serial.print(F('TRIPPED')); break;
        default:         Serial.print(F('LOCKOUT')); break;
      }
      Serial.print(F(' '));
    }
    Serial.println();
  }

  /* ======================================================================
   * STATE TRANSITIONS
   * ==================================================================== */
  function goToStep(s) {
    stepNow = u8(s);
    stepStartedAt = millis();
    computeModel();
    startAnimation();
    printState();
  }

  function startFault(f) {
    faultSel = u8(f);
    goToStep(ST_FAULT);
  }

  function resetAll() {
    faultSel = FAULT_NONE;
    goToStep(ST_NORMAL);
  }

  /* ======================================================================
   * BUTTONS
   * ==================================================================== */
  function initButtons() {
    for (let b = 0; b < NUM_BUTTONS; b++) {
      pinMode(pgm_read_byte(BTN_PIN, b), INPUT_PULLUP);
      btnStable[b]    = true;
      btnLast[b]      = true;
      btnChangedAt[b] = 0;
    }
  }

  function pollButtons() {
    let pressed = 255;
    const now = millis();

    for (let b = 0; b < NUM_BUTTONS; b++) {
      const raw = (digitalRead(pgm_read_byte(BTN_PIN, b)) === HIGH);
      if (raw !== btnLast[b]) {
        btnLast[b]      = raw;
        btnChangedAt[b] = now;
      }
      else if (u32(now - btnChangedAt[b]) >= D.DEBOUNCE_MS && raw !== btnStable[b]) {
        btnStable[b] = raw;
        if (!raw && pressed === 255) pressed = b;
      }
    }
    return pressed;
  }

  function handleButton(b) {
    if (b === BTN_RESET_IDX) { resetAll(); return; }

    const f = (b === BTN_DER_IDX) ? FAULT_DER : u8(b + 1);

    if (f === faultSel && stepNow !== ST_NORMAL) {
      if (stepNow < ST_LAST) goToStep(stepNow + 1);
    } else {
      startFault(f);
    }
  }

  /* ======================================================================
   * SETUP AND LOOP
   * setup() is a generator so delay(ms) can hand time back to the board:
   * `yield ms` is delay(ms).
   * ==================================================================== */
  function* segmentTest() {
    let startIdx = 0;
    for (let s = 0; s < NUM_SEGMENTS; s++) {
      const len = pgm_read_byte(T.SEG_LEN, s);
      if (len === 0) continue;

      fill_solid(leds, NUM_LEDS, BLACK);
      for (let i = 0; i < len && u16(startIdx + i) < NUM_LEDS; i++)
        setLed(startIdx + i, hsv2rgb_rainbow(u8(Math.floor((s * 255) / NUM_SEGMENTS)), 255, 255));
      FastLED.show();

      Serial.print(F('segment '));  Serial.print(s + 1);
      Serial.print(F('  px '));     Serial.print(startIdx);
      Serial.print(F(' .. '));      Serial.print(startIdx + len - 1);
      Serial.print(F('  len '));    Serial.println(len);

      startIdx = u16(startIdx + len);
      yield D.SEGMENT_TEST_MS;
    }
  }

  function* setup() {
    Serial.begin(115200);
    yield 200;

    Serial.println(F('\n=== JEA Tabletop FLISR Trainer REV2 ==='));

    let sum = 0;
    for (let s = 0; s < NUM_SEGMENTS; s++) sum = u16(sum + pgm_read_byte(T.SEG_LEN, s));
    Serial.print(F('segment table total : ')); Serial.println(sum);
    Serial.print(F('NUM_LEDS            : ')); Serial.println(NUM_LEDS);
    if (sum !== NUM_LEDS) {
      Serial.println(F('[!] MISMATCH. Set NUM_LEDS to the segment table total above.'));
    } else {
      Serial.println(F('[OK] segment table matches NUM_LEDS'));
    }

    for (let d = 0; d < NUM_DEVICES; d++) {
      const s = pgm_read_byte(T.DEV_SEG, d);
      const i = pgm_read_byte(T.DEV_PX, d);
      if (s >= NUM_SEGMENTS || i >= pgm_read_byte(T.SEG_LEN, s) || !pgm_read_byte(T.SEG_OVER, s)) {
        Serial.print(F('[!] '));
        printDeviceName(d);
        Serial.println(F(': DEV_SEG / DEV_PX is not a pixel on a visible run. See block [2].'));
      }
    }

    initButtons();

    FastLED.addLeds(D.LED_TYPE, D.LED_DATA_PIN, D.COLOR_ORDER, leds, NUM_LEDS)
           .setCorrection('TypicalLEDStrip');
    FastLED.setBrightness(D.BRIGHTNESS);
    FastLED.setMaxPowerInVoltsAndMilliamps(5, D.MAX_MILLIAMPS);
    fill_solid(leds, NUM_LEDS, BLACK);
    FastLED.show();

    if (D.SEGMENT_TEST_MODE) {
      Serial.println(F('[!] SEGMENT_TEST_MODE is on. Set it to 0 for normal operation.'));
      yield* segmentTest();
    }

    resetAll();
  }

  let lastFrame = 0;                 /* static uint32_t lastFrame in loop() */
  function loop() {
    const b = pollButtons();
    if (b !== 255) handleButton(b);

    if (animActive && animFront() >= animLast) {
      animActive = false;
      stepStartedAt = millis();
    }

    if (D.AUTO_ADVANCE) {
      if (stepNow !== ST_NORMAL && stepNow < ST_LAST && !animActive &&
          u32(millis() - stepStartedAt) >= D.STEP_INTERVAL_MS) {
        goToStep(stepNow + 1);
      }
    }

    if (u32(millis() - lastFrame) >= D.FRAME_INTERVAL_MS) {
      lastFrame = millis();
      render();
    }
  }

  return { setup, loop };
}

/* ===========================================================================
 * The board: pins, clock, strip latch, serial line. Not part of the sketch.
 *
 * Time model: a virtual millisecond clock starting at 0 on power-up or reset.
 * setup() runs first, with delay(ms) advancing the clock. After that loop()
 * runs once per virtual millisecond. Button contacts are timestamped events
 * applied when the clock reaches them, so a press shorter than DEBOUNCE_MS
 * is ignored exactly as the debounce code would ignore it.
 * =========================================================================== */
function createBoard(cfg, io) {
  let now = 0;
  const mode  = new Uint8Array(256);
  const level = new Uint8Array(256);
  const contact = io.contacts || new Uint8Array(256); /* 1 = button closed to GND */
  const events = [];

  const hal = {
    millis: () => u32(now),
    pinMode(p, m) { mode[p] = m; if (m !== OUTPUT) level[p] = LOW; },
    digitalWrite(p, v) { level[p] = v ? HIGH : LOW; },
    digitalRead(p) {
      if (contact[p]) return LOW;
      return mode[p] === INPUT_PULLUP ? HIGH : LOW;
    },
    pgm_read_byte: (arr, i) => arr[i],
    Serial: makeSerial(io.onSerial || (() => {})),
    FastLED: makeFastLED(io.onShow || (() => {}))
  };

  const fw = createFirmware(cfg, hal);
  const setupIt = fw.setup();
  let inSetup = true, delayUntil = 0;

  function applyEvents() {
    while (events.length && events[0].t <= now) {
      const e = events.shift();
      contact[e.pin] = e.closed ? 1 : 0;
    }
  }

  return {
    get now() { return now; },
    get inSetup() { return inSetup; },
    contacts: contact,
    /* Close or open a button contact at virtual time t (defaults to now). */
    setContact(pin, closed, t) {
      events.push({ pin, closed, t: Math.max(t === undefined ? now : t, now) });
    },
    pinMode: p => mode[p],
    pinLevel: p => (mode[p] === OUTPUT ? level[p] : hal.digitalRead(p)),
    /* Run the MCU until the virtual clock reaches t. */
    runUntil(t) {
      while (now < t) {
        applyEvents();
        if (inSetup) {
          if (now < delayUntil) { now = Math.min(delayUntil, t); continue; }
          const r = setupIt.next();
          if (r.done) inSetup = false; else delayUntil = now + r.value;
          continue;
        }
        fw.loop();
        now += 1;
      }
      applyEvents();
    }
  };
}

const api = { PORTED_LOGIC_SHA256, createBoard, createFirmware, makeFastLED, hsv2rgb_rainbow,
              LOW, HIGH, INPUT, OUTPUT, INPUT_PULLUP };
if (typeof module !== 'undefined' && module.exports) module.exports = api;
else root.FLISR = api;

})(typeof window !== 'undefined' ? window : globalThis);
