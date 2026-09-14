/* ===========================================================================
 * JEA / Union University Senior Design
 * Tabletop FLISR Trainer REV1 - Fault Location, Isolation and Service Restoration
 * ---------------------------------------------------------------------------
 * Target      : Arduino Uno / Nano (ATmega328P)
 * Strip       : WS2812B, 60 LED/m, ONE continuous data chain of 337 pixels
 * Library     : FastLED (Sketch > Include Library > Manage Libraries > FastLED)
 *
 * Ground truth for this file:
 *   Cardboard Layout REV1 backup_9.12.20.dxf    (geometry, full scale, inches)
 *   JEA Cardboard Prototype Tabulated REV1.xlsx (Element/Node/Line/Fault/LED)
 *   FLISR Trainer Plan Set artifact             (restoration logic)
 * Board origin (0,0) is the bottom-left corner of the model.
 *
 * ---------------------------------------------------------------------------
 * WHAT THIS DOES
 *   Press a fault button. The sketch runs the five-step FLISR sequence:
 *     00 NORMAL -> 01 FAULT -> 02 LOCKOUT -> 03 ISOLATE -> 04 RESTORE
 *   Line sections light by their source: blue = Substation A, green =
 *   Substation B, red = faulted or lost power, dark = de-energized.
 *
 * REV1 ANIMATIONS
 *   01 FAULT   Red starts at the fault point (the Fault sheet location) and
 *              spreads along the line one pixel every ANIM_STEP_MS, through
 *              every zone that lost power, out to the open tie. When it has
 *              covered them the faulted section blinks and the rest holds
 *              solid red.
 *   03 ISOLATE The zones that only lost power go dark. The faulted section
 *              holds solid red.
 *   04 RESTORE When the tie closes, the new source color fills the restored
 *              zones outward from the tie, one pixel every ANIM_STEP_MS.
 *
 * OPERATION
 *   Press a fault button           -> starts that fault at step 01
 *   Press the SAME button again    -> advances one step immediately
 *   Press a DIFFERENT fault button -> abandons it and starts the new fault
 *   Press RESET                    -> returns to step 00 NORMAL
 *   With AUTO_ADVANCE 1 the steps also advance on their own. The timer waits
 *   for an animation to finish, then counts STEP_INTERVAL_MS from there.
 *   Set AUTO_ADVANCE to 0 for pure manual stepping.
 *
 * PIN BUDGET (Uno/Nano, 18 usable I/O with D0/D1 left for USB serial)
 *   8 buttons + 1 strip data + 8 device LEDs = 17 used, A5 spare.
 * =========================================================================== */

#include <FastLED.h>

/* ===========================================================================
 * [1] FAULT BUTTON PINS                                  <<< EDIT HERE
 * ---------------------------------------------------------------------------
 * Wire each button between its pin and GND. Internal pull-ups are enabled,
 * so a pressed button reads LOW. No external resistors needed.
 *
 * Button placements from the DXF (Sketch5 circles, r = 0.50 in):
 *   FAULT Z1  (10.09, 15.85)      FAULT Z5  (35.60, 23.50)
 *   FAULT Z2  (11.11, 21.09)      FAULT Z6  (36.60, 32.57)
 *   FAULT Z3  (20.11, 31.27)      FAULT DER (32.26, 19.07)
 *   FAULT Z4  (28.40, 27.26)      RESET     (26.46,  5.13)
 * =========================================================================== */
#define PIN_BTN_FAULT_Z1    2
#define PIN_BTN_FAULT_Z2    3
#define PIN_BTN_FAULT_Z3    4
#define PIN_BTN_FAULT_Z4    5
#define PIN_BTN_FAULT_Z5    6
#define PIN_BTN_FAULT_Z6    7
#define PIN_BTN_FAULT_DER   8
#define PIN_BTN_RESET       9

/* ===========================================================================
 * [2] DEVICE STATUS LED PINS                             <<< EDIT HERE
 * ---------------------------------------------------------------------------
 * DEVICE_LED_MODE 1 : one pin per device (fits Uno/Nano)
 *      solid ON   = CLOSED        fast blink = LOCKOUT
 *      OFF        = OPEN          slow blink = TRIPPED
 * DEVICE_LED_MODE 2 : two pins per device, green + red (needs a Mega 2560)
 *      green ON = CLOSED, red ON = OPEN, red fast blink = LOCKOUT,
 *      red slow blink = TRIPPED
 *
 * Device positions from the Element sheet / DXF blocks:
 *   E1 SUB_A_BKR (12.59,  9.12)   E5 DEV_B2    (30.08, 25.50)
 *   E2 DEV_A1    (12.59, 17.58)   E7 DEV_B1    (38.10, 21.91)
 *   E3 DEV_A2    (12.59, 29.38)   E6 SUB_B_BKR (38.10, 37.44)
 *   E4 TIE       (26.55, 25.50)   R1 DER_PCC   (34.15, 20.65)
 * =========================================================================== */
#define DEVICE_LED_MODE     1

#if DEVICE_LED_MODE == 1
  #define PIN_DEV_SUB_A_BKR  11
  #define PIN_DEV_DEV_A1     12
  #define PIN_DEV_DEV_A2     13     /* also drives the onboard LED, harmless */
  #define PIN_DEV_TIE        A0
  #define PIN_DEV_DEV_B2     A1
  #define PIN_DEV_DEV_B1     A2
  #define PIN_DEV_SUB_B_BKR  A3
  #define PIN_DEV_DER_PCC    A4
#else
  /* Green pins */
  #define PIN_DEVG_SUB_A_BKR 22
  #define PIN_DEVG_DEV_A1    24
  #define PIN_DEVG_DEV_A2    26
  #define PIN_DEVG_TIE       28
  #define PIN_DEVG_DEV_B2    30
  #define PIN_DEVG_DEV_B1    32
  #define PIN_DEVG_SUB_B_BKR 34
  #define PIN_DEVG_DER_PCC   36
  /* Red pins */
  #define PIN_DEVR_SUB_A_BKR 23
  #define PIN_DEVR_DEV_A1    25
  #define PIN_DEVR_DEV_A2    27
  #define PIN_DEVR_TIE       29
  #define PIN_DEVR_DEV_B2    31
  #define PIN_DEVR_DEV_B1    33
  #define PIN_DEVR_SUB_B_BKR 35
  #define PIN_DEVR_DER_PCC   37
#endif

/* ===========================================================================
 * [3] STRIP CONFIGURATION                                <<< EDIT HERE
 * ---------------------------------------------------------------------------
 * NUM_LEDS must equal the sum of SEG_LEN[] in block [4]. setup() checks this
 * for you and prints the correct number on the serial monitor if it is wrong.
 * =========================================================================== */
#define LED_DATA_PIN       10
#define NUM_LEDS          337
#define LED_TYPE        WS2812B
#define COLOR_ORDER         GRB
#define BRIGHTNESS           80   /* 0-255 */
#define MAX_MILLIAMPS      4000   /* FastLED soft power cap at 5 V */

/* Section colors. Tuned for LEDs, not for paper. */
#define COLOR_SRC_A     CRGB(0x1E, 0x6B, 0xFF)   /* fed from Substation A */
#define COLOR_SRC_B     CRGB(0x00, 0xD0, 0x50)   /* fed from Substation B */
#define COLOR_FAULT     CRGB(0xFF, 0x18, 0x10)   /* faulted section       */
#define COLOR_DEAD      CRGB(0x00, 0x00, 0x00)   /* de-energized, dark    */

/* ===========================================================================
 * [4] LED SEGMENT TABLE                                  <<< EDIT HERE
 * ---------------------------------------------------------------------------
 * One row per run of strip, in the order the data line travels. Taken from
 * the LED sheet. If you miscounted a run, change its number in SEG_LEN and
 * update NUM_LEDS above. Nothing else needs to move.
 *
 * OVER = 1 runs on the visible surface. OVER = 0 passes UNDER the display to
 * get back to a branch point, so those pixels are always held dark. That is
 * what makes the branching look seamless.
 *
 * ZONE is the protection zone the run belongs to. Three runs cross a device
 * partway along, so they carry a SPLIT: the first SPLIT pixels belong to
 * ZONE, the rest belong to ZONE2. SPLIT = 0 means the whole run is ZONE.
 *
 * Array index: runs 1 - 24 are index 0 - 23, J1 is index 24, runs 25 - 30
 * are index 25 - 30. The REV1 tables in [4b] and [4c] use the array index.
 *
 *  #   len over from  to    zone       note
 *  1    17   1   N1    N2   BUSA -> Z1 see note on run 1 below, splits at 8 px
 *  2    17   1   N2    N3   Z1         RES-1 south street
 *  3    17   0   N3    N2   hidden     return under the board
 *  4    10   1   N2    N4   Z1 -> Z2   CROSSES DEV_A1 at 2 px
 *  5    17   1   N4    N5   Z2         RES-1 north street
 *  6    17   0   N5    N4   hidden     return under the board
 *  7     2   1   N4   N32   Z2         trunk up to the y = 24 seam
 *  8     9   1  N32   N30   Z2         seam up to the DEV_A2 corner
 *  9     6   1  N30    N6   Z3         DEV_A2 corner out to the RES-2 tap
 * 10     8   1   N6    N7   Z3         RES-2 lateral north
 * 11    11   1   N7    N8   Z3         RES-2 west
 * 12    14   1   N8    N9   Z3         RES-2 north
 * 13    28   1   N9   N10   Z3         RES-2 top street
 * 14    26   0  N10    N6   hidden     return under the board
 * 15    12   1   N6   N33   Z3         trunk east to the x = 24 seam
 * 16     4   1  N33   N11   Z3         seam east to the corner
 * 17     6   1  N11   N12   Z3         corner south to the TIE
 * 18     6   1  N12   N13   Z4         TIE east toward DEV_B2
 * 19     9   1  N13   N14   Z4         COMMERCIAL lateral, taps ahead of DEV_B2
 * 20    10   0  N14   N13   hidden     return under the board
 * 21     3   1  N13   N35   Z4 -> Z5   THE DIAGONAL, crosses DEV_B2 at 1 px
 * 22    22   0  N35   N29   hidden     under the board to Substation B
 * 23    12   1  N29   N27   Z6         SUB_B_BKR south to the industrial tap
 * 24     4   1  N27   N28   Z6         INDUSTRIAL lateral
 * J1     0   0  N28   N27   hidden     JUMPER, plain wire N28 -> N27, 0 pixels
 * 25     7   1  N27   N34   Z6         tap south to the y = 24 seam
 * 26     4   1  N34   N26   Z6         seam south to DEV_B1
 * 27    12   1  N26   N16   Z5         DEV_B1 west toward DEV_B2
 * 28     3   1  N16   N35   Z5         north to the seam
 * 29    11   0  N35   N17   hidden     under the board to the DER tap
 * 30    13   1  N17   N24   Z5 -> DER  CROSSES DER_PCC at 2 px
 *
 * NOTE on run 1. The strip does not begin at N1. It begins 8 px SOUTH of N1,
 * inside Substation A, runs north through N1 and carries on 9 px to N2, which
 * is why the run is 17 px when N1 -> N2 alone measures only 6.08 in = 9.3 px.
 * N1 is the SUB_A_BKR location, so those first 8 px sit on the SOURCE side of
 * the breaker. They are the substation bus and they stay energized no matter
 * what the breaker does. They are given the zone BUSA, which is always lit in
 * the Substation A color and never goes dark, not even on a Z1 lockout. That
 * is the point: the bus stays hot, the breaker is what opens.
 *
 * NOTE on N30. N30 is the DEV_A2 corner at about (12.59, 29.51), confirmed.
 * Run 8 measures 5.51 in = 8.4 px against the 9 counted and run 9 measures
 * 3.54 in = 5.4 px against the 6 counted. DEV_A2 sits on that corner, which
 * is why the zone flips cleanly between run 8 (Z2) and run 9 (Z3) with no
 * split needed. The Node sheet may still carry the old (21.58, 29.50).
 * =========================================================================== */
#define NUM_SEGMENTS  31

/* Zone codes used by the table below. */
#define ZN_HID   0   /* runs under the display, always dark            */
#define ZN_BUSA  8   /* Substation A bus, source side of SUB_A_BKR,
                        always lit in the Source A color, never dark    */
#define ZN_Z1    1
#define ZN_Z2    2
#define ZN_Z3    3
#define ZN_Z4    4
#define ZN_Z5    5
#define ZN_Z6    6
#define ZN_DER   7

const uint8_t SEG_LEN[NUM_SEGMENTS] PROGMEM = {
   17, 17, 17, 10, 17, 17,  2,  9,  6,  8,   /*  1 - 10          */
   11, 14, 28, 26, 12,  4,  6,  6,  9, 10,   /* 11 - 20          */
    3, 22, 12,  4,  0,  7,  4, 12,  3, 11,   /* 21 - 24, J1, 25 - 29 */
   13                                        /* 30               */
};

const uint8_t SEG_OVER[NUM_SEGMENTS] PROGMEM = {
    1,  1,  0,  1,  1,  0,  1,  1,  1,  1,
    1,  1,  1,  0,  1,  1,  1,  1,  1,  0,
    1,  0,  1,  1,  0,  1,  1,  1,  1,  0,
    1
};

const uint8_t SEG_ZONE[NUM_SEGMENTS] PROGMEM = {
   ZN_BUSA, ZN_Z1, ZN_HID, ZN_Z1, ZN_Z2, ZN_HID, ZN_Z2, ZN_Z2, ZN_Z3, ZN_Z3,
   ZN_Z3, ZN_Z3, ZN_Z3,  ZN_HID, ZN_Z3, ZN_Z3,  ZN_Z3, ZN_Z4, ZN_Z4, ZN_HID,
   ZN_Z4, ZN_HID, ZN_Z6, ZN_Z6,  ZN_HID, ZN_Z6, ZN_Z6, ZN_Z5, ZN_Z5, ZN_HID,
   ZN_Z5
};

/* Pixels at the head of the run that stay in SEG_ZONE. 0 = the whole run. */
const uint8_t SEG_SPLIT[NUM_SEGMENTS] PROGMEM = {
    8,  0,  0,  2,  0,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    1,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    2
};

/* Zone of the tail of a split run. Ignored when SEG_SPLIT is 0. */
const uint8_t SEG_ZONE2[NUM_SEGMENTS] PROGMEM = {
   ZN_Z1,  ZN_HID, ZN_HID, ZN_Z2,  ZN_HID, ZN_HID, ZN_HID, ZN_HID, ZN_HID, ZN_HID,
   ZN_HID, ZN_HID, ZN_HID, ZN_HID, ZN_HID, ZN_HID, ZN_HID, ZN_HID, ZN_HID, ZN_HID,
   ZN_Z5,  ZN_HID, ZN_HID, ZN_HID, ZN_HID, ZN_HID, ZN_HID, ZN_HID, ZN_HID, ZN_HID,
   ZN_DER
};

/* ===========================================================================
 * [4b] HOW THE RUNS JOIN (REV1)                          <<< EDIT HERE
 * ---------------------------------------------------------------------------
 * The fault wave and the restore fill travel along the line, so the sketch
 * needs to know where runs meet. SEG_FROM and SEG_TO are the From and To
 * node numbers from the table above (N12 -> 12). Hidden runs are listed to
 * keep the rows lined up; the animations never travel along them.
 *
 * A tap is a node partway along a run instead of at one end. N17, where the
 * DER branch leaves the Z5 line, sits 6.78 px into run 27 (index 27), which
 * is between its pixels 6 and 7, so TAP_PX is 7.
 *
 * The restore fill starts at TIE_NODE, the node the TIE sits on.
 * =========================================================================== */
#define NUM_NODES     36   /* N0 - N35, N0 unused */

const uint8_t SEG_FROM[NUM_SEGMENTS] PROGMEM = {
    1,  2,  3,  2,  4,  5,  4, 32, 30,  6,   /*  1 - 10          */
    7,  8,  9, 10,  6, 33, 11, 12, 13, 14,   /* 11 - 20          */
   13, 35, 29, 27, 28, 27, 34, 26, 16, 35,   /* 21 - 24, J1, 25 - 29 */
   17                                        /* 30               */
};

const uint8_t SEG_TO[NUM_SEGMENTS] PROGMEM = {
    2,  3,  2,  4,  5,  4, 32, 30,  6,  7,
    8,  9, 10,  6, 33, 11, 12, 13, 14, 13,
   35, 29, 27, 28, 27, 34, 26, 16, 35, 17,
   24
};

#define NUM_TAPS      1
const uint8_t TAP_SEG[NUM_TAPS]  PROGMEM = { 27 };
const uint8_t TAP_PX[NUM_TAPS]   PROGMEM = {  7 };
const uint8_t TAP_NODE[NUM_TAPS] PROGMEM = { 17 };

#define TIE_NODE      12   /* N12, E4 TIE */

/* ===========================================================================
 * [4c] FAULT LOCATIONS (REV1)                            <<< EDIT HERE
 * ---------------------------------------------------------------------------
 * Where each fault wave starts: the array index of the run it sits on and
 * the pixel along that run (0 = the run's first pixel). Taken from the Fault
 * sheet by finding the pixel nearest each fault point.
 *
 *   fault   Fault sheet       run  index  pixel
 *   Z1     (12.59, 15.84)      1      0     16
 *   Z2     (12.59, 21.05)      4      3      7
 *   Z3     (20.10, 29.50)     15     14      6
 *   Z4     (28.40, 25.50)     18     17      3
 *   Z5     (35.60, 21.90)     27     27      4
 *   Z6     (38.13, 32.55)     23     22      6
 *   DER    (34.10, 19.10)     30     30      4
 * =========================================================================== */
#define NUM_FAULTS    7    /* Z1 - Z6, then DER */

const uint8_t FAULT_SEG[NUM_FAULTS] PROGMEM = {  0,  3, 14, 17, 27, 22, 30 };
const uint8_t FAULT_PX[NUM_FAULTS]  PROGMEM = { 16,  7,  6,  3,  4,  6,  4 };

/* ===========================================================================
 * [5] TIMING AND BEHAVIOR                                <<< EDIT HERE
 * =========================================================================== */
#define AUTO_ADVANCE           1     /* 1 = step on a timer, 0 = manual only  */
#define STEP_INTERVAL_MS    2500UL   /* time between automatic steps          */
#define DEBOUNCE_MS           40UL
#define FAULT_BLINK_MS       350UL   /* faulted section blink, steps 01 - 02  */
#define DEV_TRIP_BLINK_MS    500UL   /* device TRIPPED slow blink             */
#define DEV_LOCK_BLINK_MS    150UL   /* device LOCKOUT fast blink             */
#define FRAME_INTERVAL_MS     20UL   /* strip refresh, 50 fps. See note below.*/
#define ANIM_STEP_MS          30UL   /* fault wave and restore fill, per pixel */

/* Why the strip is not refreshed every pass of loop(): on an AVR the WS2812
 * driver has to disable interrupts while it clocks the data out, about 10 ms
 * for 337 pixels. Refreshing flat out would leave the processor with
 * interrupts off roughly half the time. 50 fps is far smoother than the eye
 * needs and keeps button polling responsive.                                */

/* Light every run in a different color at boot so you can verify your counts.
 * Set to 1, upload, and walk the board comparing to the table in block [4].  */
#define SEGMENT_TEST_MODE      0
#define SEGMENT_TEST_MS     1200UL

/* ===========================================================================
 *                    NOTHING BELOW HERE NEEDS EDITING
 * =========================================================================== */

/* ---- device chain ------------------------------------------------------ */
/* Index order is the electrical order from Substation A to Substation B.
 * Zone Zk lies between device k-1 and device k.                            */
#define DEV_SUB_A_BKR  0
#define DEV_A1         1
#define DEV_A2         2
#define DEV_TIE        3
#define DEV_B2         4
#define DEV_B1         5
#define DEV_SUB_B_BKR  6
#define DEV_DER_PCC    7
#define NUM_DEVICES    8

/* ---- states ------------------------------------------------------------ */
enum ZState : uint8_t { ZS_A, ZS_B, ZS_DEAD, ZS_FAULT };
enum DState : uint8_t { DS_CLOSED, DS_OPEN, DS_TRIPPED, DS_LOCKOUT };

/* ---- steps ------------------------------------------------------------- */
#define ST_NORMAL   0
#define ST_FAULT    1
#define ST_LOCKOUT  2
#define ST_ISOLATE  3
#define ST_RESTORE  4
#define ST_LAST     4

/* ---- fault selection --------------------------------------------------- */
#define FAULT_NONE  0    /* 1..6 select Z1..Z6 */
#define FAULT_DER   7

/* ---- buttons ----------------------------------------------------------- */
#define NUM_BUTTONS   8
#define BTN_DER_IDX   6
#define BTN_RESET_IDX 7

/* ---- animations (REV1) ------------------------------------------------- */
#define ANIM_NONE     0
#define ANIM_FAULT    1    /* red wave out from the fault point, 01 - 02   */
#define ANIM_RESTORE  2    /* new source color out from the tie, 04        */
#define NUM_POINTS    (NUM_NODES + NUM_SEGMENTS)  /* nodes, then one split
                                                     point per run          */
#define DIST_NONE     255  /* not reachable                                 */
#define SRC_IS_TIE    255  /* animSrcSeg value when the source is TIE_NODE  */

const uint8_t BTN_PIN[NUM_BUTTONS] PROGMEM = {
  PIN_BTN_FAULT_Z1, PIN_BTN_FAULT_Z2, PIN_BTN_FAULT_Z3, PIN_BTN_FAULT_Z4,
  PIN_BTN_FAULT_Z5, PIN_BTN_FAULT_Z6, PIN_BTN_FAULT_DER, PIN_BTN_RESET
};

#if DEVICE_LED_MODE == 1
const uint8_t DEV_PIN[NUM_DEVICES] PROGMEM = {
  PIN_DEV_SUB_A_BKR, PIN_DEV_DEV_A1, PIN_DEV_DEV_A2, PIN_DEV_TIE,
  PIN_DEV_DEV_B2, PIN_DEV_DEV_B1, PIN_DEV_SUB_B_BKR, PIN_DEV_DER_PCC
};
#else
const uint8_t DEV_PIN_G[NUM_DEVICES] PROGMEM = {
  PIN_DEVG_SUB_A_BKR, PIN_DEVG_DEV_A1, PIN_DEVG_DEV_A2, PIN_DEVG_TIE,
  PIN_DEVG_DEV_B2, PIN_DEVG_DEV_B1, PIN_DEVG_SUB_B_BKR, PIN_DEVG_DER_PCC
};
const uint8_t DEV_PIN_R[NUM_DEVICES] PROGMEM = {
  PIN_DEVR_SUB_A_BKR, PIN_DEVR_DEV_A1, PIN_DEVR_DEV_A2, PIN_DEVR_TIE,
  PIN_DEVR_DEV_B2, PIN_DEVR_DEV_B1, PIN_DEVR_SUB_B_BKR, PIN_DEVR_DER_PCC
};
#endif

/* ---- runtime state ----------------------------------------------------- */
CRGB    leds[NUM_LEDS];

uint8_t faultSel  = FAULT_NONE;
uint8_t stepNow   = ST_NORMAL;

ZState  zoneState[7];          /* index 1..6 used, 0 unused */
DState  devState[NUM_DEVICES];
bool    derFaulted = false;

uint32_t stepStartedAt = 0;
bool     btnStable[NUM_BUTTONS];
bool     btnLast[NUM_BUTTONS];
uint32_t btnChangedAt[NUM_BUTTONS];

/* REV1 animation state */
uint8_t  animKind      = ANIM_NONE;
bool     animActive    = false;    /* true until it reaches its last pixel  */
uint32_t animStartedAt = 0;
uint8_t  animLast      = 0;        /* distance of the farthest pixel        */
uint16_t animZones     = 0;        /* one bit per zone code it covers       */
uint16_t faultZones    = 0;        /* one bit per zone code that is faulted */
uint8_t  animSrcSeg    = SRC_IS_TIE;
uint8_t  animSrcPx     = 0;
uint8_t  pointDist[NUM_POINTS];    /* pixel steps from the source           */

/* ===========================================================================
 * FLISR MODEL
 * ---------------------------------------------------------------------------
 * Mirrors the logic in the FLISR Trainer Plan Set artifact exactly.
 *
 *   aSide  : the fault is on the Substation A half of the chain (Z1..Z3)
 *   trip   : the source-side boundary device, the one that sees fault current
 *   far    : the far-side boundary device, which sees none. That disagreement
 *            is what locates the fault to the section between them.
 *   strand : every zone from the fault out to the open tie, all of which lose
 *            their source the moment the source-side device opens.
 * =========================================================================== */
void computeModel()
{
  /* normal: closed everywhere but the tie, A feeds Z1-Z3, B feeds Z4-Z6 */
  for (uint8_t k = 1; k <= 6; k++) zoneState[k] = (k <= 3) ? ZS_A : ZS_B;
  for (uint8_t d = 0; d < NUM_DEVICES; d++) devState[d] = DS_CLOSED;
  devState[DEV_TIE] = DS_OPEN;
  derFaulted = false;

  if (stepNow == ST_NORMAL || faultSel == FAULT_NONE) return;

  /* --- DER branch fault -------------------------------------------------
   * Properly coordinated. The point of common coupling recloser owns this
   * branch, clears the fault by itself and locks out. The feeder never sees
   * it, so Z5 and everything else stay energized. There is nothing further
   * to isolate and nothing stranded to restore.                            */
  if (faultSel == FAULT_DER) {
    derFaulted = true;
    devState[DEV_DER_PCC] = (stepNow >= ST_LOCKOUT) ? DS_LOCKOUT : DS_TRIPPED;
    return;
  }

  /* --- zone fault, Z1..Z6 ----------------------------------------------- */
  const uint8_t f     = faultSel;
  const bool    aSide = (f <= 3);
  const uint8_t trip  = aSide ? (uint8_t)(f - 1) : f;
  const uint8_t farSide = aSide ? f : (uint8_t)(f - 1);

  if (aSide) { for (uint8_t k = f; k <= 3; k++) zoneState[k] = ZS_DEAD; }
  else       { for (uint8_t k = 4; k <= f; k++) zoneState[k] = ZS_DEAD; }
  zoneState[f] = ZS_FAULT;

  /* 01 the device trips, 02 reclose fails and it goes to lockout */
  devState[trip] = (stepNow >= ST_LOCKOUT) ? DS_LOCKOUT : DS_TRIPPED;

  /* 03 isolate: the far side opens a de-energized line, no interrupting duty */
  if (stepNow >= ST_ISOLATE) devState[farSide] = DS_OPEN;

  /* 04 restore: close the tie only if healthy load is stranded past the fault */
  if (stepNow >= ST_RESTORE) {
    const uint8_t lo = aSide ? (uint8_t)(f + 1) : 4;
    const uint8_t hi = aSide ? 3 : (uint8_t)(f - 1);
    if (lo <= hi) {
      devState[DEV_TIE] = DS_CLOSED;
      for (uint8_t k = lo; k <= hi; k++) zoneState[k] = aSide ? ZS_B : ZS_A;
    }
    /* If nothing is stranded the tie stays open. Closing it would energize
     * the fault from the other substation. That is the correct answer.     */
  }

  /* IEEE 1547 anti-islanding: the DER must never backfeed a dead or faulted
   * line that someone is about to touch.                                   */
  if (zoneState[5] == ZS_DEAD || zoneState[5] == ZS_FAULT)
    devState[DEV_DER_PCC] = DS_TRIPPED;
}

/* The DER branch is live only when Z5 is live and the PCC is closed. */
ZState derDisplayState()
{
  if (derFaulted)                          return ZS_FAULT;
  if (devState[DEV_DER_PCC] != DS_CLOSED)  return ZS_DEAD;
  return zoneState[5];
}

/* ===========================================================================
 * LINE WALKING (REV1)
 * ---------------------------------------------------------------------------
 * Each run is cut into pieces at its split (a device partway along) and at
 * any tap. A piece is a straight stretch of pixels lo..hi with a point at
 * each end: a node, the run's split point, or a tap node. Point numbers are
 * the node number for nodes and taps, and NUM_NODES + run index for splits.
 *
 * Distances count pixels. A point's distance is that of the last pixel
 * before it, so the first pixel past a point is one more. The source pixel
 * is 0. The line is radial, so relaxing the pieces settles in a few passes.
 * =========================================================================== */
struct Piece { uint8_t lo, hi, a, b; };

/* Piece k of run s, counted from the run's first pixel. False when none. */
bool getPiece(uint8_t s, uint8_t k, Piece &p)
{
  const uint8_t len = pgm_read_byte(&SEG_LEN[s]);
  if (len == 0) return false;

  uint8_t cutPx[2], cutPt[2], n = 0;
  const uint8_t split = pgm_read_byte(&SEG_SPLIT[s]);
  if (split) { cutPx[n] = split; cutPt[n] = NUM_NODES + s; n++; }
  for (uint8_t t = 0; t < NUM_TAPS && n < 2; t++) {
    if (pgm_read_byte(&TAP_SEG[t]) != s) continue;
    cutPx[n] = pgm_read_byte(&TAP_PX[t]);
    cutPt[n] = pgm_read_byte(&TAP_NODE[t]);
    n++;
  }
  if (n == 2 && cutPx[1] < cutPx[0]) {
    uint8_t x = cutPx[0]; cutPx[0] = cutPx[1]; cutPx[1] = x;
    x = cutPt[0]; cutPt[0] = cutPt[1]; cutPt[1] = x;
  }
  if (k > n) return false;

  p.lo = (k == 0) ? 0 : cutPx[k - 1];
  p.hi = (k == n) ? (uint8_t)(len - 1) : (uint8_t)(cutPx[k] - 1);
  p.a  = (k == 0) ? pgm_read_byte(&SEG_FROM[s]) : cutPt[k - 1];
  p.b  = (k == n) ? pgm_read_byte(&SEG_TO[s])   : cutPt[k];
  return true;
}

uint8_t zoneOfPixel(uint8_t s, uint8_t i)
{
  if (!pgm_read_byte(&SEG_OVER[s])) return ZN_HID;
  const uint8_t split = pgm_read_byte(&SEG_SPLIT[s]);
  return (split && i >= split) ? pgm_read_byte(&SEG_ZONE2[s])
                               : pgm_read_byte(&SEG_ZONE[s]);
}

uint8_t addSteps(uint8_t d, uint8_t n)
{
  const uint16_t v = (uint16_t)d + n;
  return (v >= DIST_NONE) ? (uint8_t)(DIST_NONE - 1) : (uint8_t)v;
}

/* Distance of pixel i, which lies on piece p of run s. */
uint8_t distInPiece(uint8_t s, uint8_t i, const Piece &p)
{
  if (s == animSrcSeg && animSrcPx >= p.lo && animSrcPx <= p.hi)
    return (i > animSrcPx) ? (uint8_t)(i - animSrcPx) : (uint8_t)(animSrcPx - i);

  uint8_t d = DIST_NONE;
  if (pointDist[p.a] != DIST_NONE) d = addSteps(pointDist[p.a], i - p.lo + 1);
  if (pointDist[p.b] != DIST_NONE) {
    const uint8_t e = addSteps(pointDist[p.b], p.hi - i + 1);
    if (e < d) d = e;
  }
  return d;
}

/* Fill pointDist[] from the source, through pieces in animZones only. */
void computeDistances()
{
  for (uint8_t q = 0; q < NUM_POINTS; q++) pointDist[q] = DIST_NONE;

  Piece p;
  if (animSrcSeg == SRC_IS_TIE) {
    pointDist[TIE_NODE] = 0;
  } else {
    for (uint8_t k = 0; getPiece(animSrcSeg, k, p); k++) {
      if (animSrcPx < p.lo || animSrcPx > p.hi) continue;
      pointDist[p.a] = animSrcPx - p.lo;
      pointDist[p.b] = p.hi - animSrcPx;
    }
  }

  bool changed = true;
  for (uint8_t pass = 0; changed && pass < NUM_POINTS; pass++) {
    changed = false;
    for (uint8_t s = 0; s < NUM_SEGMENTS; s++) {
      if (!pgm_read_byte(&SEG_OVER[s])) continue;
      for (uint8_t k = 0; getPiece(s, k, p); k++) {
        if (!(animZones & (1u << zoneOfPixel(s, p.lo)))) continue;
        const uint8_t n = p.hi - p.lo + 1;
        if (pointDist[p.a] != DIST_NONE && addSteps(pointDist[p.a], n) < pointDist[p.b]) {
          pointDist[p.b] = addSteps(pointDist[p.a], n); changed = true;
        }
        if (pointDist[p.b] != DIST_NONE && addSteps(pointDist[p.b], n) < pointDist[p.a]) {
          pointDist[p.a] = addSteps(pointDist[p.b], n); changed = true;
        }
      }
    }
  }
}

/* Pixels the animation has reached so far. */
uint16_t animFront()
{
  const uint32_t steps = (millis() - animStartedAt) / ANIM_STEP_MS;
  return (steps > 0xFFFF) ? 0xFFFF : (uint16_t)steps;
}

/* Called by goToStep() after computeModel(). */
void startAnimation()
{
  if (stepNow == ST_LOCKOUT) return;       /* the fault wave carries on */

  animKind   = ANIM_NONE;
  animActive = false;
  animZones  = 0;
  faultZones = 0;

  if (stepNow == ST_FAULT) {
    /* everything that lost power, which includes the faulted section */
    for (uint8_t k = 1; k <= 6; k++) {
      if (zoneState[k] == ZS_DEAD || zoneState[k] == ZS_FAULT) animZones |= (1u << k);
      if (zoneState[k] == ZS_FAULT) faultZones |= (1u << k);
    }
    const ZState der = derDisplayState();
    if (der == ZS_DEAD || der == ZS_FAULT) animZones |= (1u << ZN_DER);
    if (der == ZS_FAULT) faultZones |= (1u << ZN_DER);

    animSrcSeg = pgm_read_byte(&FAULT_SEG[faultSel - 1]);
    animSrcPx  = pgm_read_byte(&FAULT_PX[faultSel - 1]);
    animKind   = ANIM_FAULT;
  }
  else if (stepNow == ST_RESTORE && devState[DEV_TIE] == DS_CLOSED) {
    /* the zones now fed across the tie */
    for (uint8_t k = 1; k <= 6; k++) {
      if ((k <= 3 && zoneState[k] == ZS_B) || (k >= 4 && zoneState[k] == ZS_A))
        animZones |= (1u << k);
    }
    if ((animZones & (1u << 5)) && derDisplayState() == ZS_A) animZones |= (1u << ZN_DER);

    animSrcSeg = SRC_IS_TIE;
    animKind   = ANIM_RESTORE;
  }
  if (animKind == ANIM_NONE) return;

  computeDistances();

  animLast = 0;
  Piece p;
  for (uint8_t s = 0; s < NUM_SEGMENTS; s++) {
    if (!pgm_read_byte(&SEG_OVER[s])) continue;
    for (uint8_t k = 0; getPiece(s, k, p); k++) {
      if (!(animZones & (1u << zoneOfPixel(s, p.lo)))) continue;
      for (uint8_t i = p.lo; i <= p.hi; i++) {
        const uint8_t d = distInPiece(s, i, p);
        if (d != DIST_NONE && d > animLast) animLast = d;
      }
    }
  }

  animStartedAt = millis();
  animActive = true;
}

/* ===========================================================================
 * RENDER
 * =========================================================================== */
CRGB colorForState(ZState s, bool blinkOn)
{
  switch (s) {
    case ZS_A:     return COLOR_SRC_A;
    case ZS_B:     return COLOR_SRC_B;
    case ZS_FAULT: return blinkOn ? COLOR_FAULT : COLOR_DEAD;
    default:       return COLOR_DEAD;
  }
}

CRGB colorForZone(uint8_t zn, bool blinkOn)
{
  /* These three return before the zoneState[] lookup on purpose. ZN_DER and
   * ZN_BUSA are 7 and 8, and zoneState[] only holds indices 0..6.           */
  if (zn == ZN_HID)  return COLOR_DEAD;             /* under the board       */
  if (zn == ZN_BUSA) return COLOR_SRC_A;            /* bus, always energized */
  if (zn == ZN_DER)  return colorForState(derDisplayState(), blinkOn);
  return colorForState(zoneState[zn], blinkOn);     /* zn is 1..6 here       */
}

/* REV1: the animations sit on top of colorForZone(). */
CRGB colorForPixel(uint8_t zn, uint8_t s, uint8_t i, const Piece &p,
                   uint16_t front, bool blinkOn)
{
  if (zn == ZN_HID || zn == ZN_BUSA || !(animZones & (1u << zn)))
    return colorForZone(zn, blinkOn);

  if (animKind == ANIM_FAULT) {
    if (animActive) {
      if (distInPiece(s, i, p) <= front) return COLOR_FAULT;
      return (zn <= ZN_Z3) ? COLOR_SRC_A : COLOR_SRC_B;   /* as it was at 00 */
    }
    if (!(faultZones & (1u << zn))) return COLOR_FAULT;   /* lost power      */
    return colorForZone(zn, blinkOn);                     /* faulted, blinks */
  }

  if (animKind == ANIM_RESTORE && animActive && distInPiece(s, i, p) > front)
    return COLOR_DEAD;                                    /* not reached yet */

  return colorForZone(zn, blinkOn);
}

void render()
{
  /* The faulted section blinks while it is live and arcing, steps 01 and 02.
   * Once it is isolated it holds solid red as a work boundary.             */
  const bool blinking = (stepNow == ST_FAULT || stepNow == ST_LOCKOUT);
  const bool blinkOn  = blinking ? (((millis() / FAULT_BLINK_MS) & 1) != 0) : true;
  const uint16_t front = animFront();

  uint16_t idx = 0;
  for (uint8_t s = 0; s < NUM_SEGMENTS; s++) {
    const uint8_t len   = pgm_read_byte(&SEG_LEN[s]);
    const uint8_t over  = pgm_read_byte(&SEG_OVER[s]);
    const uint8_t split = pgm_read_byte(&SEG_SPLIT[s]);
    const uint8_t zHead = pgm_read_byte(&SEG_ZONE[s]);
    const uint8_t zTail = pgm_read_byte(&SEG_ZONE2[s]);

    Piece p;
    uint8_t pk = 0;
    getPiece(s, 0, p);

    for (uint8_t i = 0; i < len; i++) {
      if (idx >= NUM_LEDS) break;
      if (i > p.hi) getPiece(s, ++pk, p);
      uint8_t zn = (split && i >= split) ? zTail : zHead;
      if (!over) zn = ZN_HID;                       /* never light a return */
      leds[idx++] = colorForPixel(zn, s, i, p, front, blinkOn);
    }
  }
  while (idx < NUM_LEDS) leds[idx++] = COLOR_DEAD;  /* any surplus pixels */

  FastLED.show();
}

void renderDeviceLeds()
{
  const bool slow = ((millis() / DEV_TRIP_BLINK_MS) & 1) != 0;
  const bool fast = ((millis() / DEV_LOCK_BLINK_MS) & 1) != 0;

  for (uint8_t d = 0; d < NUM_DEVICES; d++) {
#if DEVICE_LED_MODE == 1
    /* one pin: lit means closed, blinking means tripped or locked out */
    bool lit = (devState[d] == DS_CLOSED);
    if (devState[d] == DS_TRIPPED) lit = slow;
    if (devState[d] == DS_LOCKOUT) lit = fast;
    digitalWrite(pgm_read_byte(&DEV_PIN[d]), lit ? HIGH : LOW);
#else
    bool closed = (devState[d] == DS_CLOSED);
    bool opened = (devState[d] == DS_OPEN);
    if (devState[d] == DS_TRIPPED) opened = slow;
    if (devState[d] == DS_LOCKOUT) opened = fast;
    digitalWrite(pgm_read_byte(&DEV_PIN_G[d]), closed ? HIGH : LOW);
    digitalWrite(pgm_read_byte(&DEV_PIN_R[d]), opened ? HIGH : LOW);
#endif
  }
}

/* ===========================================================================
 * SERIAL NARRATION
 * =========================================================================== */
void printDeviceName(uint8_t d)
{
  switch (d) {
    case DEV_SUB_A_BKR: Serial.print(F("SUB_A_BKR")); break;
    case DEV_A1:        Serial.print(F("DEV_A1"));    break;
    case DEV_A2:        Serial.print(F("DEV_A2"));    break;
    case DEV_TIE:       Serial.print(F("TIE"));       break;
    case DEV_B2:        Serial.print(F("DEV_B2"));    break;
    case DEV_B1:        Serial.print(F("DEV_B1"));    break;
    case DEV_SUB_B_BKR: Serial.print(F("SUB_B_BKR")); break;
    default:            Serial.print(F("DER_PCC"));   break;
  }
}

void printZState(ZState z)
{
  switch (z) {
    case ZS_A:     Serial.print(F("A"));    break;
    case ZS_B:     Serial.print(F("B"));    break;
    case ZS_FAULT: Serial.print(F("FLT"));  break;
    default:       Serial.print(F("dead")); break;
  }
}

void printState()
{
  Serial.println();
  Serial.print(F("STEP 0"));
  Serial.print(stepNow);
  Serial.print(F("  "));
  switch (stepNow) {
    case ST_NORMAL:  Serial.println(F("NORMAL"));  break;
    case ST_FAULT:   Serial.println(F("FAULT"));   break;
    case ST_LOCKOUT: Serial.println(F("LOCKOUT")); break;
    case ST_ISOLATE: Serial.println(F("ISOLATE")); break;
    default:         Serial.println(F("RESTORE")); break;
  }

  Serial.print(F("  fault   : "));
  if      (faultSel == FAULT_NONE) Serial.println(F("none"));
  else if (faultSel == FAULT_DER)  Serial.println(F("DER branch"));
  else  { Serial.print(F("Z")); Serial.println(faultSel); }

  Serial.print(F("  zones   : "));
  for (uint8_t k = 1; k <= 6; k++) {
    Serial.print(F("Z")); Serial.print(k); Serial.print(F("="));
    printZState(zoneState[k]);
    Serial.print(F(" "));
  }
  Serial.print(F("DER="));
  printZState(derDisplayState());
  Serial.println();

  Serial.print(F("  devices : "));
  for (uint8_t d = 0; d < NUM_DEVICES; d++) {
    printDeviceName(d);
    Serial.print(F("="));
    switch (devState[d]) {
      case DS_CLOSED:  Serial.print(F("CLOSED"));  break;
      case DS_OPEN:    Serial.print(F("OPEN"));    break;
      case DS_TRIPPED: Serial.print(F("TRIPPED")); break;
      default:         Serial.print(F("LOCKOUT")); break;
    }
    Serial.print(F(" "));
  }
  Serial.println();
}

/* ===========================================================================
 * STATE TRANSITIONS
 * =========================================================================== */
void goToStep(uint8_t s)
{
  stepNow = s;
  stepStartedAt = millis();
  computeModel();
  startAnimation();
  printState();
}

void startFault(uint8_t f)
{
  faultSel = f;
  goToStep(ST_FAULT);
}

void resetAll()
{
  faultSel = FAULT_NONE;
  goToStep(ST_NORMAL);
}

/* ===========================================================================
 * BUTTONS
 * =========================================================================== */
void initButtons()
{
  for (uint8_t b = 0; b < NUM_BUTTONS; b++) {
    pinMode(pgm_read_byte(&BTN_PIN[b]), INPUT_PULLUP);
    btnStable[b]    = true;      /* true = released, pull-up holds it HIGH */
    btnLast[b]      = true;
    btnChangedAt[b] = 0;
  }
}

/* Returns the index of a button that was just pressed, or 255 for none. */
uint8_t pollButtons()
{
  uint8_t pressed = 255;
  const uint32_t now = millis();

  for (uint8_t b = 0; b < NUM_BUTTONS; b++) {
    const bool raw = (digitalRead(pgm_read_byte(&BTN_PIN[b])) == HIGH);
    if (raw != btnLast[b]) {
      btnLast[b]      = raw;
      btnChangedAt[b] = now;
    }
    else if ((now - btnChangedAt[b]) >= DEBOUNCE_MS && raw != btnStable[b]) {
      btnStable[b] = raw;
      if (!raw && pressed == 255) pressed = b;   /* falling edge = pressed */
    }
  }
  return pressed;
}

void handleButton(uint8_t b)
{
  if (b == BTN_RESET_IDX) { resetAll(); return; }

  /* b 0..5 -> Z1..Z6, b 6 -> DER */
  const uint8_t f = (b == BTN_DER_IDX) ? FAULT_DER : (uint8_t)(b + 1);

  if (f == faultSel && stepNow != ST_NORMAL) {
    if (stepNow < ST_LAST) goToStep(stepNow + 1);   /* same button steps on */
  } else {
    startFault(f);
  }
}

/* ===========================================================================
 * SETUP AND LOOP
 * =========================================================================== */
void segmentTest()
{
  /* Walk the chain one run at a time so you can check the counts by eye. */
  uint16_t startIdx = 0;
  for (uint8_t s = 0; s < NUM_SEGMENTS; s++) {
    const uint8_t len = pgm_read_byte(&SEG_LEN[s]);
    if (len == 0) continue;

    fill_solid(leds, NUM_LEDS, CRGB::Black);
    for (uint8_t i = 0; i < len && (uint16_t)(startIdx + i) < NUM_LEDS; i++)
      leds[startIdx + i] = CHSV((uint8_t)((uint16_t)s * 255 / NUM_SEGMENTS), 255, 255);
    FastLED.show();

    Serial.print(F("segment "));  Serial.print(s + 1);
    Serial.print(F("  px "));     Serial.print(startIdx);
    Serial.print(F(" .. "));      Serial.print(startIdx + len - 1);
    Serial.print(F("  len "));    Serial.println(len);

    startIdx += len;
    delay(SEGMENT_TEST_MS);
  }
}

void setup()
{
  Serial.begin(115200);
  delay(200);

  Serial.println(F("\n=== JEA Tabletop FLISR Trainer REV1 ==="));

  /* verify the table adds up to the compiled strip length */
  uint16_t sum = 0;
  for (uint8_t s = 0; s < NUM_SEGMENTS; s++) sum += pgm_read_byte(&SEG_LEN[s]);
  Serial.print(F("segment table total : ")); Serial.println(sum);
  Serial.print(F("NUM_LEDS            : ")); Serial.println(NUM_LEDS);
  if (sum != NUM_LEDS) {
    Serial.println(F("[!] MISMATCH. Set NUM_LEDS to the segment table total above."));
  } else {
    Serial.println(F("[OK] segment table matches NUM_LEDS"));
  }

  initButtons();

#if DEVICE_LED_MODE == 1
  for (uint8_t d = 0; d < NUM_DEVICES; d++) {
    pinMode(pgm_read_byte(&DEV_PIN[d]), OUTPUT);
    digitalWrite(pgm_read_byte(&DEV_PIN[d]), LOW);
  }
#else
  for (uint8_t d = 0; d < NUM_DEVICES; d++) {
    pinMode(pgm_read_byte(&DEV_PIN_G[d]), OUTPUT);
    pinMode(pgm_read_byte(&DEV_PIN_R[d]), OUTPUT);
    digitalWrite(pgm_read_byte(&DEV_PIN_G[d]), LOW);
    digitalWrite(pgm_read_byte(&DEV_PIN_R[d]), LOW);
  }
#endif

  FastLED.addLeds<LED_TYPE, LED_DATA_PIN, COLOR_ORDER>(leds, NUM_LEDS)
         .setCorrection(TypicalLEDStrip);
  FastLED.setBrightness(BRIGHTNESS);
  FastLED.setMaxPowerInVoltsAndMilliamps(5, MAX_MILLIAMPS);
  fill_solid(leds, NUM_LEDS, CRGB::Black);
  FastLED.show();

#if SEGMENT_TEST_MODE
  Serial.println(F("[!] SEGMENT_TEST_MODE is on. Set it to 0 for normal operation."));
  segmentTest();
#endif

  resetAll();
}

void loop()
{
  const uint8_t b = pollButtons();
  if (b != 255) handleButton(b);

  /* REV1: when an animation reaches its last pixel the step timer restarts,
   * so every step is on screen for STEP_INTERVAL_MS after it finishes.     */
  if (animActive && animFront() >= animLast) {
    animActive = false;
    stepStartedAt = millis();
  }

#if AUTO_ADVANCE
  if (stepNow != ST_NORMAL && stepNow < ST_LAST && !animActive &&
      (millis() - stepStartedAt) >= STEP_INTERVAL_MS) {
    goToStep(stepNow + 1);
  }
#endif

  renderDeviceLeds();          /* cheap, runs every pass so blinks stay even */

  static uint32_t lastFrame = 0;
  if ((millis() - lastFrame) >= FRAME_INTERVAL_MS) {
    lastFrame = millis();
    render();
  }
}
