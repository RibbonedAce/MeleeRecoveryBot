#define PY_SSIZE_T_CLEAN

#include <Python.h>
#include <algorithm>
#include <iostream>
#include <map>
#include <vector>
#include <string>
#include "trajectory.cpp"
#include "vector2.cpp"
#include "range.cpp"
#include "knockback.cpp"
#include "defaultdict.cpp"
#include "ledgebox.cpp"
#include "frameinput.cpp"
#include "utils.cpp"

using namespace std;

#define MAX_NUM_FRAMES 60
#define TOO_LOW_RESULT -100
typedef DefaultDict<const long, const FrameInput*> InputFrames;

#define TF Trajectory::Frame
#define V2 new Vector2

static map<const string, const Trajectory*> trajectoryMap{
    // Dev starts at 0. Accelerate dev by 0.044 * input per frame, up to 0.952. If trimmed forward input * 0.952 < dev, then dev is trimmed input * 0.952. Result is dev + mid vel
    {"FalconDive.Normal", new Trajectory(0, 44, LEDGE_GRAB_MODE_ALWAYS, false, new Trajectory::Frames{
        new TF(V2(0, 0), V2(4.68226, 3.05551)),
        new TF(TF::defaultHorizontalCalculator( 0.00000,  0.00000, 0.044, 0.952,  0.00000), V2( 3.26468,  4.40120)),
        new TF(TF::defaultHorizontalCalculator( 0.00000,  0.00000, 0.044, 0.952,  0.00000), V2( 3.25177,  4.64514)),
        new TF(TF::defaultHorizontalCalculator( 0.00000,  0.00000, 0.044, 0.952,  0.00000), V2( 8.79018,  4.39903)),
        new TF(TF::defaultHorizontalCalculator( 0.00000,  0.00000, 0.044, 0.952,  0.00000), V2( 9.28287,  2.17155)),
        new TF(TF::defaultHorizontalCalculator(-0.00191,  0.00000, 0.044, 0.952, -0.00078), V2( 9.31236,  2.04197)),
        new TF(TF::defaultHorizontalCalculator(-0.00464, -0.00191, 0.044, 0.952, -0.00189), V2( 9.32870,  1.95708)),
        new TF(TF::defaultHorizontalCalculator(-0.00573, -0.00464, 0.044, 0.952, -0.00233), V2( 9.33434,  1.91307)),
        new TF(TF::defaultHorizontalCalculator(-0.00518, -0.00573, 0.044, 0.952, -0.00211), V2( 9.33206,  1.90608)),
        new TF(TF::defaultHorizontalCalculator(-0.00300, -0.00518, 0.044, 0.952, -0.00122), V2( 9.32266,  1.93227)),
        new TF(TF::defaultHorizontalCalculator( 0.00082, -0.00300, 0.044, 0.952,  0.00033), V2( 9.30284,  1.98782)),
        new TF(TF::defaultHorizontalCalculator( 0.00628,  0.00082, 0.044, 0.952,  0.00255), V2( 9.27229,  2.06885)),
        new TF(TF::defaultHorizontalCalculator( 0.01337,  0.00628, 0.044, 0.952,  0.00544), V2( 9.22549,  2.17155), new vector<double>{0, 0.3, 1}),
        new TF(TF::defaultHorizontalCalculator( 0.34782,  0.01337, 0.044, 0.952,  2.55553), V2( 4.48185,  2.17155)),
        new TF(TF::defaultHorizontalCalculator( 0.35129,  0.34782, 0.044, 0.952,  2.45635), V2( 2.79940,  2.17155)),
        new TF(TF::defaultHorizontalCalculator( 0.35466,  0.35129, 0.044, 0.952,  2.35818), V2( 3.10504,  2.17155)),
        new TF(TF::defaultHorizontalCalculator( 0.35790,  0.35466, 0.044, 0.952,  2.26101), V2( 3.15591,  2.17155)),
        new TF(TF::defaultHorizontalCalculator( 0.36104,  0.35790, 0.044, 0.952,  2.16485), V2( 3.21330,  2.09195)),
        new TF(TF::defaultHorizontalCalculator( 0.36407,  0.36104, 0.044, 0.952,  2.06970), V2( 3.27756,  2.03454)),
        new TF(TF::defaultHorizontalCalculator( 0.36698,  0.36407, 0.044, 0.952,  1.97556), V2( 3.34645,  1.92649)),
        new TF(TF::defaultHorizontalCalculator( 0.36979,  0.36698, 0.044, 0.952,  1.88242), V2( 3.41775,  1.82328)),
        new TF(TF::defaultHorizontalCalculator( 0.37248,  0.36979, 0.044, 0.952,  1.79029), V2( 3.49127,  1.78043)),
        new TF(TF::defaultHorizontalCalculator( 0.37506,  0.37248, 0.044, 0.952,  1.69916), V2( 3.57682,  1.85330)),
        new TF(TF::defaultHorizontalCalculator( 0.37753,  0.37506, 0.044, 0.952,  1.60904), V2( 3.85916,  2.09409)),
        new TF(TF::defaultHorizontalCalculator( 0.37989,  0.37753, 0.044, 0.952,  1.51993), V2( 4.14859,  2.43761)),
        new TF(TF::defaultHorizontalCalculator( 0.38213,  0.37989, 0.044, 0.952,  1.43183), V2( 4.38652,  2.84683)),
        new TF(TF::defaultHorizontalCalculator( 0.38427,  0.38213, 0.044, 0.952,  1.34473), V2( 4.66598,  3.28535)),
        new TF(TF::defaultHorizontalCalculator( 0.38629,  0.38427, 0.044, 0.952,  1.25863), V2( 4.61559,  3.71272)),
        new TF(TF::defaultHorizontalCalculator( 0.38820,  0.38629, 0.044, 0.952,  1.17355), V2( 4.55109,  4.11132)),
        new TF(TF::defaultHorizontalCalculator( 0.39000,  0.38820, 0.044, 0.952,  1.08947), V2( 4.69933,  4.46805)),
        new TF(TF::defaultHorizontalCalculator( 0.39169,  0.39000, 0.044, 0.952,  1.00640), V2( 4.57400,  4.82301)),
        new TF(TF::defaultHorizontalCalculator( 0.39326,  0.39169, 0.044, 0.952,  0.92434), V2( 3.75492,  4.91762)),
        new TF(TF::defaultHorizontalCalculator( 0.39473,  0.39326, 0.044, 0.952,  0.84328), V2( 3.14838,  5.20760)),
        new TF(TF::defaultHorizontalCalculator( 0.39608,  0.39473, 0.044, 0.952,  0.76332), V2( 3.94477,  5.91740)),
        new TF(TF::defaultHorizontalCalculator( 0.39732,  0.39608, 0.044, 0.952,  0.68419), V2( 4.54568,  6.68407)),
        new TF(TF::defaultHorizontalCalculator( 0.39845,  0.39732, 0.044, 0.952,  0.60614), V2(11.01106,  7.16891)),
        new TF(TF::defaultHorizontalCalculator( 0.39947,  0.39845, 0.044, 0.952,  0.52912), V2(10.62404,  7.24241)),
        new TF(TF::defaultHorizontalCalculator( 0.40038,  0.39947, 0.044, 0.952,  0.45309), V2( 4.97551,  7.64799)),
        new TF(TF::defaultHorizontalCalculator( 0.40117,  0.40038, 0.044, 0.952,  0.37807), V2( 3.98034,  8.44759)),
        new TF(TF::defaultHorizontalCalculator( 0.40186,  0.40117, 0.044, 0.952,  0.30406), V2( 3.36038,  8.54461)),
        new TF(TF::defaultHorizontalCalculator( 0.40243,  0.40186, 0.044, 0.952,  0.23106), V2( 2.94270,  9.12956)),
        new TF(TF::defaultHorizontalCalculator( 0.40290,  0.40243, 0.044, 0.952,  0.15906), V2( 3.68528, 11.20951)),
        new TF(TF::defaultHorizontalCalculator( 0.40324,  0.40290, 0.044, 0.952,  0.08807), V2( 3.10056, 13.17873)),
        new TF(TF::defaultHorizontalCalculator( 0.40349,  0.40324, 0.044, 0.952,  0.01808), V2( 2.75662, 12.47581)),
        new TF(TF::defaultHorizontalCalculator( 0.40361,  0.40349, 0.044, 0.952, -0.05088), V2( 3.89386, 12.42949)),
        new TF(TF::defaultHorizontalCalculator( 0.40362,  0.40361, 0.044, 0.952, -0.11886), V2( 4.60036, 12.86417)),
        new TF(TF::defaultHorizontalCalculator( 0.40353,  0.40362, 0.044, 0.952, -0.27163), V2( 6.00366, 13.55915)),
        new TF(TF::defaultHorizontalCalculator( 0.40332,  0.40353, 0.044, 0.952, -0.49663), V2( 5.73695, 14.35724)),
        new TF(TF::defaultHorizontalCalculator( 0.40300,  0.40332, 0.044, 0.952, -0.70176), V2( 5.63338, 13.16108)),
        new TF(TF::defaultHorizontalCalculator( 0.40257,  0.40300, 0.044, 0.952, -0.88704), V2( 6.48798, 11.59608)),
        new TF(TF::defaultHorizontalCalculator( 0.40203,  0.40257, 0.044, 0.952, -1.05243), V2( 3.93866,  9.92639)),
        new TF(TF::defaultHorizontalCalculator( 0.40137,  0.40203, 0.044, 0.952, -1.19797), V2( 2.58432,  7.72705)),
        new TF(TF::defaultHorizontalCalculator( 0.40061,  0.40137, 0.044, 0.952, -1.32366), V2( 2.00000,  6.41431)),
        new TF(TF::defaultHorizontalCalculator( 0.39973,  0.40061, 0.044, 0.952, -1.42945), V2( 2.00000,  6.58787)),
        new TF(TF::defaultHorizontalCalculator( 0.39874,  0.39973, 0.044, 0.952, -1.51540), V2( 2.37886,  8.26091)),
        new TF(TF::defaultHorizontalCalculator( 0.39764,  0.39874, 0.044, 0.952, -1.58148), V2( 2.77595,  9.84751)),
        new TF(TF::defaultHorizontalCalculator( 0.39643,  0.39764, 0.044, 0.952, -1.62769), V2( 2.38101, 12.09016)),
        new TF(TF::defaultHorizontalCalculator( 0.39511,  0.39643, 0.044, 0.952, -1.65403), V2( 2.39545, 11.62578)),
        new TF(TF::defaultHorizontalCalculator( 0.39367,  0.39511, 0.044, 0.952, -1.66051), V2( 2.30524, 10.76665)),
        new TF(TF::defaultHorizontalCalculator( 0.39212,  0.39367, 0.044, 0.952, -1.64713), V2( 2.19550,  9.73038)),
        new TF(TF::defaultHorizontalCalculator( 0.39047,  0.39212, 0.044, 0.952, -1.61388), V2( 2.63750,  8.72971)),
        new TF(TF::defaultHorizontalCalculator( 0.38869,  0.39047, 0.044, 0.952, -1.56076), V2( 2.80614,  7.34959)),
        new TF(TF::defaultHorizontalCalculator( 0.38682,  0.38869, 0.044, 0.952, -1.48778), V2( 2.89906,  4.83779)),
        new TF(TF::defaultHorizontalCalculator( 0.38482,  0.38682, 0.044, 0.952, -1.39494), V2( 3.63506,  3.19494)),
        new TF(TF::driftCalculator(0.13, 2.9, 1.12, 0.06, 0.01, 2.9), V2(2, 0))
    })},
    {"FalconDive.Reverse", new Trajectory(0, 44, LEDGE_GRAB_MODE_DURING, false, new Trajectory::Frames{
        new TF(V2(0, 0), V2(4.68226, 3.05551)),
        new TF(TF::defaultHorizontalCalculator( 0.00000,  0.00000, 0.044, 0.952,  0.00000), V2( 3.26468,  4.40120)),
        new TF(TF::defaultHorizontalCalculator( 0.00000,  0.00000, 0.044, 0.952,  0.00000), V2( 3.25177,  4.64514)),
        new TF(TF::defaultHorizontalCalculator( 0.00000,  0.00000, 0.044, 0.952,  0.00000), V2( 8.79018,  4.39903)),
        new TF(TF::defaultHorizontalCalculator( 0.00000,  0.00000, 0.044, 0.952,  0.00000), V2( 9.28287,  2.17155)),
        new TF(TF::defaultHorizontalCalculator(-0.00191,  0.00000, 0.044, 0.952, -0.00078), V2( 9.31236,  2.04197)),
        new TF(TF::defaultHorizontalCalculator(-0.00464, -0.00191, 0.044, 0.952, -0.00189), V2( 9.32870,  1.95708)),
        new TF(TF::defaultHorizontalCalculator(-0.00573, -0.00464, 0.044, 0.952, -0.00233), V2( 9.33434,  1.91307)),
        new TF(TF::defaultHorizontalCalculator(-0.00518, -0.00573, 0.044, 0.952, -0.00211), V2( 9.33206,  1.90608)),
        new TF(TF::defaultHorizontalCalculator(-0.00300, -0.00518, 0.044, 0.952, -0.00122), V2( 9.32266,  1.93227)),
        new TF(TF::defaultHorizontalCalculator( 0.00082, -0.00300, 0.044, 0.952,  0.00033), V2( 9.30284,  1.98782)),
        new TF(TF::defaultHorizontalCalculator( 0.00628,  0.00082, 0.044, 0.952,  0.00255), V2( 9.27229,  2.06885)),
        new TF(TF::defaultHorizontalCalculator(-0.01337,  0.00628, 0.044, 0.952,  0.00544), V2( 3.69378,  2.17155), new vector<double>{-1, -0.3}),
        new TF(TF::defaultHorizontalCalculator(-0.34782, -0.01337, 0.044, 0.952,  2.55553), V2( 4.48185,  2.17155)),
        new TF(TF::defaultHorizontalCalculator(-0.35129, -0.34782, 0.044, 0.952,  2.45635), V2( 2.79940,  2.17155)),
        new TF(TF::defaultHorizontalCalculator(-0.35466, -0.35129, 0.044, 0.952,  2.35818), V2( 3.10504,  2.17155)),
        new TF(TF::defaultHorizontalCalculator(-0.35790, -0.35466, 0.044, 0.952,  2.26101), V2( 3.15591,  2.17155)),
        new TF(TF::defaultHorizontalCalculator(-0.36104, -0.35790, 0.044, 0.952,  2.16485), V2( 3.21330,  2.09195)),
        new TF(TF::defaultHorizontalCalculator(-0.36407, -0.36104, 0.044, 0.952,  2.06970), V2( 3.27756,  2.03454)),
        new TF(TF::defaultHorizontalCalculator(-0.36698, -0.36407, 0.044, 0.952,  1.97556), V2( 3.34645,  1.92649)),
        new TF(TF::defaultHorizontalCalculator(-0.36979, -0.36698, 0.044, 0.952,  1.88242), V2( 3.41775,  1.82328)),
        new TF(TF::defaultHorizontalCalculator(-0.37248, -0.36979, 0.044, 0.952,  1.79029), V2( 3.49127,  1.78043)),
        new TF(TF::defaultHorizontalCalculator(-0.37506, -0.37248, 0.044, 0.952,  1.69916), V2( 3.57682,  1.85330)),
        new TF(TF::defaultHorizontalCalculator(-0.37753, -0.37506, 0.044, 0.952,  1.60904), V2( 3.85916,  2.09409)),
        new TF(TF::defaultHorizontalCalculator(-0.37989, -0.37753, 0.044, 0.952,  1.51993), V2( 4.14859,  2.43761)),
        new TF(TF::defaultHorizontalCalculator(-0.38213, -0.37989, 0.044, 0.952,  1.43183), V2( 4.38652,  2.84683)),
        new TF(TF::defaultHorizontalCalculator(-0.38427, -0.38213, 0.044, 0.952,  1.34473), V2( 4.66598,  3.28535)),
        new TF(TF::defaultHorizontalCalculator(-0.38629, -0.38427, 0.044, 0.952,  1.25863), V2( 4.61559,  3.71272)),
        new TF(TF::defaultHorizontalCalculator(-0.38820, -0.38629, 0.044, 0.952,  1.17355), V2( 4.55109,  4.11132)),
        new TF(TF::defaultHorizontalCalculator(-0.39000, -0.38820, 0.044, 0.952,  1.08947), V2( 4.69933,  4.46805)),
        new TF(TF::defaultHorizontalCalculator(-0.39169, -0.39000, 0.044, 0.952,  1.00640), V2( 4.57400,  4.82301)),
        new TF(TF::defaultHorizontalCalculator(-0.39326, -0.39169, 0.044, 0.952,  0.92434), V2( 3.75492,  4.91762)),
        new TF(TF::defaultHorizontalCalculator(-0.39473, -0.39326, 0.044, 0.952,  0.84328), V2( 3.14838,  5.20760)),
        new TF(TF::defaultHorizontalCalculator(-0.39608, -0.39473, 0.044, 0.952,  0.76332), V2( 3.94477,  5.91740)),
        new TF(TF::defaultHorizontalCalculator(-0.39732, -0.39608, 0.044, 0.952,  0.68419), V2( 4.54568,  6.68407)),
        new TF(TF::defaultHorizontalCalculator(-0.39845, -0.39732, 0.044, 0.952,  0.60614), V2( 2.00000,  7.16891)),
        new TF(TF::defaultHorizontalCalculator(-0.39947, -0.39845, 0.044, 0.952,  0.52912), V2( 2.00000,  7.24241)),
        new TF(TF::defaultHorizontalCalculator(-0.40038, -0.39947, 0.044, 0.952,  0.45309), V2( 4.97551,  7.64799)),
        new TF(TF::defaultHorizontalCalculator(-0.40117, -0.40038, 0.044, 0.952,  0.37807), V2( 3.98034,  8.44759)),
        new TF(TF::defaultHorizontalCalculator(-0.40186, -0.40117, 0.044, 0.952,  0.30406), V2( 3.36038,  8.54461)),
        new TF(TF::defaultHorizontalCalculator(-0.40243, -0.40186, 0.044, 0.952,  0.23106), V2( 2.94270,  9.12956)),
        new TF(TF::defaultHorizontalCalculator(-0.40290, -0.40243, 0.044, 0.952,  0.15906), V2( 3.68528, 11.20951)),
        new TF(TF::defaultHorizontalCalculator(-0.40324, -0.40290, 0.044, 0.952,  0.08807), V2( 3.10056, 13.17873)),
        new TF(TF::defaultHorizontalCalculator(-0.40349, -0.40324, 0.044, 0.952,  0.01808), V2( 2.75662, 12.47581)),
        new TF(TF::defaultHorizontalCalculator(-0.40361, -0.40349, 0.044, 0.952, -0.05088), V2( 3.89386, 12.42949)),
        new TF(TF::defaultHorizontalCalculator(-0.40362, -0.40361, 0.044, 0.952, -0.11886), V2( 4.60036, 12.86417)),
        new TF(TF::defaultHorizontalCalculator(-0.40353, -0.40362, 0.044, 0.952, -0.27163), V2( 4.94836, 13.55915)),
        new TF(TF::defaultHorizontalCalculator(-0.40332, -0.40353, 0.044, 0.952, -0.49663), V2( 5.83629, 14.35724)),
        new TF(TF::defaultHorizontalCalculator(-0.40300, -0.40332, 0.044, 0.952, -0.70176), V2( 6.04415, 13.16108)),
        new TF(TF::defaultHorizontalCalculator(-0.40257, -0.40300, 0.044, 0.952, -0.88704), V2( 5.30399, 11.59608)),
        new TF(TF::defaultHorizontalCalculator(-0.40203, -0.40257, 0.044, 0.952, -1.05243), V2( 3.93865,  9.92639)),
        new TF(TF::defaultHorizontalCalculator(-0.40137, -0.40203, 0.044, 0.952, -1.19797), V2( 2.58432,  7.72705)),
        new TF(TF::defaultHorizontalCalculator(-0.40061, -0.40137, 0.044, 0.952, -1.32366), V2( 2.00000,  6.41431)),
        new TF(TF::defaultHorizontalCalculator(-0.39973, -0.40061, 0.044, 0.952, -1.42945), V2( 2.00000,  6.58787)),
        new TF(TF::defaultHorizontalCalculator(-0.39874, -0.39973, 0.044, 0.952, -1.51540), V2( 2.37886,  8.26091)),
        new TF(TF::defaultHorizontalCalculator(-0.39764, -0.39874, 0.044, 0.952, -1.58148), V2( 2.77595,  9.84751)),
        new TF(TF::defaultHorizontalCalculator(-0.39643, -0.39764, 0.044, 0.952, -1.62769), V2( 2.38101, 12.09016)),
        new TF(TF::defaultHorizontalCalculator(-0.39511, -0.39643, 0.044, 0.952, -1.65403), V2( 2.39545, 11.62578)),
        new TF(TF::defaultHorizontalCalculator(-0.39367, -0.39511, 0.044, 0.952, -1.66051), V2( 2.30524, 10.76665)),
        new TF(TF::defaultHorizontalCalculator(-0.39212, -0.39367, 0.044, 0.952, -1.64713), V2( 2.19550,  9.73038)),
        new TF(TF::defaultHorizontalCalculator(-0.39047, -0.39212, 0.044, 0.952, -1.61388), V2( 2.63750,  8.72971)),
        new TF(TF::defaultHorizontalCalculator(-0.38869, -0.39047, 0.044, 0.952, -1.56076), V2( 2.80614,  7.34959)),
        new TF(TF::defaultHorizontalCalculator(-0.38682, -0.38869, 0.044, 0.952, -1.48778), V2( 2.89906,  4.83779)),
        new TF(TF::defaultHorizontalCalculator(-0.38482, -0.38682, 0.044, 0.952, -1.39494), V2( 3.63506,  3.19494)),
        new TF(TF::driftCalculator(0.13, 2.9, 1.12, 0.06, 0.01, 2.9), V2(2, 0))
    })},
    {"DarkDive.Normal", new Trajectory(0, 44, LEDGE_GRAB_MODE_ALWAYS, false, new Trajectory::Frames{
        new TF(V2(0, 0), V2(6.82229, 3.00536)),
        new TF(TF::defaultHorizontalCalculator( 0.00000,  0.00000, 0.044, 0.663,  0.00000), V2( 3.41854,  4.17136)),
        new TF(TF::defaultHorizontalCalculator( 0.00000,  0.00000, 0.044, 0.663,  0.00000), V2( 2.97136,  4.52726)),
        new TF(TF::defaultHorizontalCalculator( 0.00000,  0.00000, 0.044, 0.663,  0.00000), V2( 9.48408,  4.00385)),
        new TF(TF::defaultHorizontalCalculator( 0.00000,  0.00000, 0.044, 0.663,  0.00000), V2(10.68512,  1.69978)),
        new TF(TF::defaultHorizontalCalculator(-0.00213,  0.00000, 0.044, 0.663, -0.00087), V2(10.71249,  1.55549)),
        new TF(TF::defaultHorizontalCalculator(-0.00517, -0.00213, 0.044, 0.663, -0.00210), V2(10.73668,  1.46099)),
        new TF(TF::defaultHorizontalCalculator(-0.00638, -0.00517, 0.044, 0.663, -0.00260), V2(10.75568,  1.41198)),
        new TF(TF::defaultHorizontalCalculator(-0.00577, -0.00638, 0.044, 0.663, -0.00235), V2(10.76583,  1.40420)),
        new TF(TF::defaultHorizontalCalculator(-0.00334, -0.00577, 0.044, 0.663, -0.00136), V2(10.76215,  1.43336)),
        new TF(TF::defaultHorizontalCalculator( 0.00091, -0.00334, 0.044, 0.663,  0.00037), V2(10.73588,  1.49520)),
        new TF(TF::defaultHorizontalCalculator( 0.00699,  0.00091, 0.044, 0.663,  0.00284), V2(10.68268,  1.58543)),
        new TF(TF::defaultHorizontalCalculator( 0.01489,  0.00699, 0.044, 0.663,  0.00606), V2(10.59043,  1.69978), new vector<double>{0, 0.3, 1}),
        new TF(TF::defaultHorizontalCalculator( 0.38727,  0.01489, 0.044, 0.663,  2.84533), V2( 4.28408,  1.69978)),
        new TF(TF::defaultHorizontalCalculator( 0.39113,  0.38727, 0.044, 0.663,  2.73491), V2( 3.17785,  1.69978)),
        new TF(TF::defaultHorizontalCalculator( 0.39487,  0.39113, 0.044, 0.663,  2.62560), V2( 3.78630,  1.69978)),
        new TF(TF::defaultHorizontalCalculator( 0.39849,  0.39487, 0.044, 0.663,  2.51742), V2( 3.80862,  1.69978)),
        new TF(TF::defaultHorizontalCalculator( 0.40199,  0.39849, 0.044, 0.663,  2.41035), V2( 3.81985,  2.33026)),
        new TF(TF::defaultHorizontalCalculator( 0.40536,  0.40199, 0.044, 0.663,  2.30441), V2( 3.82517,  2.26294)),
        new TF(TF::defaultHorizontalCalculator( 0.40860,  0.40536, 0.044, 0.663,  2.19959), V2( 3.82999,  2.13864)),
        new TF(TF::defaultHorizontalCalculator( 0.41172,  0.40860, 0.044, 0.663,  2.09588), V2( 3.83962,  2.01963)),
        new TF(TF::defaultHorizontalCalculator( 0.41472,  0.41172, 0.044, 0.663,  1.99331), V2( 3.85875,  1.96821)),
        new TF(TF::defaultHorizontalCalculator( 0.41759,  0.41472, 0.044, 0.663,  1.89185), V2( 3.89097,  2.04651)),
        new TF(TF::defaultHorizontalCalculator( 0.42034,  0.41759, 0.044, 0.663,  1.79151), V2( 4.19507,  2.31339)),
        new TF(TF::defaultHorizontalCalculator( 0.42297,  0.42034, 0.044, 0.663,  1.69229), V2( 4.55337,  2.69658)),
        new TF(TF::defaultHorizontalCalculator( 0.42547,  0.42297, 0.044, 0.663,  1.59420), V2( 4.77227,  3.16121)),
        new TF(TF::defaultHorizontalCalculator( 0.42784,  0.42547, 0.044, 0.663,  1.49722), V2( 4.98158,  3.66881)),
        new TF(TF::defaultHorizontalCalculator( 0.43009,  0.42784, 0.044, 0.663,  1.40436), V2( 4.86576,  4.16086)),
        new TF(TF::defaultHorizontalCalculator( 0.43222,  0.43009, 0.044, 0.663,  1.30663), V2( 4.93086,  4.59776)),
        new TF(TF::defaultHorizontalCalculator( 0.43423,  0.43222, 0.044, 0.663,  1.21302), V2(10.13076,  4.98760)),
        new TF(TF::defaultHorizontalCalculator( 0.43610,  0.43423, 0.044, 0.663,  1.12053), V2(10.06803,  5.33732)),
        new TF(TF::defaultHorizontalCalculator( 0.43786,  0.43610, 0.044, 0.663,  1.02916), V2( 4.16913,  5.49883)),
        new TF(TF::defaultHorizontalCalculator( 0.43949,  0.43786, 0.044, 0.663,  0.93891), V2( 3.37916,  5.78750)),
        new TF(TF::defaultHorizontalCalculator( 0.44100,  0.43949, 0.044, 0.663,  0.84977), V2( 4.20500,  6.50863)),
        new TF(TF::defaultHorizontalCalculator( 0.44238,  0.44100, 0.044, 0.663,  0.76177), V2(11.39693,  7.31673)),
        new TF(TF::defaultHorizontalCalculator( 0.44364,  0.44238, 0.044, 0.663,  0.67488), V2(11.80814,  7.87220)),
        new TF(TF::defaultHorizontalCalculator( 0.44478,  0.44364, 0.044, 0.663,  0.58912), V2(11.40607,  8.02565)),
        new TF(TF::defaultHorizontalCalculator( 0.44579,  0.44478, 0.044, 0.663,  0.50447), V2(10.30527,  8.50790)),
        new TF(TF::defaultHorizontalCalculator( 0.44667,  0.44579, 0.044, 0.663,  0.42094), V2( 4.33091,  9.39970)),
        new TF(TF::defaultHorizontalCalculator( 0.44744,  0.44667, 0.044, 0.663,  0.33854), V2( 3.72317,  9.85487)),
        new TF(TF::defaultHorizontalCalculator( 0.44807,  0.44744, 0.044, 0.663,  0.25727), V2( 3.66230, 10.42325)),
        new TF(TF::defaultHorizontalCalculator( 0.44859,  0.44807, 0.044, 0.663,  0.17709), V2( 4.05747, 11.66661)),
        new TF(TF::defaultHorizontalCalculator( 0.44897,  0.44859, 0.044, 0.663,  0.09805), V2( 3.42157, 13.63853)),
        new TF(TF::defaultHorizontalCalculator( 0.44924,  0.44897, 0.044, 0.663,  0.02013), V2( 3.33973, 13.97571)),
        new TF(TF::defaultHorizontalCalculator( 0.44938,  0.44924, 0.044, 0.663, -0.05665), V2( 4.77655, 13.80859)),
        new TF(TF::defaultHorizontalCalculator( 0.44940,  0.44938, 0.044, 0.663, -0.13234), V2( 6.38091, 14.22937)),
        new TF(TF::defaultHorizontalCalculator( 0.44929,  0.44940, 0.044, 0.663, -0.30244), V2( 6.68967, 14.82293)),
        new TF(TF::defaultHorizontalCalculator( 0.44906,  0.44929, 0.044, 0.663, -0.55295), V2( 6.38539, 15.64799)),
        new TF(TF::defaultHorizontalCalculator( 0.44870,  0.44906, 0.044, 0.663, -0.78135), V2( 5.97937, 14.53217)),
        new TF(TF::defaultHorizontalCalculator( 0.44822,  0.44870, 0.044, 0.663, -0.98763), V2( 7.01775, 12.67262)),
        new TF(TF::defaultHorizontalCalculator( 0.44762,  0.44822, 0.044, 0.663, -1.17178), V2( 4.02711, 10.69318)),
        new TF(TF::defaultHorizontalCalculator( 0.44688,  0.44762, 0.044, 0.663, -1.33383), V2( 2.64370,  8.23380)),
        new TF(TF::defaultHorizontalCalculator( 0.44604,  0.44688, 0.044, 0.663, -1.47376), V2( 2.00000,  6.82758)),
        new TF(TF::defaultHorizontalCalculator( 0.44506,  0.44604, 0.044, 0.663, -1.59156), V2( 2.58889,  6.67253)),
        new TF(TF::defaultHorizontalCalculator( 0.44396,  0.44506, 0.044, 0.663, -1.68725), V2( 2.94444,  8.39870)),
        new TF(TF::defaultHorizontalCalculator( 0.44273,  0.44396, 0.044, 0.663, -1.76082), V2( 3.45689, 10.02879)),
        new TF(TF::defaultHorizontalCalculator( 0.44139,  0.44273, 0.044, 0.663, -1.81227), V2( 2.86595, 12.82765)),
        new TF(TF::defaultHorizontalCalculator( 0.43991,  0.44139, 0.044, 0.663, -1.84160), V2( 3.66016, 12.94481)),
        new TF(TF::defaultHorizontalCalculator( 0.43831,  0.43991, 0.044, 0.663, -1.84882), V2( 3.81384, 11.99182)),
        new TF(TF::defaultHorizontalCalculator( 0.43659,  0.43831, 0.044, 0.663, -1.83392), V2( 2.98728, 10.84010)),
        new TF(TF::defaultHorizontalCalculator( 0.43475,  0.43659, 0.044, 0.663, -1.79690), V2( 3.07188,  8.58006)),
        new TF(TF::defaultHorizontalCalculator( 0.43277,  0.43475, 0.044, 0.663, -1.73776), V2( 3.04584,  6.23389)),
        new TF(TF::defaultHorizontalCalculator( 0.43069,  0.43277, 0.044, 0.663, -1.65650), V2( 3.11685,  4.57366)),
        new TF(TF::defaultHorizontalCalculator( 0.42846,  0.43069, 0.044, 0.663, -1.55313), V2( 3.85152,  2.90939)),
        new TF(TF::driftCalculator(0.13, 2, 0.78, 0.06, 0.02, 2.6), V2(2, 0))
    })},
    {"DarkDive.Reverse", new Trajectory(0, 44, LEDGE_GRAB_MODE_DURING, false, new Trajectory::Frames{
        new TF(V2(0, 0), V2(6.82229, 3.00536)),
        new TF(TF::defaultHorizontalCalculator( 0.00000,  0.00000, 0.044, 0.663,  0.00000), V2( 3.41854,  4.17136)),
        new TF(TF::defaultHorizontalCalculator( 0.00000,  0.00000, 0.044, 0.663,  0.00000), V2( 2.97136,  4.52726)),
        new TF(TF::defaultHorizontalCalculator( 0.00000,  0.00000, 0.044, 0.663,  0.00000), V2( 9.48408,  4.00385)),
        new TF(TF::defaultHorizontalCalculator( 0.00000,  0.00000, 0.044, 0.663,  0.00000), V2(10.68512,  1.69978)),
        new TF(TF::defaultHorizontalCalculator(-0.00213,  0.00000, 0.044, 0.663, -0.00087), V2(10.71249,  1.55549)),
        new TF(TF::defaultHorizontalCalculator(-0.00517, -0.00213, 0.044, 0.663, -0.00210), V2(10.73668,  1.46099)),
        new TF(TF::defaultHorizontalCalculator(-0.00638, -0.00517, 0.044, 0.663, -0.00260), V2(10.75568,  1.41198)),
        new TF(TF::defaultHorizontalCalculator(-0.00577, -0.00638, 0.044, 0.663, -0.00235), V2(10.76583,  1.40420)),
        new TF(TF::defaultHorizontalCalculator(-0.00334, -0.00577, 0.044, 0.663, -0.00136), V2(10.76215,  1.43336)),
        new TF(TF::defaultHorizontalCalculator( 0.00091, -0.00334, 0.044, 0.663,  0.00037), V2(10.73588,  1.49520)),
        new TF(TF::defaultHorizontalCalculator( 0.00699,  0.00091, 0.044, 0.663,  0.00284), V2(10.68268,  1.58543)),
        new TF(TF::defaultHorizontalCalculator(-0.01489,  0.00699, 0.044, 0.663,  0.00606), V2( 4.22097,  1.69978), new vector<double>{-1, -0.3}),
        new TF(TF::defaultHorizontalCalculator(-0.38727, -0.01489, 0.044, 0.663,  2.84533), V2( 4.28408,  1.69978)),
        new TF(TF::defaultHorizontalCalculator(-0.39113, -0.38727, 0.044, 0.663,  2.73491), V2( 3.17785,  1.69978)),
        new TF(TF::defaultHorizontalCalculator(-0.39487, -0.39113, 0.044, 0.663,  2.62560), V2( 3.78630,  1.69978)),
        new TF(TF::defaultHorizontalCalculator(-0.39849, -0.39487, 0.044, 0.663,  2.51742), V2( 3.80862,  1.69978)),
        new TF(TF::defaultHorizontalCalculator(-0.40199, -0.39849, 0.044, 0.663,  2.41035), V2( 3.81985,  2.33026)),
        new TF(TF::defaultHorizontalCalculator(-0.40536, -0.40199, 0.044, 0.663,  2.30441), V2( 3.82517,  2.26294)),
        new TF(TF::defaultHorizontalCalculator(-0.40860, -0.40536, 0.044, 0.663,  2.19959), V2( 3.82999,  2.13864)),
        new TF(TF::defaultHorizontalCalculator(-0.41172, -0.40860, 0.044, 0.663,  2.09588), V2( 3.83962,  2.01963)),
        new TF(TF::defaultHorizontalCalculator(-0.41472, -0.41172, 0.044, 0.663,  1.99331), V2( 3.85875,  1.96821)),
        new TF(TF::defaultHorizontalCalculator(-0.41759, -0.41472, 0.044, 0.663,  1.89185), V2( 3.89097,  2.04651)),
        new TF(TF::defaultHorizontalCalculator(-0.42034, -0.41759, 0.044, 0.663,  1.79151), V2( 4.19507,  2.31339)),
        new TF(TF::defaultHorizontalCalculator(-0.42297, -0.42034, 0.044, 0.663,  1.69229), V2( 4.55337,  2.69658)),
        new TF(TF::defaultHorizontalCalculator(-0.42547, -0.42297, 0.044, 0.663,  1.59420), V2( 4.77227,  3.16121)),
        new TF(TF::defaultHorizontalCalculator(-0.42784, -0.42547, 0.044, 0.663,  1.49722), V2( 4.98158,  3.66881)),
        new TF(TF::defaultHorizontalCalculator(-0.43009, -0.42784, 0.044, 0.663,  1.40436), V2( 4.86576,  4.16086)),
        new TF(TF::defaultHorizontalCalculator(-0.43222, -0.43009, 0.044, 0.663,  1.30663), V2( 4.93086,  4.59776)),
        new TF(TF::defaultHorizontalCalculator(-0.43423, -0.43222, 0.044, 0.663,  1.21302), V2( 2.00000,  4.98760)),
        new TF(TF::defaultHorizontalCalculator(-0.43610, -0.43423, 0.044, 0.663,  1.12053), V2( 2.00000,  5.33732)),
        new TF(TF::defaultHorizontalCalculator(-0.43786, -0.43610, 0.044, 0.663,  1.02916), V2( 4.16913,  5.49883)),
        new TF(TF::defaultHorizontalCalculator(-0.43949, -0.43786, 0.044, 0.663,  0.93891), V2( 3.37916,  5.78750)),
        new TF(TF::defaultHorizontalCalculator(-0.44100, -0.43949, 0.044, 0.663,  0.84977), V2( 4.20500,  6.50863)),
        new TF(TF::defaultHorizontalCalculator(-0.44238, -0.44100, 0.044, 0.663,  0.76177), V2( 2.00000,  7.31673)),
        new TF(TF::defaultHorizontalCalculator(-0.44364, -0.44238, 0.044, 0.663,  0.67488), V2( 2.00000,  7.87220)),
        new TF(TF::defaultHorizontalCalculator(-0.44478, -0.44364, 0.044, 0.663,  0.58912), V2( 2.00000,  8.02565)),
        new TF(TF::defaultHorizontalCalculator(-0.44579, -0.44478, 0.044, 0.663,  0.50447), V2( 2.00000,  8.50790)),
        new TF(TF::defaultHorizontalCalculator(-0.44667, -0.44579, 0.044, 0.663,  0.42094), V2( 4.33091,  9.39970)),
        new TF(TF::defaultHorizontalCalculator(-0.44744, -0.44667, 0.044, 0.663,  0.33854), V2( 3.72317,  9.85487)),
        new TF(TF::defaultHorizontalCalculator(-0.44807, -0.44744, 0.044, 0.663,  0.25727), V2( 3.66230, 10.42325)),
        new TF(TF::defaultHorizontalCalculator(-0.44859, -0.44807, 0.044, 0.663,  0.17709), V2( 4.05747, 11.66661)),
        new TF(TF::defaultHorizontalCalculator(-0.44897, -0.44859, 0.044, 0.663,  0.09805), V2( 3.42157, 13.63853)),
        new TF(TF::defaultHorizontalCalculator(-0.44924, -0.44897, 0.044, 0.663,  0.02013), V2( 3.33973, 13.97571)),
        new TF(TF::defaultHorizontalCalculator(-0.44938, -0.44924, 0.044, 0.663, -0.05665), V2( 4.77655, 13.80859)),
        new TF(TF::defaultHorizontalCalculator(-0.44940, -0.44938, 0.044, 0.663, -0.13234), V2( 4.04944, 14.22937)),
        new TF(TF::defaultHorizontalCalculator(-0.44929, -0.44940, 0.044, 0.663, -0.30244), V2( 5.16347, 14.82293)),
        new TF(TF::defaultHorizontalCalculator(-0.44906, -0.44929, 0.044, 0.663, -0.55295), V2( 6.22149, 15.64799)),
        new TF(TF::defaultHorizontalCalculator(-0.44870, -0.44906, 0.044, 0.663, -0.78135), V2( 6.50696, 14.53217)),
        new TF(TF::defaultHorizontalCalculator(-0.44822, -0.44870, 0.044, 0.663, -0.98763), V2( 5.79451, 12.67262)),
        new TF(TF::defaultHorizontalCalculator(-0.44762, -0.44822, 0.044, 0.663, -1.17178), V2( 4.02711, 10.69318)),
        new TF(TF::defaultHorizontalCalculator(-0.44688, -0.44762, 0.044, 0.663, -1.33383), V2( 2.64370,  8.23380)),
        new TF(TF::defaultHorizontalCalculator(-0.44604, -0.44688, 0.044, 0.663, -1.47376), V2( 2.00000,  6.82758)),
        new TF(TF::defaultHorizontalCalculator(-0.44506, -0.44604, 0.044, 0.663, -1.59156), V2( 2.58889,  6.67253)),
        new TF(TF::defaultHorizontalCalculator(-0.44396, -0.44506, 0.044, 0.663, -1.68725), V2( 2.94444,  8.39870)),
        new TF(TF::defaultHorizontalCalculator(-0.44273, -0.44396, 0.044, 0.663, -1.76082), V2( 3.45689, 10.02879)),
        new TF(TF::defaultHorizontalCalculator(-0.44139, -0.44273, 0.044, 0.663, -1.81227), V2( 2.86595, 12.82765)),
        new TF(TF::defaultHorizontalCalculator(-0.43991, -0.44139, 0.044, 0.663, -1.84160), V2( 3.66016, 12.94481)),
        new TF(TF::defaultHorizontalCalculator(-0.43831, -0.43991, 0.044, 0.663, -1.84882), V2( 3.81384, 11.99182)),
        new TF(TF::defaultHorizontalCalculator(-0.43659, -0.43831, 0.044, 0.663, -1.83392), V2( 2.98728, 10.84010)),
        new TF(TF::defaultHorizontalCalculator(-0.43475, -0.43659, 0.044, 0.663, -1.79690), V2( 3.07188,  8.58006)),
        new TF(TF::defaultHorizontalCalculator(-0.43277, -0.43475, 0.044, 0.663, -1.73776), V2( 3.04584,  6.23389)),
        new TF(TF::defaultHorizontalCalculator(-0.43069, -0.43277, 0.044, 0.663, -1.65650), V2( 3.11685,  4.57366)),
        new TF(TF::defaultHorizontalCalculator(-0.42846, -0.43069, 0.044, 0.663, -1.55313), V2( 3.85152,  2.90939)),
        new TF(TF::driftCalculator(0.13, 2, 0.78, 0.06, 0.02, 2.6), V2(2, 0))
    })},
    {"FalconKick", new Trajectory(0, 12, LEDGE_GRAB_MODE_AFTER, false, new Trajectory::Frames{
        new TF(V2(-0.31605,  0.20183), V2( 4.47041,  3.04274)),
        new TF(V2(-0.36565,  0.27723), V2( 5.03334,  6.24597)),
        new TF(V2(-0.21252,  0.33551), V2( 4.68771,  6.77937)),
        new TF(V2( 0.24607,  0.37668), V2( 4.63432,  6.64106)),
        new TF(V2( 0.24607,  0.40073), V2( 4.60378,  6.54073)),
        new TF(V2( 0.24607,  0.40766), V2( 4.59310,  6.47538)),
        new TF(V2( 0.24607,  0.39748), V2( 4.59826,  6.44247)),
        new TF(V2( 0.24607,  0.37018), V2( 4.61455,  6.43979)),
        new TF(V2( 0.24607,  0.32577), V2( 4.63691,  6.46545)),
        new TF(V2( 0.24607,  0.26424), V2( 4.66060,  6.51788)),
        new TF(V2( 0.24607,  0.18559), V2( 4.67868,  6.59574)),
        new TF(V2( 0.24607,  0.08983), V2( 4.68728,  6.69780)),
        new TF(V2( 0.24607, -0.02305), V2( 4.68022,  6.82293)),
        new TF(V2( 0.24607, -0.15304), V2( 4.31310,  6.02108)),
        new TF(V2( 0.24607, -0.30015), V2( 4.20284,  4.39322)),
        new TF(V2( 0.24607, -0.46438), V2( 4.56600,  2.97842)),
        new TF(V2( 1.22542, -3.81748), V2( 4.59141,  3.00264)),
        new TF(V2( 1.22542, -3.81748), V2( 4.58768,  2.99760)),
        new TF(V2( 1.22542, -3.81748), V2( 4.56623,  2.97099)),
        new TF(V2( 1.22542, -3.81748), V2( 4.53775,  2.93158)),
        new TF(V2( 1.22542, -3.81748), V2( 4.51244,  2.88816)),
        new TF(V2( 1.22542, -3.81748), V2( 4.50006,  2.84911)),
        new TF(V2( 1.22542, -3.81748), V2( 4.50323,  2.81308)),
        new TF(V2( 1.22542, -3.81748), V2( 4.50811,  2.77350)),
        new TF(V2( 1.22542, -3.81748), V2( 4.51366,  2.73073)),
        new TF(V2( 1.22542, -3.81748), V2( 4.51908,  2.68511)),
        new TF(V2( 1.22542, -3.81748), V2( 4.52399,  2.63698)),
        new TF(V2( 1.22542, -3.81748), V2( 4.52802,  2.58667)),
        new TF(V2( 1.22542, -3.81748), V2( 4.53086,  2.53454)),
        new TF(V2( 1.21542, -2.90000), V2( 4.65802,  2.53454)),
        new TF(V2( 1.20542, -2.90000), V2( 4.08289,  2.53454)),
        new TF(V2( 1.19542, -2.90000), V2( 3.34848,  2.53454)),
        new TF(V2( 1.18542, -2.90000), V2( 2.71397,  2.53454)),
        new TF(V2( 1.17542, -2.90000), V2( 2.41572,  2.53454)),
        new TF(V2( 1.16542, -2.90000), V2( 2.65804,  2.53454)),
        new TF(V2( 1.15542, -2.90000), V2( 2.97446,  2.53454)),
        new TF(V2( 1.14542, -2.90000), V2( 3.01314,  2.53454)),
        new TF(V2( 1.13542, -2.90000), V2( 2.86655,  2.53454)),
        new TF(V2( 1.12542, -2.90000), V2( 2.78992,  0.77500)),
        new TF(V2( 1.11542, -2.90000), V2( 2.78710,  1.90425)),
        new TF(V2( 1.10542, -2.90000), V2( 2.87750,  2.67024)),
        new TF(V2( 1.09542, -2.90000), V2( 2.89241,  2.57416)),
        new TF(V2( 1.08542, -2.90000), V2( 2.95931,  0.00000)),
        new TF(V2( 1.07542, -2.90000), V2( 2.94094,  0.00000)),
        new TF(V2( 1.06542, -2.90000), V2( 3.07280,  2.57142)),
        new TF(V2( 1.05542, -2.90000), V2( 3.67239,  3.36185)),
        new TF(V2( 1.04542, -2.90000), V2( 4.00201,  3.54652)),
        new TF(V2( 1.03542, -2.90000), V2( 4.02197,  4.01226)),
        new TF(V2( 1.02542, -2.90000), V2( 3.82286,  2.51706)),
        new TF(V2( 1.01542, -2.90000), V2( 3.80428,  2.04388)),
        new TF(V2( 1.00542, -2.90000), V2( 3.90124,  1.68863)),
        new TF(V2( 0.99542, -2.90000), V2( 4.24667,  1.48116)),
        new TF(V2( 0.98542, -2.90000), V2( 4.58267,  1.77460)),
        new TF(V2( 0.97542, -2.90000), V2( 4.79899,  2.27834)),
        new TF(V2( 0.96542, -2.90000), V2( 4.89793,  2.78949)),
        new TF(V2( 0.95542, -2.90000), V2( 4.72794,  2.98927)),
        new TF(V2( 0.94542, -2.90000), V2( 4.32374,  2.65326)),
        new TF(V2( 0.93542, -2.90000), V2( 3.94088,  2.23287))
    })},
    {"WizardsFoot", new Trajectory(0, 12, LEDGE_GRAB_MODE_AFTER, false, new Trajectory::Frames{
        new TF(V2(-0.35189,  0.22472), V2( 6.50301,  3.01820)),
        new TF(V2(-0.40711,  0.30867), V2( 5.89899,  6.62870)),
        new TF(V2(-0.23662,  0.37356), V2( 4.92789,  6.44625)),
        new TF(V2( 0.27398,  0.41940), V2( 4.83740,  6.32632)),
        new TF(V2( 0.27398,  0.44617), V2( 4.82417,  6.24238)),
        new TF(V2( 0.27398,  0.45389), V2( 4.83505,  6.19056)),
        new TF(V2( 0.27398,  0.44256), V2( 4.85714,  6.16749)),
        new TF(V2( 0.27398,  0.41216), V2( 4.87964,  6.17036)),
        new TF(V2( 0.27398,  0.36271), V2( 4.89534,  6.19673)),
        new TF(V2( 0.27398,  0.29420), V2( 4.90103,  6.24451)),
        new TF(V2( 0.27398,  0.20664), V2( 4.89700,  6.31183)),
        new TF(V2( 0.27398,  0.10002), V2( 4.90068,  6.39701)),
        new TF(V2( 0.27398, -0.02566), V2( 4.89714,  6.49839)),
        new TF(V2( 0.27398, -0.17040), V2( 4.69592,  5.71409)),
        new TF(V2( 0.27398, -0.33419), V2( 4.50022,  4.75557)),
        new TF(V2( 0.27398, -0.51704), V2( 3.99406,  3.96149)),
        new TF(V2( 1.36439, -3.24753), V2( 3.96980,  3.94133)),
        new TF(V2( 1.36439, -3.24753), V2( 3.94554,  3.91728)),
        new TF(V2( 1.36439, -3.24753), V2( 3.92132,  3.88939)),
        new TF(V2( 1.36439, -3.24753), V2( 3.89713,  3.85770)),
        new TF(V2( 1.36439, -3.24753), V2( 3.87300,  3.82227)),
        new TF(V2( 1.36439, -3.24753), V2( 3.84897,  3.87314)),
        new TF(V2( 1.36439, -3.24753), V2( 3.82506,  3.74035)),
        new TF(V2( 1.36439, -3.24753), V2( 3.80128,  3.69395)),
        new TF(V2( 1.36439, -3.24753), V2( 3.77766,  3.64400)),
        new TF(V2( 1.36439, -3.24753), V2( 3.75423,  3.59053)),
        new TF(V2( 1.36439, -3.24753), V2( 3.73100,  3.53360)),
        new TF(V2( 1.36439, -3.24753), V2( 3.70798,  3.47325)),
        new TF(V2( 1.36439, -3.24753), V2( 3.68521,  3.40953)),
        new TF(V2( 1.34439, -2.00000), V2( 4.75240,  3.40953)),
        new TF(V2( 1.32439, -2.00000), V2( 4.19373,  3.40953)),
        new TF(V2( 1.30439, -2.00000), V2( 3.51887,  3.40953)),
        new TF(V2( 1.28439, -2.00000), V2( 3.11580,  3.40953)),
        new TF(V2( 1.26439, -2.00000), V2( 2.79090,  3.40953)),
        new TF(V2( 1.24439, -2.00000), V2( 2.91934,  3.40953)),
        new TF(V2( 1.22439, -2.00000), V2( 3.43505,  3.40953)),
        new TF(V2( 1.20439, -2.00000), V2( 3.46271,  3.40953)),
        new TF(V2( 1.18439, -2.00000), V2( 3.55484,  3.40953)),
        new TF(V2( 1.16439, -2.00000), V2( 3.43090,  0.47813)),
        new TF(V2( 1.14439, -2.00000), V2( 3.66360,  2.13990)),
        new TF(V2( 1.12439, -2.00000), V2( 3.70756,  2.35260)),
        new TF(V2( 1.10439, -2.00000), V2( 3.59766,  2.07626)),
        new TF(V2( 1.08439, -2.00000), V2( 3.61294,  0.00000)),
        new TF(V2( 1.06439, -2.00000), V2( 3.66642,  0.00000)),
        new TF(V2( 1.04439, -2.00000), V2( 3.67429,  2.80553)),
        new TF(V2( 1.02439, -2.00000), V2( 4.07691,  3.74294)),
        new TF(V2( 1.00439, -2.00000), V2( 4.40622,  3.94857)),
        new TF(V2( 0.98439, -2.00000), V2( 4.49535,  4.44210)),
        new TF(V2( 0.96439, -2.00000), V2( 4.28782,  2.76543)),
        new TF(V2( 0.94439, -2.00000), V2( 4.29752,  2.09176)),
        new TF(V2( 0.92439, -2.00000), V2( 4.45649,  1.30682)),
        new TF(V2( 0.90439, -2.00000), V2( 4.76670,  4.06219)),
        new TF(V2( 0.88439, -2.00000), V2( 6.71039,  1.31285)),
        new TF(V2( 0.86439, -2.00000), V2( 7.00510,  1.74813)),
        new TF(V2( 0.84439, -2.00000), V2( 7.26999,  2.18660)),
        new TF(V2( 0.82439, -2.00000), V2( 7.17744,  2.56257)),
        new TF(V2( 0.80439, -2.00000), V2( 6.96919,  2.36125)),
        new TF(V2( 0.78439, -2.00000), V2( 4.73248,  2.18873))
    })},
    {"RaptorBoost", new Trajectory(0, 30, LEDGE_GRAB_MODE_AFTER, false, new Trajectory::Frames{
        new TF(V2( 0.00000,  0.00000), V2( 3.78725,  2.73032)),
        new TF(V2( 0.00000,  0.00000), V2( 8.02988,  2.73032)),
        new TF(V2( 0.00000,  0.00000), V2( 8.15715,  2.73032)),
        new TF(V2( 0.00000,  0.00000), V2( 6.91919,  2.73032)),
        new TF(V2( 0.00000,  0.00000), V2( 6.86819,  1.90617)),
        new TF(V2( 0.00000,  0.00000), V2( 6.84862,  2.08945)),
        new TF(V2( 0.00000,  0.00000), V2( 6.79689,  2.25625)),
        new TF(V2( 0.00000,  0.00000), V2( 6.72339,  2.40133)),
        new TF(V2( 0.00000,  0.00000), V2( 6.62900,  2.53273)),
        new TF(V2( 0.00000,  0.00000), V2( 6.53914,  2.66314)),
        new TF(V2( 0.00000,  0.00000), V2( 6.49925,  2.63678)),
        new TF(V2( 0.00000,  0.00000), V2( 6.54384,  2.61777)),
        new TF(V2( 0.00000,  0.00000), V2( 6.68341,  2.59514)),
        new TF(V2( 0.00000,  0.00000), V2( 6.93004,  2.55945)),
        new TF(V2( 0.00000,  0.00000), V2( 7.31392,  2.50366)),
        new TF(V2( 2.27937,  0.00000), V2( 7.25902,  2.57597)),
        new TF(V2( 1.82957,  0.00000), V2( 7.24419,  2.20474)),
        new TF(V2( 1.65988,  0.00000), V2( 7.36293,  2.21038)),
        new TF(V2( 1.77032,  0.00000), V2(10.45380,  3.59588)),
        new TF(V2( 2.16086,  0.00000), V2(10.73952,  3.68277)),
        new TF(V2( 2.40854,  0.00000), V2(10.86107,  4.10989)),
        new TF(V2( 2.32754,  0.00000), V2(11.01353,  4.10979)),
        new TF(V2( 2.24791,  0.00000), V2(11.12446,  3.95215)),
        new TF(V2( 2.16967,  0.00000), V2(11.23960,  3.82033)),
        new TF(V2( 2.09282,  0.00000), V2(11.37151,  3.79396)),
        new TF(V2( 2.01735,  0.00000), V2(11.50796,  3.89310)),
        new TF(V2( 1.94326,  0.00000), V2(11.61216,  4.07447)),
        new TF(V2( 1.87056,  0.00000), V2(11.67870,  4.27964)),
        new TF(V2( 1.79924,  0.00000), V2(11.71288,  4.43861)),
        new TF(V2( 1.72931, -0.05000), V2(11.71819,  4.52493)),
        new TF(V2( 1.66076, -0.10000), V2(11.69933,  4.51804)),
        new TF(V2( 1.59359, -0.15000), V2(11.64420,  4.38906)),
        new TF(V2( 1.52782, -0.20000), V2(11.53226,  4.11228)),
        new TF(V2( 1.46342, -0.25000), V2(11.32838,  3.67184)),
        new TF(V2( 1.40040, -0.30000), V2(10.97910,  3.07395)),
        new TF(V2( 1.33878, -0.35000), V2( 9.81707,  1.15201)),
        new TF(V2( 1.27853, -0.40000), V2(10.89488,  0.00000)),
        new TF(V2( 1.21968, -0.45000), V2(12.67571,  0.00000)),
        new TF(V2( 1.16220, -0.50000), V2(12.82780,  0.00000)),
        new TF(V2( 1.10611, -0.55000), V2(12.31119,  1.29880)),
        new TF(V2( 1.05141, -0.60000), V2(10.33372,  0.23924)),
        new TF(V2( 0.99808, -0.65000), V2( 7.06634,  0.00000)),
        new TF(V2( 0.94615, -0.70000), V2( 4.72509,  0.00000)),
        new TF(V2( 0.89559, -0.75000), V2( 4.91050,  0.22355)),
        new TF(V2( 0.84642, -0.80000), V2( 6.33263,  0.73548)),
        new TF(V2( 0.79864, -0.85000), V2( 6.42918,  1.10453)),
        new TF(V2( 0.75225, -0.90000), V2( 6.46437,  1.39063)),
        new TF(V2( 0.70722, -0.95000), V2( 6.43492,  1.69522)),
        new TF(V2( 0.66359, -1.00000), V2( 4.89017,  2.04250)),
        new TF(V2( 0.62135, -1.05000), V2( 4.72839,  2.41800)),
        new TF(V2( 0.58048, -1.10000), V2( 4.76573,  2.73204)),
        new TF(V2( 0.54100, -1.15000), V2( 7.33180,  2.95683)),
        new TF(V2( 0.50291, -1.20000), V2( 8.29927,  3.07652)),
        new TF(V2( 0.46619, -1.25000), V2( 9.15936,  2.80036)),
        new TF(V2( 0.43089, -1.30000), V2( 9.85410,  2.41690)),
        new TF(V2( 0.39694, -1.35000), V2(10.34127,  2.11477)),
        new TF(V2( 0.36437, -1.40000), V2(10.61197,  1.90619)),
        new TF(V2( 0.33320, -1.45000), V2(10.58328,  1.79178)),
        new TF(V2( 0.30343, -1.50000), V2(10.05034,  1.81489)),
        new TF(V2( 0.27500, -1.55000), V2( 8.81828,  0.27198)),
        new TF(V2( 0.24800, -1.60000), V2( 7.25484,  0.00000)),
        new TF(V2( 0.22235, -1.65000), V2( 4.51528,  0.00000)),
        new TF(V2( 0.19812, -1.70000), V2( 2.74831,  0.00000)),
        new TF(V2( 0.17523, -1.75000), V2( 2.66676,  0.00000)),
        new TF(V2( 0.15378, -1.80000), V2( 3.92780,  0.00000)),
        new TF(V2( 0.13364, -1.85000), V2( 3.12574,  0.00000)),
        new TF(V2( 0.11496, -1.90000), V2( 3.30847,  1.60612)),
        new TF(V2( 0.09761, -1.95000), V2( 4.24731,  3.62517)),
        new TF(V2( 0.08167, -2.00000), V2( 5.25221,  3.63011)),
        new TF(V2( 0.06713, -2.05000), V2( 5.85935,  3.86222)),
        new TF(V2( 0.05394, -2.10000), V2( 6.29140,  4.24495)),
        new TF(V2( 0.04214, -2.15000), V2( 6.60296,  3.87188)),
        new TF(V2( 0.03175, -2.20000), V2( 6.86433,  3.49290)),
        new TF(V2( 0.02271, -2.25000), V2( 7.14101,  3.17443)),
        new TF(V2( 0.15090, -2.30000), V2( 4.95147,  2.93018)),
        new TF(V2( 0.00881, -2.35000), V2( 4.80810,  2.78490)),
        new TF(V2( 0.00396, -2.40000), V2( 4.80127,  2.75246)),
        new TF(V2( 0.00046, -2.45000), V2( 4.64814,  2.66660)),
        new TF(V2(-0.00165, -2.50000), V2( 4.34089,  2.51716)),
        new TF(TF::driftCalculator(0.13, 2.9, 1.12, 0.06, 0.01, 2.9), V2(2, 0))
    })},
    {"GerudoDragon", new Trajectory(0, 30, LEDGE_GRAB_MODE_AFTER, false, new Trajectory::Frames{
        new TF(V2( 0.00000,  0.00000), V2( 6.28461,  4.76120)),
        new TF(V2( 0.00000,  0.00000), V2( 9.25500,  4.76120)),
        new TF(V2( 0.00000,  0.00000), V2(10.62864,  4.76120)),
        new TF(V2( 0.00000,  0.00000), V2(10.10815,  4.76120)),
        new TF(V2( 0.00000,  0.00000), V2(10.19148,  1.73749)),
        new TF(V2( 0.00000,  0.00000), V2(10.24401,  1.95246)),
        new TF(V2( 0.00000,  0.00000), V2(10.33289,  2.14644)),
        new TF(V2( 0.00000,  0.00000), V2(10.43704,  2.31315)),
        new TF(V2( 0.00000,  0.00000), V2(10.55499,  2.45775)),
        new TF(V2( 0.00000,  0.00000), V2(10.68807,  2.48404)),
        new TF(V2( 0.00000,  0.00000), V2(10.84002,  2.41684)),
        new TF(V2( 0.00000,  0.00000), V2(11.01596,  2.35403)),
        new TF(V2( 0.00000,  0.00000), V2(11.22028,  2.28738)),
        new TF(V2( 0.00000,  0.00000), V2(11.43668,  2.21111)),
        new TF(V2( 0.00000,  0.00000), V2(11.64652,  2.12332)),
        new TF(V2( 2.69842,  0.00000), V2(11.11872,  2.42337)),
        new TF(V2( 2.35818,  0.00000), V2( 9.93040,  1.72649)),
        new TF(V2( 2.08897,  0.00000), V2(10.38019,  1.54572)),
        new TF(V2( 1.89079,  0.00000), V2(11.91584,  3.46842)),
        new TF(V2( 1.76365,  0.00000), V2(11.71297,  2.94803)),
        new TF(V2( 1.69797,  0.00000), V2(11.27635,  3.12341)),
        new TF(V2( 1.64690,  0.00000), V2(11.17303,  3.15848)),
        new TF(V2( 1.59660,  0.00000), V2(11.25758,  3.28909)),
        new TF(V2( 1.54707,  0.00000), V2(11.45245,  3.48873)),
        new TF(V2( 1.49831,  0.00000), V2(11.67767,  3.74188)),
        new TF(V2( 1.45032,  0.00000), V2(11.85925,  4.03060)),
        new TF(V2( 1.40310,  0.00000), V2(11.97536,  4.32455)),
        new TF(V2( 1.35665,  0.00000), V2(12.05534,  4.58671)),
        new TF(V2( 1.31096,  0.00000), V2(12.11075,  4.78293)),
        new TF(V2( 1.26604, -0.05000), V2(12.15604,  4.87871)),
        new TF(V2( 1.22190, -0.10000), V2(12.20264,  4.83830)),
        new TF(V2( 1.17852, -0.15000), V2(12.24345,  4.60056)),
        new TF(V2( 1.13591, -0.20000), V2(12.26079,  4.14338)),
        new TF(V2( 1.09407, -0.25000), V2(12.22701,  3.48653)),
        new TF(V2( 1.05300, -0.30000), V2(12.09663,  2.65147)),
        new TF(V2( 1.01269, -0.35000), V2(10.94594,  0.19970)),
        new TF(V2( 0.97316, -0.40000), V2(13.00554,  0.00000)),
        new TF(V2( 0.93439, -0.45000), V2(14.81137,  0.00000)),
        new TF(V2( 0.89640, -0.50000), V2(15.32357,  0.00000)),
        new TF(V2( 0.85917, -0.55000), V2(14.49341,  1.60838)),
        new TF(V2( 0.82271, -0.60000), V2(11.81155,  0.01612)),
        new TF(V2( 0.78702, -0.65000), V2( 7.91777,  0.00000)),
        new TF(V2( 0.75210, -0.70000), V2( 7.51830,  0.51486)),
        new TF(V2( 0.71795, -0.75000), V2( 7.76823,  1.10952)),
        new TF(V2( 0.68456, -0.80000), V2( 7.94286,  1.49479)),
        new TF(V2( 0.65195, -0.85000), V2( 8.04107,  1.79939)),
        new TF(V2( 0.62010, -0.90000), V2( 8.07828,  2.09640)),
        new TF(V2( 0.58902, -0.95000), V2( 8.03763,  2.36981)),
        new TF(V2( 0.55872, -1.00000), V2( 7.90131,  2.59566)),
        new TF(V2( 0.52917, -1.05000), V2( 7.65465,  2.74120)),
        new TF(V2( 0.50040, -1.10000), V2( 7.29015,  2.76871)),
        new TF(V2( 0.47240, -1.15000), V2( 7.61357,  2.64337)),
        new TF(V2( 0.44517, -1.20000), V2( 9.03131,  2.33197)),
        new TF(V2( 0.41870, -1.25000), V2(10.36513,  1.85428)),
        new TF(V2( 0.39301, -1.30000), V2(11.51918,  1.28729)),
        new TF(V2( 0.36809, -1.35000), V2(12.37268,  0.73009)),
        new TF(V2( 0.34391, -1.40000), V2(12.91016,  0.37558)),
        new TF(V2( 0.32053, -1.45000), V2(13.11552,  0.44942)),
        new TF(V2( 0.29792, -1.50000), V2(12.81618,  1.12567)),
        new TF(V2( 0.27605, -1.55000), V2(11.79509,  1.56517)),
        new TF(V2( 0.25499, -1.60000), V2(10.36684,  0.00000)),
        new TF(V2( 0.23466, -1.65000), V2( 8.20686,  0.00000)),
        new TF(V2( 0.21513, -1.70000), V2( 4.67139,  0.00000)),
        new TF(V2( 0.19633, -1.75000), V2( 4.64267,  0.00000)),
        new TF(V2( 0.17835, -1.80000), V2( 4.12861,  0.00000)),
        new TF(V2( 0.16108, -1.85000), V2( 3.98105,  0.00000)),
        new TF(V2( 0.14463, -1.90000), V2( 3.78680,  0.00000)),
        new TF(V2( 0.12893, -1.95000), V2( 4.19701,  3.24619)),
        new TF(V2( 0.11399, -2.00000), V2( 5.55334,  3.42772)),
        new TF(V2( 0.09983, -2.05000), V2( 6.94489,  3.68501)),
        new TF(V2( 0.08644, -2.10000), V2( 7.96449,  4.07552)),
        new TF(V2( 0.07380, -2.15000), V2( 8.69717,  3.99019)),
        new TF(V2( 0.06195, -2.20000), V2( 9.15205,  3.54180)),
        new TF(V2( 0.05086, -2.25000), V2( 9.44041,  3.16446)),
        new TF(V2( 0.04055, -2.30000), V2( 9.65689,  2.86761)),
        new TF(V2( 0.03098, -2.35000), V2( 9.83653,  2.67162)),
        new TF(V2( 0.02222, -2.40000), V2( 9.91006,  2.58936)),
        new TF(V2( 0.01419, -2.45000), V2( 9.76720,  2.45690)),
        new TF(V2( 0.00695, -2.50000), V2( 9.41476,  2.26749)),
        new TF(TF::driftCalculator(0.13, 2, 0.78, 0.06, 0.02, 2.6), V2(2, 0))
    })},
    {"FireFox", new Trajectory(42, 78, LEDGE_GRAB_MODE_ALWAYS, true, new Trajectory::Frames{
        new TF(TF::convergeHorizontalCalculator(0.8, 0.02, 0,  0.000), V2(2.00000, 4.26627)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0,  0.000), V2(2.00000, 5.18958)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0,  0.000), V2(2.00000, 5.80825)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0,  0.000), V2(2.00000, 5.53235)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0,  0.000), V2(2.00000, 5.34966)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0,  0.000), V2(2.00000, 4.91772)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0,  0.000), V2(2.00000, 4.54156)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0,  0.000), V2(2.00000, 4.32345)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0,  0.000), V2(2.00000, 4.31181)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0,  0.000), V2(2.00000, 4.35564)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0,  0.000), V2(2.00000, 4.40383)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0,  0.000), V2(2.00000, 4.38403)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0,  0.000), V2(2.00000, 4.34747)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0,  0.000), V2(2.00000, 4.32854)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0,  0.000), V2(2.00000, 4.32772)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0, -0.015), V2(2.00000, 4.34386)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0, -0.030), V2(2.00000, 4.35088)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0, -0.045), V2(2.00000, 4.34066)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0, -0.060), V2(2.00000, 4.31133)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0, -0.075), V2(2.00000, 4.29350)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0, -0.090), V2(2.00000, 4.29494)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0, -0.105), V2(2.00000, 4.31026)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0, -0.120), V2(2.00000, 4.31902)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0, -0.135), V2(2.00000, 4.31316)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0, -0.150), V2(2.00000, 4.29150)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0, -0.165), V2(2.00000, 4.27720)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0, -0.180), V2(2.00000, 4.27565)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0, -0.195), V2(2.00000, 4.28283)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0, -0.210), V2(2.00000, 4.28700)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0, -0.225), V2(2.00000, 4.28126)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0, -0.240), V2(2.00000, 4.26373)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0, -0.255), V2(2.00000, 4.25422)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0, -0.270), V2(2.00000, 4.25768)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0, -0.285), V2(2.00000, 4.28341)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0, -0.300), V2(2.00000, 4.36911)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0, -0.315), V2(2.00000, 4.79478)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0, -0.330), V2(2.00000, 4.89193)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0, -0.345), V2(2.00000, 4.67149)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0, -0.360), V2(2.00000, 4.63289)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0, -0.375), V2(2.00000, 3.57449)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0, -0.390), V2(2.00000, 2.32137)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0, -0.405), V2(3.42337, 2.04703)),
        new TF(TF::angleCalculator(3.8), V2(2, 0)),
        new TF(TF::repeatCalculator(), V2(2, 0)),
        new TF(TF::repeatCalculator(), V2(2, 0)),
        new TF(TF::repeatCalculator(), V2(2, 0)),
        new TF(TF::repeatCalculator(), V2(2, 0)),
        new TF(TF::addCalculator(-0.1), V2(2, 0)),
        new TF(TF::addCalculator(-0.1), V2(2, 0)),
        new TF(TF::addCalculator(-0.1), V2(2, 0)),
        new TF(TF::addCalculator(-0.1), V2(2, 0)),
        new TF(TF::addCalculator(-0.1), V2(2, 0)),
        new TF(TF::addCalculator(-0.1), V2(2, 0)),
        new TF(TF::addCalculator(-0.1), V2(2, 0)),
        new TF(TF::addCalculator(-0.1), V2(2, 0)),
        new TF(TF::addCalculator(-0.1), V2(2, 0)),
        new TF(TF::addCalculator(-0.1), V2(2, 0)),
        new TF(TF::addCalculator(-0.1), V2(2, 0)),
        new TF(TF::addCalculator(-0.1), V2(2, 0)),
        new TF(TF::addCalculator(-0.1), V2(2, 0)),
        new TF(TF::addCalculator(-0.1), V2(2, 0)),
        new TF(TF::addCalculator(-0.1), V2(2, 0)),
        new TF(TF::addCalculator(-0.1), V2(2, 0)),
        new TF(TF::addCalculator(-0.1), V2(2, 0)),
        new TF(TF::addCalculator(-0.1), V2(2, 0)),
        new TF(TF::addCalculator(-0.1), V2(2, 0)),
        new TF(TF::addCalculator(-0.1), V2(2, 0)),
        new TF(TF::addCalculator(-0.1), V2(2, 0)),
        new TF(TF::addCalculator(-0.1), V2(2, 0)),
        new TF(TF::addCalculator(-0.1), V2(2, 0)),
        new TF(TF::addCalculator(-0.1), V2(2, 0)),
        new TF(TF::addCalculator(-0.1), V2(2, 0)),
        new TF(TF::driftCalculator(0.23, 2.8, 0.83, 0.08, 0.02, 3.4), V2(4.00951, 2.49287)),
        new TF(TF::driftCalculator(0.23, 2.8, 0.83, 0.08, 0.02, 3.4), V2(3.16311, 3.21647)),
        new TF(TF::driftCalculator(0.23, 2.8, 0.83, 0.08, 0.02, 3.4), V2(2.00000, 3.29348)),
        new TF(TF::driftCalculator(0.23, 2.8, 0.83, 0.08, 0.02, 3.4), V2(2.00000, 2.27059)),
        new TF(TF::driftCalculator(0.23, 2.8, 0.83, 0.08, 0.02, 3.4), V2(2.00000, 1.57691)),
        new TF(TF::driftCalculator(0.23, 2.8, 0.83, 0.08, 0.02, 3.4), V2(2.00000, 1.90824)),
        new TF(TF::driftCalculator(0.23, 2.8, 0.83, 0.08, 0.02, 3.4), V2(2.00000, 1.52977)),
        new TF(TF::driftCalculator(0.23, 2.8, 0.83, 0.08, 0.02, 3.4), V2(2.00000, 1.45309)),
        new TF(TF::driftCalculator(0.23, 2.8, 0.83, 0.08, 0.02, 3.4), V2(2.00000, 1.83273)),
        new TF(TF::driftCalculator(0.23, 2.8, 0.83, 0.08, 0.02, 3.4), V2(2.00000, 2.54185)),
        new TF(TF::driftCalculator(0.23, 2.8, 0.83, 0.08, 0.02, 3.4), V2(2.00000, 3.13248)),
        new TF(TF::driftCalculator(0.23, 2.8, 0.83, 0.08, 0.02, 3.4), V2(2.00000, 2.80453)),
        new TF(TF::driftCalculator(0.23, 2.8, 0.83, 0.08, 0.02, 3.4), V2(2.00000, 2.49725)),
        new TF(TF::driftCalculator(0.23, 2.8, 0.83, 0.08, 0.02, 3.4), V2(2.00000, 2.28819)),
        new TF(TF::driftCalculator(0.23, 2.8, 0.83, 0.08, 0.02, 3.4), V2(2.00000, 2.09543)),
        new TF(TF::driftCalculator(0.23, 2.8, 0.83, 0.08, 0.02, 3.4), V2(2.00000, 1.76834)),
        new TF(TF::driftCalculator(0.23, 2.8, 0.83, 0.08, 0.02, 3.4), V2(2.00000, 1.59851)),
        new TF(TF::driftCalculator(0.23, 2.8, 0.83, 0.08, 0.02, 3.4), V2(2.00000, 0.79139)),
        new TF(TF::driftCalculator(0.23, 2.8, 0.83, 0.08, 0.02, 3.4), V2(2.14488, 0.00000)),
        new TF(TF::driftCalculator(0.23, 2.8, 0.83, 0.08, 0.02, 3.4), V2(2.70596, 0.00000)),
        new TF(TF::driftCalculator(0.23, 2.8, 0.83, 0.08, 0.02, 3.4), V2(2.00000, 0.00000))
    })},
    {"FireBird", new Trajectory(42, 70, LEDGE_GRAB_MODE_ALWAYS, true, new Trajectory::Frames{
        new TF(TF::convergeHorizontalCalculator(0.8, 0.02, 0,  0.000), V2(2.00000, 4.88859)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0,  0.000), V2(2.00000, 5.94628)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0,  0.000), V2(2.12389, 6.65456)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0,  0.000), V2(2.07417, 6.33949)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0,  0.000), V2(2.00000, 6.13013)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0,  0.000), V2(2.00000, 5.63678)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0,  0.000), V2(2.00000, 5.20667)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0,  0.000), V2(2.00000, 4.95706)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0,  0.000), V2(2.00000, 4.94419)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0,  0.000), V2(2.00000, 4.99453)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0,  0.000), V2(2.00000, 5.04981)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0,  0.000), V2(2.00000, 5.02734)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0,  0.000), V2(2.00000, 4.98535)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0,  0.000), V2(2.00000, 4.96371)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0,  0.000), V2(2.00000, 4.96280)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0, -0.016), V2(2.00000, 4.98120)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0, -0.032), V2(2.00000, 4.98924)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0, -0.048), V2(2.00000, 4.97760)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0, -0.064), V2(2.00000, 4.94403)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0, -0.080), V2(2.00000, 4.92355)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0, -0.096), V2(2.00000, 4.92522)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0, -0.112), V2(2.00000, 4.94272)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0, -0.128), V2(2.00000, 4.95287)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0, -0.144), V2(2.00000, 4.94634)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0, -0.160), V2(2.00000, 4.92170)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0, -0.176), V2(2.00000, 4.90535)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0, -0.192), V2(2.00000, 4.90359)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0, -0.208), V2(2.00000, 4.91172)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0, -0.224), V2(2.00000, 4.91652)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0, -0.240), V2(2.00000, 4.91006)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0, -0.256), V2(2.00000, 4.89011)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0, -0.272), V2(2.00000, 4.87927)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0, -0.288), V2(2.00000, 4.88337)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0, -0.304), V2(2.00000, 4.91299)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0, -0.320), V2(2.00000, 5.01128)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0, -0.336), V2(2.00000, 5.49743)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0, -0.352), V2(2.00000, 5.60563)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0, -0.368), V2(2.00000, 5.35302)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0, -0.384), V2(2.00000, 5.30878)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0, -0.400), V2(2.00000, 4.09591)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0, -0.416), V2(2.00000, 2.66004)),
        new TF(TF::convergeHorizontalCalculator(1.0, 0.02, 0, -0.432), V2(3.69668, 2.34544)),
        new TF(TF::angleCalculator(4.2), V2(2, 0)),
        new TF(TF::repeatCalculator(), V2(2, 0)),
        new TF(TF::repeatCalculator(), V2(2, 0)),
        new TF(TF::addCalculator(-0.17), V2(2, 0)),
        new TF(TF::addCalculator(-0.17), V2(2, 0)),
        new TF(TF::addCalculator(-0.17), V2(2, 0)),
        new TF(TF::addCalculator(-0.17), V2(2, 0)),
        new TF(TF::addCalculator(-0.17), V2(2, 0)),
        new TF(TF::addCalculator(-0.17), V2(2, 0)),
        new TF(TF::addCalculator(-0.17), V2(2, 0)),
        new TF(TF::addCalculator(-0.17), V2(2, 0)),
        new TF(TF::addCalculator(-0.17), V2(2, 0)),
        new TF(TF::addCalculator(-0.17), V2(2, 0)),
        new TF(TF::addCalculator(-0.17), V2(2, 0)),
        new TF(TF::addCalculator(-0.17), V2(2, 0)),
        new TF(TF::addCalculator(-0.17), V2(2, 0)),
        new TF(TF::addCalculator(-0.17), V2(2, 0)),
        new TF(TF::addCalculator(-0.17), V2(2, 0)),
        new TF(TF::addCalculator(-0.17), V2(2, 0)),
        new TF(TF::addCalculator(-0.17), V2(2, 0)),
        new TF(TF::addCalculator(-0.17), V2(2, 0)),
        new TF(TF::addCalculator(-0.17), V2(2, 0)),
        new TF(TF::driftCalculator(0.17, 3.1, 0.83, 0.07, 0.02, 3.5), V2(4.22708, 2.85620)),
        new TF(TF::driftCalculator(0.17, 3.1, 0.83, 0.07, 0.02, 3.5), V2(4.39175, 4.26080)),
        new TF(TF::driftCalculator(0.17, 3.1, 0.83, 0.07, 0.02, 3.5), V2(2.60956, 2.43257)),
        new TF(TF::driftCalculator(0.17, 3.1, 0.83, 0.07, 0.02, 3.5), V2(2.00000, 2.15451)),
        new TF(TF::driftCalculator(0.17, 3.1, 0.83, 0.07, 0.02, 3.5), V2(2.06231, 1.91264)),
        new TF(TF::driftCalculator(0.17, 3.1, 0.83, 0.07, 0.02, 3.5), V2(2.00000, 2.18654)),
        new TF(TF::driftCalculator(0.17, 3.1, 0.83, 0.07, 0.02, 3.5), V2(2.00000, 1.75287)),
        new TF(TF::driftCalculator(0.17, 3.1, 0.83, 0.07, 0.02, 3.5), V2(2.00000, 1.66501)),
        new TF(TF::driftCalculator(0.17, 3.1, 0.83, 0.07, 0.02, 3.5), V2(2.00000, 2.10001)),
        new TF(TF::driftCalculator(0.17, 3.1, 0.83, 0.07, 0.02, 3.5), V2(2.00000, 2.91254)),
        new TF(TF::driftCalculator(0.17, 3.1, 0.83, 0.07, 0.02, 3.5), V2(2.19424, 3.58929)),
        new TF(TF::driftCalculator(0.17, 3.1, 0.83, 0.07, 0.02, 3.5), V2(2.24217, 3.21381)),
        new TF(TF::driftCalculator(0.17, 3.1, 0.83, 0.07, 0.02, 3.5), V2(2.17722, 2.86174)),
        new TF(TF::driftCalculator(0.17, 3.1, 0.83, 0.07, 0.02, 3.5), V2(2.00401, 2.62224)),
        new TF(TF::driftCalculator(0.17, 3.1, 0.83, 0.07, 0.02, 3.5), V2(2.00000, 2.39804)),
        new TF(TF::driftCalculator(0.17, 3.1, 0.83, 0.07, 0.02, 3.5), V2(2.00000, 2.02351)),
        new TF(TF::driftCalculator(0.17, 3.1, 0.83, 0.07, 0.02, 3.5), V2(2.00000, 1.82715)),
        new TF(TF::driftCalculator(0.17, 3.1, 0.83, 0.07, 0.02, 3.5), V2(2.00000, 0.90439)),
        new TF(TF::driftCalculator(0.17, 3.1, 0.83, 0.07, 0.02, 3.5), V2(2.37942, 0.00000)),
        new TF(TF::driftCalculator(0.17, 3.1, 0.83, 0.07, 0.02, 3.5), V2(2.96388, 0.00000)),
        new TF(TF::driftCalculator(0.17, 3.1, 0.83, 0.07, 0.02, 3.5), V2(2.00000, 0.00000))
    })},
    {"FoxIllusion.Full", new Trajectory(0, 15, LEDGE_GRAB_MODE_ALWAYS, false, new Trajectory::Frames{
        new TF(TF::convergeHorizontalCalculator(2.0 / 3.0, 0.05, 0,  0.00000), V2(2.00000, 3.50615)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.30477, 2.82410)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.43458, 2.08694)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.28246, 1.36353)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.33513, 1.35867)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.34783, 1.37415)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.35759, 1.38735)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.36466, 1.39845)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.36927, 1.40767)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.37167, 1.41525)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.37210, 1.42145)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.37076, 1.42650)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.36790, 1.43069)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.36374, 1.43430)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.35850, 1.43758)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, -0.01667), V2(2.35239, 1.44083)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, -0.03333), V2(2.16145, 1.97665)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, -0.05000), V2(2.00000, 2.54279)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, -0.06667), V2(2.00000, 1.45539)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(3.02330, 2.56316)),
        new TF(V2(18.72,  0.00), V2(3.00192, 2.51796)),
        new TF(V2(18.72,  0.00), V2(2.98050, 2.47445)),
        new TF(V2(18.72,  0.00), V2(2.95905, 2.43257)),
        new TF(V2( 1.93,  0.00), V2(3.02325, 2.56327)),
        new TF(V2( 1.86,  0.00), V2(3.64085, 4.78200)),
        new TF(V2( 1.79,  0.00), V2(3.69643, 4.85575)),
        new TF(V2( 1.72,  0.00), V2(3.70336, 4.81454)),
        new TF(V2( 1.65,  0.00), V2(3.70004, 4.70577)),
        new TF(V2( 1.58, -0.08), V2(3.69420, 4.57793)),
        new TF(V2( 1.51, -0.16), V2(3.69127, 4.47876)),
        new TF(V2( 1.44, -0.24), V2(3.69114, 4.41003)),
        new TF(V2( 1.37, -0.32), V2(3.68956, 4.34082)),
        new TF(V2( 1.30, -0.40), V2(3.68594, 4.26933)),
        new TF(V2( 1.23, -0.48), V2(3.68319, 4.19396)),
        new TF(V2( 1.16, -0.56), V2(3.68364, 4.11326)),
        new TF(V2( 1.09, -0.64), V2(3.68466, 4.02602)),
        new TF(V2( 1.02, -0.72), V2(3.68516, 3.93124)),
        new TF(V2( 0.95, -0.80), V2(3.68507, 3.82826)),
        new TF(V2( 0.88, -0.88), V2(3.68428, 3.71671)),
        new TF(V2( 0.81, -0.96), V2(3.68268, 3.59665)),
        new TF(V2( 0.74, -1.04), V2(3.68012, 3.46857)),
        new TF(V2( 0.67, -1.12), V2(3.67649, 3.33354)),
        new TF(V2( 0.60, -1.20), V2(3.67161, 3.19239)),
        new TF(V2( 0.53, -1.28), V2(3.66532, 3.05036)),
        new TF(V2( 0.46, -1.36), V2(3.65743, 2.90823)),
        new TF(V2( 0.39, -1.44), V2(3.64775, 2.77161)),
        new TF(V2( 0.32, -1.52), V2(3.63609, 2.64659)),
        new TF(V2( 0.25, -1.60), V2(3.62220, 2.54095)),
        new TF(V2( 0.18, -1.68), V2(3.60791, 2.46444)),
        new TF(V2( 0.11, -1.76), V2(3.44959, 2.94891)),
        new TF(V2( 0.04, -1.84), V2(3.30907, 3.36998)),
        new TF(V2( 0.00, -1.92), V2(3.25845, 4.34032)),
        new TF(V2( 0.00, -2.00), V2(3.32169, 4.54768)),
        new TF(V2( 0.00, -2.08), V2(3.27599, 5.69292)),
        new TF(V2( 0.00, -2.16), V2(3.14473, 5.97133)),
        new TF(V2( 0.00, -2.24), V2(3.19374, 4.72139)),
        new TF(V2( 0.00, -2.32), V2(3.21177, 4.73918)),
        new TF(V2( 0.00, -2.40), V2(3.41658, 5.60891)),
        new TF(V2( 0.00, -2.48), V2(3.17428, 4.58500)),
        new TF(V2( 0.00, -2.56), V2(3.09681, 3.46683)),
        new TF(V2( 0.00, -2.64), V2(3.08015, 2.74863)),
        new TF(V2( 0.00, -2.72), V2(3.06682, 1.81617)),
        new TF(V2( 0.00, -2.80), V2(3.01981, 1.00061)),
        new TF(TF::driftCalculator(0.23, 2.8, 0.83, 0.08, 0.02, 3.4), V2(2, 0))
    })},
    {"FoxIllusion.Long", new Trajectory(0, 15, LEDGE_GRAB_MODE_ALWAYS, false, new Trajectory::Frames{
        new TF(TF::convergeHorizontalCalculator(2.0 / 3.0, 0.05, 0,  0.00000), V2(2.00000, 3.50615)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.30477, 2.82410)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.43458, 2.08694)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.28246, 1.36353)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.33513, 1.35867)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.34783, 1.37415)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.35759, 1.38735)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.36466, 1.39845)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.36927, 1.40767)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.37167, 1.41525)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.37210, 1.42145)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.37076, 1.42650)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.36790, 1.43069)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.36374, 1.43430)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.35850, 1.43758)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, -0.01667), V2(2.35239, 1.44083)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, -0.03333), V2(2.16145, 1.97665)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, -0.05000), V2(2.00000, 2.54279)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, -0.06667), V2(2.00000, 1.45539)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(3.02330, 2.56316)),
        new TF(V2(18.72,  0.00), V2(3.00192, 2.51796)),
        new TF(V2(18.72,  0.00), V2(2.98050, 2.47445)),
        new TF(V2( 1.93,  0.00), V2(3.02325, 2.56327)),
        new TF(V2( 1.86,  0.00), V2(3.64085, 4.78200)),
        new TF(V2( 1.79,  0.00), V2(3.69643, 4.85575)),
        new TF(V2( 1.72,  0.00), V2(3.70336, 4.81454)),
        new TF(V2( 1.65,  0.00), V2(3.70004, 4.70577)),
        new TF(V2( 1.58, -0.08), V2(3.69420, 4.57793)),
        new TF(V2( 1.51, -0.16), V2(3.69127, 4.47876)),
        new TF(V2( 1.44, -0.24), V2(3.69114, 4.41003)),
        new TF(V2( 1.37, -0.32), V2(3.68956, 4.34082)),
        new TF(V2( 1.30, -0.40), V2(3.68594, 4.26933)),
        new TF(V2( 1.23, -0.48), V2(3.68319, 4.19396)),
        new TF(V2( 1.16, -0.56), V2(3.68364, 4.11326)),
        new TF(V2( 1.09, -0.64), V2(3.68466, 4.02602)),
        new TF(V2( 1.02, -0.72), V2(3.68516, 3.93124)),
        new TF(V2( 0.95, -0.80), V2(3.68507, 3.82826)),
        new TF(V2( 0.88, -0.88), V2(3.68428, 3.71671)),
        new TF(V2( 0.81, -0.96), V2(3.68268, 3.59665)),
        new TF(V2( 0.74, -1.04), V2(3.68012, 3.46857)),
        new TF(V2( 0.67, -1.12), V2(3.67649, 3.33354)),
        new TF(V2( 0.60, -1.20), V2(3.67161, 3.19239)),
        new TF(V2( 0.53, -1.28), V2(3.66532, 3.05036)),
        new TF(V2( 0.46, -1.36), V2(3.65743, 2.90823)),
        new TF(V2( 0.39, -1.44), V2(3.64775, 2.77161)),
        new TF(V2( 0.32, -1.52), V2(3.63609, 2.64659)),
        new TF(V2( 0.25, -1.60), V2(3.62220, 2.54095)),
        new TF(V2( 0.18, -1.68), V2(3.60791, 2.46444)),
        new TF(V2( 0.11, -1.76), V2(3.44959, 2.94891)),
        new TF(V2( 0.04, -1.84), V2(3.30907, 3.36998)),
        new TF(V2( 0.00, -1.92), V2(3.25845, 4.34032)),
        new TF(V2( 0.00, -2.00), V2(3.32169, 4.54768)),
        new TF(V2( 0.00, -2.08), V2(3.27599, 5.69292)),
        new TF(V2( 0.00, -2.16), V2(3.14473, 5.97133)),
        new TF(V2( 0.00, -2.24), V2(3.19374, 4.72139)),
        new TF(V2( 0.00, -2.32), V2(3.21177, 4.73918)),
        new TF(V2( 0.00, -2.40), V2(3.41658, 5.60891)),
        new TF(V2( 0.00, -2.48), V2(3.17428, 4.58500)),
        new TF(V2( 0.00, -2.56), V2(3.09681, 3.46683)),
        new TF(V2( 0.00, -2.64), V2(3.08015, 2.74863)),
        new TF(V2( 0.00, -2.72), V2(3.06682, 1.81617)),
        new TF(V2( 0.00, -2.80), V2(3.01981, 1.00061)),
        new TF(TF::driftCalculator(0.23, 2.8, 0.83, 0.08, 0.02, 3.4), V2(2, 0))
    })},
    {"FoxIllusion.Mid", new Trajectory(0, 15, LEDGE_GRAB_MODE_ALWAYS, false, new Trajectory::Frames{
        new TF(TF::convergeHorizontalCalculator(2.0 / 3.0, 0.05, 0,  0.00000), V2(2.00000, 3.50615)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.30477, 2.82410)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.43458, 2.08694)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.28246, 1.36353)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.33513, 1.35867)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.34783, 1.37415)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.35759, 1.38735)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.36466, 1.39845)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.36927, 1.40767)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.37167, 1.41525)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.37210, 1.42145)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.37076, 1.42650)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.36790, 1.43069)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.36374, 1.43430)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.35850, 1.43758)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, -0.01667), V2(2.35239, 1.44083)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, -0.03333), V2(2.16145, 1.97665)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, -0.05000), V2(2.00000, 2.54279)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, -0.06667), V2(2.00000, 1.45539)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(3.02330, 2.56316)),
        new TF(V2(18.72,  0.00), V2(3.00192, 2.51796)),
        new TF(V2( 1.93,  0.00), V2(3.02325, 2.56327)),
        new TF(V2( 1.86,  0.00), V2(3.64085, 4.78200)),
        new TF(V2( 1.79,  0.00), V2(3.69643, 4.85575)),
        new TF(V2( 1.72,  0.00), V2(3.70336, 4.81454)),
        new TF(V2( 1.65,  0.00), V2(3.70004, 4.70577)),
        new TF(V2( 1.58, -0.08), V2(3.69420, 4.57793)),
        new TF(V2( 1.51, -0.16), V2(3.69127, 4.47876)),
        new TF(V2( 1.44, -0.24), V2(3.69114, 4.41003)),
        new TF(V2( 1.37, -0.32), V2(3.68956, 4.34082)),
        new TF(V2( 1.30, -0.40), V2(3.68594, 4.26933)),
        new TF(V2( 1.23, -0.48), V2(3.68319, 4.19396)),
        new TF(V2( 1.16, -0.56), V2(3.68364, 4.11326)),
        new TF(V2( 1.09, -0.64), V2(3.68466, 4.02602)),
        new TF(V2( 1.02, -0.72), V2(3.68516, 3.93124)),
        new TF(V2( 0.95, -0.80), V2(3.68507, 3.82826)),
        new TF(V2( 0.88, -0.88), V2(3.68428, 3.71671)),
        new TF(V2( 0.81, -0.96), V2(3.68268, 3.59665)),
        new TF(V2( 0.74, -1.04), V2(3.68012, 3.46857)),
        new TF(V2( 0.67, -1.12), V2(3.67649, 3.33354)),
        new TF(V2( 0.60, -1.20), V2(3.67161, 3.19239)),
        new TF(V2( 0.53, -1.28), V2(3.66532, 3.05036)),
        new TF(V2( 0.46, -1.36), V2(3.65743, 2.90823)),
        new TF(V2( 0.39, -1.44), V2(3.64775, 2.77161)),
        new TF(V2( 0.32, -1.52), V2(3.63609, 2.64659)),
        new TF(V2( 0.25, -1.60), V2(3.62220, 2.54095)),
        new TF(V2( 0.18, -1.68), V2(3.60791, 2.46444)),
        new TF(V2( 0.11, -1.76), V2(3.44959, 2.94891)),
        new TF(V2( 0.04, -1.84), V2(3.30907, 3.36998)),
        new TF(V2( 0.00, -1.92), V2(3.25845, 4.34032)),
        new TF(V2( 0.00, -2.00), V2(3.32169, 4.54768)),
        new TF(V2( 0.00, -2.08), V2(3.27599, 5.69292)),
        new TF(V2( 0.00, -2.16), V2(3.14473, 5.97133)),
        new TF(V2( 0.00, -2.24), V2(3.19374, 4.72139)),
        new TF(V2( 0.00, -2.32), V2(3.21177, 4.73918)),
        new TF(V2( 0.00, -2.40), V2(3.41658, 5.60891)),
        new TF(V2( 0.00, -2.48), V2(3.17428, 4.58500)),
        new TF(V2( 0.00, -2.56), V2(3.09681, 3.46683)),
        new TF(V2( 0.00, -2.64), V2(3.08015, 2.74863)),
        new TF(V2( 0.00, -2.72), V2(3.06682, 1.81617)),
        new TF(V2( 0.00, -2.80), V2(3.01981, 1.00061)),
        new TF(TF::driftCalculator(0.23, 2.8, 0.83, 0.08, 0.02, 3.4), V2(2, 0))
    })},
    {"FoxIllusion.SlowShort", new Trajectory(0, 15, LEDGE_GRAB_MODE_ALWAYS, false, new Trajectory::Frames{
        new TF(TF::convergeHorizontalCalculator(2.0 / 3.0, 0.05, 0,  0.00000), V2(2.00000, 3.50615)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.30477, 2.82410)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.43458, 2.08694)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.28246, 1.36353)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.33513, 1.35867)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.34783, 1.37415)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.35759, 1.38735)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.36466, 1.39845)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.36927, 1.40767)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.37167, 1.41525)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.37210, 1.42145)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.37076, 1.42650)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.36790, 1.43069)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.36374, 1.43430)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.35850, 1.43758)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, -0.01667), V2(2.35239, 1.44083)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, -0.03333), V2(2.16145, 1.97665)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, -0.05000), V2(2.00000, 2.54279)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, -0.06667), V2(2.00000, 1.45539)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(3.02330, 2.56316)),
        new TF(V2( 1.93,  0.00), V2(3.02325, 2.56327)),
        new TF(V2( 1.86,  0.00), V2(3.64085, 4.78200)),
        new TF(V2( 1.79,  0.00), V2(3.69643, 4.85575)),
        new TF(V2( 1.72,  0.00), V2(3.70336, 4.81454)),
        new TF(V2( 1.65,  0.00), V2(3.70004, 4.70577)),
        new TF(V2( 1.58, -0.08), V2(3.69420, 4.57793)),
        new TF(V2( 1.51, -0.16), V2(3.69127, 4.47876)),
        new TF(V2( 1.44, -0.24), V2(3.69114, 4.41003)),
        new TF(V2( 1.37, -0.32), V2(3.68956, 4.34082)),
        new TF(V2( 1.30, -0.40), V2(3.68594, 4.26933)),
        new TF(V2( 1.23, -0.48), V2(3.68319, 4.19396)),
        new TF(V2( 1.16, -0.56), V2(3.68364, 4.11326)),
        new TF(V2( 1.09, -0.64), V2(3.68466, 4.02602)),
        new TF(V2( 1.02, -0.72), V2(3.68516, 3.93124)),
        new TF(V2( 0.95, -0.80), V2(3.68507, 3.82826)),
        new TF(V2( 0.88, -0.88), V2(3.68428, 3.71671)),
        new TF(V2( 0.81, -0.96), V2(3.68268, 3.59665)),
        new TF(V2( 0.74, -1.04), V2(3.68012, 3.46857)),
        new TF(V2( 0.67, -1.12), V2(3.67649, 3.33354)),
        new TF(V2( 0.60, -1.20), V2(3.67161, 3.19239)),
        new TF(V2( 0.53, -1.28), V2(3.66532, 3.05036)),
        new TF(V2( 0.46, -1.36), V2(3.65743, 2.90823)),
        new TF(V2( 0.39, -1.44), V2(3.64775, 2.77161)),
        new TF(V2( 0.32, -1.52), V2(3.63609, 2.64659)),
        new TF(V2( 0.25, -1.60), V2(3.62220, 2.54095)),
        new TF(V2( 0.18, -1.68), V2(3.60791, 2.46444)),
        new TF(V2( 0.11, -1.76), V2(3.44959, 2.94891)),
        new TF(V2( 0.04, -1.84), V2(3.30907, 3.36998)),
        new TF(V2( 0.00, -1.92), V2(3.25845, 4.34032)),
        new TF(V2( 0.00, -2.00), V2(3.32169, 4.54768)),
        new TF(V2( 0.00, -2.08), V2(3.27599, 5.69292)),
        new TF(V2( 0.00, -2.16), V2(3.14473, 5.97133)),
        new TF(V2( 0.00, -2.24), V2(3.19374, 4.72139)),
        new TF(V2( 0.00, -2.32), V2(3.21177, 4.73918)),
        new TF(V2( 0.00, -2.40), V2(3.41658, 5.60891)),
        new TF(V2( 0.00, -2.48), V2(3.17428, 4.58500)),
        new TF(V2( 0.00, -2.56), V2(3.09681, 3.46683)),
        new TF(V2( 0.00, -2.64), V2(3.08015, 2.74863)),
        new TF(V2( 0.00, -2.72), V2(3.06682, 1.81617)),
        new TF(V2( 0.00, -2.80), V2(3.01981, 1.00061)),
        new TF(TF::driftCalculator(0.23, 2.8, 0.83, 0.08, 0.02, 3.4), V2(2, 0))
    })},
    {"FoxIllusion.FastShort", new Trajectory(0, 15, LEDGE_GRAB_MODE_ALWAYS, false, new Trajectory::Frames{
        new TF(TF::convergeHorizontalCalculator(2.0 / 3.0, 0.05, 0,  0.00000), V2(2.00000, 3.50615)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.30477, 2.82410)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.43458, 2.08694)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.28246, 1.36353)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.33513, 1.35867)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.34783, 1.37415)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.35759, 1.38735)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.36466, 1.39845)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.36927, 1.40767)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.37167, 1.41525)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.37210, 1.42145)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.37076, 1.42650)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.36790, 1.43069)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.36374, 1.43430)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0,  0.00000), V2(2.35850, 1.43758)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, -0.01667), V2(2.35239, 1.44083)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, -0.03333), V2(2.16145, 1.97665)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, -0.05000), V2(2.00000, 2.54279)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, -0.06667), V2(2.00000, 1.45539)),
        new TF(V2( 1.93,  0.00), V2(3.02325, 2.56327)),
        new TF(V2( 1.86,  0.00), V2(3.64085, 4.78200)),
        new TF(V2( 1.79,  0.00), V2(3.69643, 4.85575)),
        new TF(V2( 1.72,  0.00), V2(3.70336, 4.81454)),
        new TF(V2( 1.65,  0.00), V2(3.70004, 4.70577)),
        new TF(V2( 1.58, -0.08), V2(3.69420, 4.57793)),
        new TF(V2( 1.51, -0.16), V2(3.69127, 4.47876)),
        new TF(V2( 1.44, -0.24), V2(3.69114, 4.41003)),
        new TF(V2( 1.37, -0.32), V2(3.68956, 4.34082)),
        new TF(V2( 1.30, -0.40), V2(3.68594, 4.26933)),
        new TF(V2( 1.23, -0.48), V2(3.68319, 4.19396)),
        new TF(V2( 1.16, -0.56), V2(3.68364, 4.11326)),
        new TF(V2( 1.09, -0.64), V2(3.68466, 4.02602)),
        new TF(V2( 1.02, -0.72), V2(3.68516, 3.93124)),
        new TF(V2( 0.95, -0.80), V2(3.68507, 3.82826)),
        new TF(V2( 0.88, -0.88), V2(3.68428, 3.71671)),
        new TF(V2( 0.81, -0.96), V2(3.68268, 3.59665)),
        new TF(V2( 0.74, -1.04), V2(3.68012, 3.46857)),
        new TF(V2( 0.67, -1.12), V2(3.67649, 3.33354)),
        new TF(V2( 0.60, -1.20), V2(3.67161, 3.19239)),
        new TF(V2( 0.53, -1.28), V2(3.66532, 3.05036)),
        new TF(V2( 0.46, -1.36), V2(3.65743, 2.90823)),
        new TF(V2( 0.39, -1.44), V2(3.64775, 2.77161)),
        new TF(V2( 0.32, -1.52), V2(3.63609, 2.64659)),
        new TF(V2( 0.25, -1.60), V2(3.62220, 2.54095)),
        new TF(V2( 0.18, -1.68), V2(3.60791, 2.46444)),
        new TF(V2( 0.11, -1.76), V2(3.44959, 2.94891)),
        new TF(V2( 0.04, -1.84), V2(3.30907, 3.36998)),
        new TF(V2( 0.00, -1.92), V2(3.25845, 4.34032)),
        new TF(V2( 0.00, -2.00), V2(3.32169, 4.54768)),
        new TF(V2( 0.00, -2.08), V2(3.27599, 5.69292)),
        new TF(V2( 0.00, -2.16), V2(3.14473, 5.97133)),
        new TF(V2( 0.00, -2.24), V2(3.19374, 4.72139)),
        new TF(V2( 0.00, -2.32), V2(3.21177, 4.73918)),
        new TF(V2( 0.00, -2.40), V2(3.41658, 5.60891)),
        new TF(V2( 0.00, -2.48), V2(3.17428, 4.58500)),
        new TF(V2( 0.00, -2.56), V2(3.09681, 3.46683)),
        new TF(V2( 0.00, -2.64), V2(3.08015, 2.74863)),
        new TF(V2( 0.00, -2.72), V2(3.06682, 1.81617)),
        new TF(V2( 0.00, -2.80), V2(3.01981, 1.00061)),
        new TF(TF::driftCalculator(0.23, 2.8, 0.83, 0.08, 0.02, 3.4), V2(2, 0))
    })},
    {"FalcoPhantasm.Full", new Trajectory(0, 24, LEDGE_GRAB_MODE_ALWAYS, false, new Trajectory::Frames{
        new TF(TF::convergeHorizontalCalculator(2.0 / 3.0, 0.05, 0, 0), V2(2.12880, 4.01945)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.52756, 3.24007)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.48707, 2.39783)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.44669, 1.57153)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.50793, 1.56792)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.52137, 1.58662)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.53072, 1.60219)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.53633, 1.61497)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.53854, 1.62543)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.53774, 1.63400)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.53423, 1.64113)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.52835, 1.64730)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.29675, 2.26603)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.00000, 2.91119)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.00000, 1.66790)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(3.85365, 2.93698)),
        new TF(V2(16.50,  0.00), V2(3.82917, 2.88519)),
        new TF(V2(16.50,  0.00), V2(3.80461, 2.83530)),
        new TF(V2(16.50,  0.00), V2(3.78001, 2.78727)),
        new TF(V2( 1.93,  0.00), V2(3.85357, 2.93711)),
        new TF(V2( 1.86,  0.00), V2(4.12489, 5.46590)),
        new TF(V2( 1.79,  0.00), V2(4.04909, 5.54576)),
        new TF(V2( 1.72,  0.00), V2(4.05551, 5.49733)),
        new TF(V2( 1.65,  0.00), V2(4.05251, 5.37354)),
        new TF(V2( 1.58, -0.08), V2(4.04788, 5.22857)),
        new TF(V2( 1.51, -0.16), V2(4.04594, 5.11575)),
        new TF(V2( 1.44, -0.24), V2(4.04639, 5.03700)),
        new TF(V2( 1.37, -0.32), V2(4.04525, 4.95768)),
        new TF(V2( 1.30, -0.40), V2(4.04176, 4.87577)),
        new TF(V2( 1.23, -0.48), V2(4.03894, 4.78940)),
        new TF(V2( 1.16, -0.56), V2(4.03933, 4.69693)),
        new TF(V2( 1.09, -0.64), V2(4.04027, 4.59695)),
        new TF(V2( 1.02, -0.72), V2(4.04062, 4.48837)),
        new TF(V2( 0.95, -0.80), V2(4.04032, 4.37038)),
        new TF(V2( 0.88, -0.88), V2(4.03925, 4.24260)),
        new TF(V2( 0.81, -0.96), V2(4.03731, 4.10508)),
        new TF(V2( 0.74, -1.04), V2(4.03437, 3.95841)),
        new TF(V2( 0.67, -1.12), V2(4.03030, 3.80382)),
        new TF(V2( 0.60, -1.20), V2(4.02495, 3.64330)),
        new TF(V2( 0.53, -1.28), V2(4.01816, 3.47978)),
        new TF(V2( 0.46, -1.36), V2(4.01505, 3.31730)),
        new TF(V2( 0.39, -1.44), V2(4.02505, 3.16124)),
        new TF(V2( 0.32, -1.52), V2(4.05714, 3.01864)),
        new TF(V2( 0.25, -1.60), V2(4.11563, 2.89843)),
        new TF(V2( 0.18, -1.68), V2(4.17657, 2.81184)),
        new TF(V2( 0.11, -1.76), V2(4.27316, 3.36983)),
        new TF(V2( 0.04, -1.84), V2(4.26672, 3.85816)),
        new TF(V2( 0.00, -1.92), V2(4.15292, 4.97776)),
        new TF(V2( 0.00, -2.00), V2(4.18509, 5.21088)),
        new TF(V2( 0.00, -2.08), V2(4.22651, 6.25313)),
        new TF(V2( 0.00, -2.16), V2(4.10917, 7.01115)),
        new TF(V2( 0.00, -2.24), V2(3.90833, 5.72179)),
        new TF(V2( 0.00, -2.32), V2(3.79810, 5.75143)),
        new TF(V2( 0.00, -2.40), V2(3.90985, 6.67566)),
        new TF(V2( 0.00, -2.48), V2(3.47979, 5.24105)),
        new TF(V2( 0.00, -2.56), V2(3.38390, 3.96497)),
        new TF(V2( 0.00, -2.64), V2(3.36013, 3.14971)),
        new TF(V2( 0.00, -2.72), V2(3.35086, 2.08666)),
        new TF(V2( 0.00, -2.80), V2(3.31787, 1.15199)),
        new TF(TF::driftCalculator(0.17, 3.1, 0.83, 0.07, 0.02, 3.5), V2(2, 0))
    })},
    {"FalcoPhantasm.Long", new Trajectory(0, 23, LEDGE_GRAB_MODE_ALWAYS, false, new Trajectory::Frames{
        new TF(TF::convergeHorizontalCalculator(2.0 / 3.0, 0.05, 0, 0), V2(2.12880, 4.01945)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.52756, 3.24007)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.48707, 2.39783)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.44669, 1.57153)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.50793, 1.56792)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.52137, 1.58662)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.53072, 1.60219)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.53633, 1.61497)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.53854, 1.62543)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.53774, 1.63400)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.53423, 1.64113)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.52835, 1.64730)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.29675, 2.26603)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.00000, 2.91119)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.00000, 1.66790)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(3.85365, 2.93698)),
        new TF(V2(16.50,  0.00), V2(3.82917, 2.88519)),
        new TF(V2(16.50,  0.00), V2(3.80461, 2.83530)),
        new TF(V2( 1.93,  0.00), V2(3.85357, 2.93711)),
        new TF(V2( 1.86,  0.00), V2(4.12489, 5.46590)),
        new TF(V2( 1.79,  0.00), V2(4.04909, 5.54576)),
        new TF(V2( 1.72,  0.00), V2(4.05551, 5.49733)),
        new TF(V2( 1.65,  0.00), V2(4.05251, 5.37354)),
        new TF(V2( 1.58, -0.08), V2(4.04788, 5.22857)),
        new TF(V2( 1.51, -0.16), V2(4.04594, 5.11575)),
        new TF(V2( 1.44, -0.24), V2(4.04639, 5.03700)),
        new TF(V2( 1.37, -0.32), V2(4.04525, 4.95768)),
        new TF(V2( 1.30, -0.40), V2(4.04176, 4.87577)),
        new TF(V2( 1.23, -0.48), V2(4.03894, 4.78940)),
        new TF(V2( 1.16, -0.56), V2(4.03933, 4.69693)),
        new TF(V2( 1.09, -0.64), V2(4.04027, 4.59695)),
        new TF(V2( 1.02, -0.72), V2(4.04062, 4.48837)),
        new TF(V2( 0.95, -0.80), V2(4.04032, 4.37038)),
        new TF(V2( 0.88, -0.88), V2(4.03925, 4.24260)),
        new TF(V2( 0.81, -0.96), V2(4.03731, 4.10508)),
        new TF(V2( 0.74, -1.04), V2(4.03437, 3.95841)),
        new TF(V2( 0.67, -1.12), V2(4.03030, 3.80382)),
        new TF(V2( 0.60, -1.20), V2(4.02495, 3.64330)),
        new TF(V2( 0.53, -1.28), V2(4.01816, 3.47978)),
        new TF(V2( 0.46, -1.36), V2(4.01505, 3.31730)),
        new TF(V2( 0.39, -1.44), V2(4.02505, 3.16124)),
        new TF(V2( 0.32, -1.52), V2(4.05714, 3.01864)),
        new TF(V2( 0.25, -1.60), V2(4.11563, 2.89843)),
        new TF(V2( 0.18, -1.68), V2(4.17657, 2.81184)),
        new TF(V2( 0.11, -1.76), V2(4.27316, 3.36983)),
        new TF(V2( 0.04, -1.84), V2(4.26672, 3.85816)),
        new TF(V2( 0.00, -1.92), V2(4.15292, 4.97776)),
        new TF(V2( 0.00, -2.00), V2(4.18509, 5.21088)),
        new TF(V2( 0.00, -2.08), V2(4.22651, 6.25313)),
        new TF(V2( 0.00, -2.16), V2(4.10917, 7.01115)),
        new TF(V2( 0.00, -2.24), V2(3.90833, 5.72179)),
        new TF(V2( 0.00, -2.32), V2(3.79810, 5.75143)),
        new TF(V2( 0.00, -2.40), V2(3.90985, 6.67566)),
        new TF(V2( 0.00, -2.48), V2(3.47979, 5.24105)),
        new TF(V2( 0.00, -2.56), V2(3.38390, 3.96497)),
        new TF(V2( 0.00, -2.64), V2(3.36013, 3.14971)),
        new TF(V2( 0.00, -2.72), V2(3.35086, 2.08666)),
        new TF(V2( 0.00, -2.80), V2(3.31787, 1.15199)),
        new TF(TF::driftCalculator(0.17, 3.1, 0.83, 0.07, 0.02, 3.5), V2(2, 0))
    })},
    {"FalcoPhantasm.Mid", new Trajectory(0, 22, LEDGE_GRAB_MODE_ALWAYS, false, new Trajectory::Frames{
        new TF(TF::convergeHorizontalCalculator(2.0 / 3.0, 0.05, 0, 0), V2(2.12880, 4.01945)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.52756, 3.24007)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.48707, 2.39783)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.44669, 1.57153)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.50793, 1.56792)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.52137, 1.58662)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.53072, 1.60219)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.53633, 1.61497)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.53854, 1.62543)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.53774, 1.63400)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.53423, 1.64113)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.52835, 1.64730)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.29675, 2.26603)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.00000, 2.91119)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.00000, 1.66790)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(3.85365, 2.93698)),
        new TF(V2(16.50,  0.00), V2(3.82917, 2.88519)),
        new TF(V2( 1.93,  0.00), V2(3.85357, 2.93711)),
        new TF(V2( 1.86,  0.00), V2(4.12489, 5.46590)),
        new TF(V2( 1.79,  0.00), V2(4.04909, 5.54576)),
        new TF(V2( 1.72,  0.00), V2(4.05551, 5.49733)),
        new TF(V2( 1.65,  0.00), V2(4.05251, 5.37354)),
        new TF(V2( 1.58, -0.08), V2(4.04788, 5.22857)),
        new TF(V2( 1.51, -0.16), V2(4.04594, 5.11575)),
        new TF(V2( 1.44, -0.24), V2(4.04639, 5.03700)),
        new TF(V2( 1.37, -0.32), V2(4.04525, 4.95768)),
        new TF(V2( 1.30, -0.40), V2(4.04176, 4.87577)),
        new TF(V2( 1.23, -0.48), V2(4.03894, 4.78940)),
        new TF(V2( 1.16, -0.56), V2(4.03933, 4.69693)),
        new TF(V2( 1.09, -0.64), V2(4.04027, 4.59695)),
        new TF(V2( 1.02, -0.72), V2(4.04062, 4.48837)),
        new TF(V2( 0.95, -0.80), V2(4.04032, 4.37038)),
        new TF(V2( 0.88, -0.88), V2(4.03925, 4.24260)),
        new TF(V2( 0.81, -0.96), V2(4.03731, 4.10508)),
        new TF(V2( 0.74, -1.04), V2(4.03437, 3.95841)),
        new TF(V2( 0.67, -1.12), V2(4.03030, 3.80382)),
        new TF(V2( 0.60, -1.20), V2(4.02495, 3.64330)),
        new TF(V2( 0.53, -1.28), V2(4.01816, 3.47978)),
        new TF(V2( 0.46, -1.36), V2(4.01505, 3.31730)),
        new TF(V2( 0.39, -1.44), V2(4.02505, 3.16124)),
        new TF(V2( 0.32, -1.52), V2(4.05714, 3.01864)),
        new TF(V2( 0.25, -1.60), V2(4.11563, 2.89843)),
        new TF(V2( 0.18, -1.68), V2(4.17657, 2.81184)),
        new TF(V2( 0.11, -1.76), V2(4.27316, 3.36983)),
        new TF(V2( 0.04, -1.84), V2(4.26672, 3.85816)),
        new TF(V2( 0.00, -1.92), V2(4.15292, 4.97776)),
        new TF(V2( 0.00, -2.00), V2(4.18509, 5.21088)),
        new TF(V2( 0.00, -2.08), V2(4.22651, 6.25313)),
        new TF(V2( 0.00, -2.16), V2(4.10917, 7.01115)),
        new TF(V2( 0.00, -2.24), V2(3.90833, 5.72179)),
        new TF(V2( 0.00, -2.32), V2(3.79810, 5.75143)),
        new TF(V2( 0.00, -2.40), V2(3.90985, 6.67566)),
        new TF(V2( 0.00, -2.48), V2(3.47979, 5.24105)),
        new TF(V2( 0.00, -2.56), V2(3.38390, 3.96497)),
        new TF(V2( 0.00, -2.64), V2(3.36013, 3.14971)),
        new TF(V2( 0.00, -2.72), V2(3.35086, 2.08666)),
        new TF(V2( 0.00, -2.80), V2(3.31787, 1.15199)),
        new TF(TF::driftCalculator(0.17, 3.1, 0.83, 0.07, 0.02, 3.5), V2(2, 0))
    })},
    {"FalcoPhantasm.SlowShort", new Trajectory(0, 21, LEDGE_GRAB_MODE_ALWAYS, false, new Trajectory::Frames{
        new TF(TF::convergeHorizontalCalculator(2.0 / 3.0, 0.05, 0, 0), V2(2.12880, 4.01945)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.52756, 3.24007)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.48707, 2.39783)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.44669, 1.57153)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.50793, 1.56792)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.52137, 1.58662)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.53072, 1.60219)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.53633, 1.61497)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.53854, 1.62543)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.53774, 1.63400)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.53423, 1.64113)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.52835, 1.64730)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.29675, 2.26603)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.00000, 2.91119)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.00000, 1.66790)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(3.85365, 2.93698)),
        new TF(V2( 1.93,  0.00), V2(3.85357, 2.93711)),
        new TF(V2( 1.86,  0.00), V2(4.12489, 5.46590)),
        new TF(V2( 1.79,  0.00), V2(4.04909, 5.54576)),
        new TF(V2( 1.72,  0.00), V2(4.05551, 5.49733)),
        new TF(V2( 1.65,  0.00), V2(4.05251, 5.37354)),
        new TF(V2( 1.58, -0.08), V2(4.04788, 5.22857)),
        new TF(V2( 1.51, -0.16), V2(4.04594, 5.11575)),
        new TF(V2( 1.44, -0.24), V2(4.04639, 5.03700)),
        new TF(V2( 1.37, -0.32), V2(4.04525, 4.95768)),
        new TF(V2( 1.30, -0.40), V2(4.04176, 4.87577)),
        new TF(V2( 1.23, -0.48), V2(4.03894, 4.78940)),
        new TF(V2( 1.16, -0.56), V2(4.03933, 4.69693)),
        new TF(V2( 1.09, -0.64), V2(4.04027, 4.59695)),
        new TF(V2( 1.02, -0.72), V2(4.04062, 4.48837)),
        new TF(V2( 0.95, -0.80), V2(4.04032, 4.37038)),
        new TF(V2( 0.88, -0.88), V2(4.03925, 4.24260)),
        new TF(V2( 0.81, -0.96), V2(4.03731, 4.10508)),
        new TF(V2( 0.74, -1.04), V2(4.03437, 3.95841)),
        new TF(V2( 0.67, -1.12), V2(4.03030, 3.80382)),
        new TF(V2( 0.60, -1.20), V2(4.02495, 3.64330)),
        new TF(V2( 0.53, -1.28), V2(4.01816, 3.47978)),
        new TF(V2( 0.46, -1.36), V2(4.01505, 3.31730)),
        new TF(V2( 0.39, -1.44), V2(4.02505, 3.16124)),
        new TF(V2( 0.32, -1.52), V2(4.05714, 3.01864)),
        new TF(V2( 0.25, -1.60), V2(4.11563, 2.89843)),
        new TF(V2( 0.18, -1.68), V2(4.17657, 2.81184)),
        new TF(V2( 0.11, -1.76), V2(4.27316, 3.36983)),
        new TF(V2( 0.04, -1.84), V2(4.26672, 3.85816)),
        new TF(V2( 0.00, -1.92), V2(4.15292, 4.97776)),
        new TF(V2( 0.00, -2.00), V2(4.18509, 5.21088)),
        new TF(V2( 0.00, -2.08), V2(4.22651, 6.25313)),
        new TF(V2( 0.00, -2.16), V2(4.10917, 7.01115)),
        new TF(V2( 0.00, -2.24), V2(3.90833, 5.72179)),
        new TF(V2( 0.00, -2.32), V2(3.79810, 5.75143)),
        new TF(V2( 0.00, -2.40), V2(3.90985, 6.67566)),
        new TF(V2( 0.00, -2.48), V2(3.47979, 5.24105)),
        new TF(V2( 0.00, -2.56), V2(3.38390, 3.96497)),
        new TF(V2( 0.00, -2.64), V2(3.36013, 3.14971)),
        new TF(V2( 0.00, -2.72), V2(3.35086, 2.08666)),
        new TF(V2( 0.00, -2.80), V2(3.31787, 1.15199)),
        new TF(TF::driftCalculator(0.17, 3.1, 0.83, 0.07, 0.02, 3.5), V2(2, 0))
    })},
    {"FalcoPhantasm.FastShort", new Trajectory(0, 20, LEDGE_GRAB_MODE_ALWAYS, false, new Trajectory::Frames{
        new TF(TF::convergeHorizontalCalculator(2.0 / 3.0, 0.05, 0, 0), V2(2.12880, 4.01945)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.52756, 3.24007)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.48707, 2.39783)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.44669, 1.57153)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.50793, 1.56792)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.52137, 1.58662)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.53072, 1.60219)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.53633, 1.61497)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.53854, 1.62543)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.53774, 1.63400)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.53423, 1.64113)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.52835, 1.64730)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.29675, 2.26603)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.00000, 2.91119)),
        new TF(TF::convergeHorizontalCalculator(      1.0, 0.05, 0, 0), V2(2.00000, 1.66790)),
        new TF(V2( 1.93,  0.00), V2(3.85357, 2.93711)),
        new TF(V2( 1.86,  0.00), V2(4.12489, 5.46590)),
        new TF(V2( 1.79,  0.00), V2(4.04909, 5.54576)),
        new TF(V2( 1.72,  0.00), V2(4.05551, 5.49733)),
        new TF(V2( 1.65,  0.00), V2(4.05251, 5.37354)),
        new TF(V2( 1.58, -0.08), V2(4.04788, 5.22857)),
        new TF(V2( 1.51, -0.16), V2(4.04594, 5.11575)),
        new TF(V2( 1.44, -0.24), V2(4.04639, 5.03700)),
        new TF(V2( 1.37, -0.32), V2(4.04525, 4.95768)),
        new TF(V2( 1.30, -0.40), V2(4.04176, 4.87577)),
        new TF(V2( 1.23, -0.48), V2(4.03894, 4.78940)),
        new TF(V2( 1.16, -0.56), V2(4.03933, 4.69693)),
        new TF(V2( 1.09, -0.64), V2(4.04027, 4.59695)),
        new TF(V2( 1.02, -0.72), V2(4.04062, 4.48837)),
        new TF(V2( 0.95, -0.80), V2(4.04032, 4.37038)),
        new TF(V2( 0.88, -0.88), V2(4.03925, 4.24260)),
        new TF(V2( 0.81, -0.96), V2(4.03731, 4.10508)),
        new TF(V2( 0.74, -1.04), V2(4.03437, 3.95841)),
        new TF(V2( 0.67, -1.12), V2(4.03030, 3.80382)),
        new TF(V2( 0.60, -1.20), V2(4.02495, 3.64330)),
        new TF(V2( 0.53, -1.28), V2(4.01816, 3.47978)),
        new TF(V2( 0.46, -1.36), V2(4.01505, 3.31730)),
        new TF(V2( 0.39, -1.44), V2(4.02505, 3.16124)),
        new TF(V2( 0.32, -1.52), V2(4.05714, 3.01864)),
        new TF(V2( 0.25, -1.60), V2(4.11563, 2.89843)),
        new TF(V2( 0.18, -1.68), V2(4.17657, 2.81184)),
        new TF(V2( 0.11, -1.76), V2(4.27316, 3.36983)),
        new TF(V2( 0.04, -1.84), V2(4.26672, 3.85816)),
        new TF(V2( 0.00, -1.92), V2(4.15292, 4.97776)),
        new TF(V2( 0.00, -2.00), V2(4.18509, 5.21088)),
        new TF(V2( 0.00, -2.08), V2(4.22651, 6.25313)),
        new TF(V2( 0.00, -2.16), V2(4.10917, 7.01115)),
        new TF(V2( 0.00, -2.24), V2(3.90833, 5.72179)),
        new TF(V2( 0.00, -2.32), V2(3.79810, 5.75143)),
        new TF(V2( 0.00, -2.40), V2(3.90985, 6.67566)),
        new TF(V2( 0.00, -2.48), V2(3.47979, 5.24105)),
        new TF(V2( 0.00, -2.56), V2(3.38390, 3.96497)),
        new TF(V2( 0.00, -2.64), V2(3.36013, 3.14971)),
        new TF(V2( 0.00, -2.72), V2(3.35086, 2.08666)),
        new TF(V2( 0.00, -2.80), V2(3.31787, 1.15199)),
        new TF(TF::driftCalculator(0.17, 3.1, 0.83, 0.07, 0.02, 3.5), V2(2, 0))
    })},
    {"DancingBlade.Strong", new Trajectory(0, 16, LEDGE_GRAB_MODE_AFTER, false, new Trajectory::Frames{
        new TF(TF::convergeHorizontalCalculator(0.8, 0.0025, 0, 0.94), V2(2.11648, 4.64884)),
        new TF(TF::convergeVectorCalculator(0.0025, 0.06, 0, -1.5), V2(2.51202, 5.78777)),
        new TF(TF::convergeVectorCalculator(0.0025, 0.06, 0, -1.5), V2(2.00000, 6.15807)),
        new TF(TF::convergeVectorCalculator(0.0025, 0.06, 0, -1.5), V2(2.19584, 5.88850)),
        new TF(TF::convergeVectorCalculator(0.0025, 0.06, 0, -1.5), V2(3.22828, 6.24290)),
        new TF(TF::convergeVectorCalculator(0.0025, 0.06, 0, -1.5), V2(3.11102, 5.82793)),
        new TF(TF::convergeVectorCalculator(0.0025, 0.06, 0, -1.5), V2(3.12281, 5.16819)),
        new TF(TF::convergeVectorCalculator(0.0025, 0.06, 0, -1.5), V2(2.67862, 4.29417)),
        new TF(TF::convergeVectorCalculator(0.0025, 0.06, 0, -1.5), V2(2.42915, 2.67359)),
        new TF(TF::convergeVectorCalculator(0.0025, 0.06, 0, -1.5), V2(2.47077, 2.66928)),
        new TF(TF::convergeVectorCalculator(0.0025, 0.06, 0, -1.5), V2(2.50716, 2.85393)),
        new TF(TF::convergeVectorCalculator(0.0025, 0.06, 0, -1.5), V2(2.53860, 3.19158)),
        new TF(TF::convergeVectorCalculator(0.0025, 0.06, 0, -1.5), V2(2.56019, 3.67453)),
        new TF(TF::convergeVectorCalculator(0.0025, 0.06, 0, -1.5), V2(2.56691, 3.57507)),
        new TF(TF::convergeVectorCalculator(0.0025, 0.06, 0, -1.5), V2(2.55321, 3.42991)),
        new TF(TF::convergeVectorCalculator(0.0025, 0.06, 0, -1.5), V2(2.51177, 3.34016)),
        new TF(TF::convergeVectorCalculator(0.0025, 0.06, 0, -1.5), V2(2.44274, 3.29420)),
        new TF(TF::convergeVectorCalculator(0.0025, 0.06, 0, -1.5), V2(2.34217, 3.28966)),
        new TF(TF::convergeVectorCalculator(0.0025, 0.06, 0, -1.5), V2(2.21626, 3.31863)),
        new TF(TF::convergeVectorCalculator(0.0025, 0.06, 0, -1.5), V2(2.17749, 3.37696)),
        new TF(TF::convergeVectorCalculator(0.0025, 0.06, 0, -1.5), V2(2.15576, 3.46041)),
        new TF(TF::convergeVectorCalculator(0.0025, 0.06, 0, -1.5), V2(2.12843, 3.56277)),
        new TF(TF::convergeVectorCalculator(0.0025, 0.06, 0, -1.5), V2(2.10442, 3.67515)),
        new TF(TF::convergeVectorCalculator(0.0025, 0.06, 0, -1.5), V2(2.08996, 3.83192)),
        new TF(TF::convergeVectorCalculator(0.0025, 0.06, 0, -1.5), V2(2.11087, 4.03625)),
        new TF(TF::convergeVectorCalculator(0.0025, 0.06, 0, -1.5), V2(2.01975, 4.32269)),
        new TF(TF::convergeVectorCalculator(0.0025, 0.06, 0, -1.5), V2(2.00000, 4.69275)),
        new TF(TF::convergeVectorCalculator(0.0025, 0.06, 0, -1.5), V2(2.00000, 4.34587)),
        new TF(TF::convergeVectorCalculator(0.0025, 0.06, 0, -1.5), V2(2.00000, 3.81794))
    })},
    {"DancingBlade.Weak", new Trajectory(0, 0, LEDGE_GRAB_MODE_AFTER, false, new Trajectory::Frames{
        new TF(TF::convergeHorizontalCalculator(0.8, 0.0025, 0, -0.06), V2(2.11648, 4.64884)),
        new TF(TF::convergeVectorCalculator(0.0025, 0.06, 0, -1.5), V2(2.51202, 5.78777)),
        new TF(TF::convergeVectorCalculator(0.0025, 0.06, 0, -1.5), V2(2.00000, 6.15807)),
        new TF(TF::convergeVectorCalculator(0.0025, 0.06, 0, -1.5), V2(2.19584, 5.88850)),
        new TF(TF::convergeVectorCalculator(0.0025, 0.06, 0, -1.5), V2(3.22828, 6.24290)),
        new TF(TF::convergeVectorCalculator(0.0025, 0.06, 0, -1.5), V2(3.11102, 5.82793)),
        new TF(TF::convergeVectorCalculator(0.0025, 0.06, 0, -1.5), V2(3.12281, 5.16819)),
        new TF(TF::convergeVectorCalculator(0.0025, 0.06, 0, -1.5), V2(2.67862, 4.29417)),
        new TF(TF::convergeVectorCalculator(0.0025, 0.06, 0, -1.5), V2(2.42915, 2.67359)),
        new TF(TF::convergeVectorCalculator(0.0025, 0.06, 0, -1.5), V2(2.47077, 2.66928)),
        new TF(TF::convergeVectorCalculator(0.0025, 0.06, 0, -1.5), V2(2.50716, 2.85393)),
        new TF(TF::convergeVectorCalculator(0.0025, 0.06, 0, -1.5), V2(2.53860, 3.19158)),
        new TF(TF::convergeVectorCalculator(0.0025, 0.06, 0, -1.5), V2(2.56019, 3.67453)),
        new TF(TF::convergeVectorCalculator(0.0025, 0.06, 0, -1.5), V2(2.56691, 3.57507)),
        new TF(TF::convergeVectorCalculator(0.0025, 0.06, 0, -1.5), V2(2.55321, 3.42991)),
        new TF(TF::convergeVectorCalculator(0.0025, 0.06, 0, -1.5), V2(2.51177, 3.34016)),
        new TF(TF::convergeVectorCalculator(0.0025, 0.06, 0, -1.5), V2(2.44274, 3.29420)),
        new TF(TF::convergeVectorCalculator(0.0025, 0.06, 0, -1.5), V2(2.34217, 3.28966)),
        new TF(TF::convergeVectorCalculator(0.0025, 0.06, 0, -1.5), V2(2.21626, 3.31863)),
        new TF(TF::convergeVectorCalculator(0.0025, 0.06, 0, -1.5), V2(2.17749, 3.37696)),
        new TF(TF::convergeVectorCalculator(0.0025, 0.06, 0, -1.5), V2(2.15576, 3.46041)),
        new TF(TF::convergeVectorCalculator(0.0025, 0.06, 0, -1.5), V2(2.12843, 3.56277)),
        new TF(TF::convergeVectorCalculator(0.0025, 0.06, 0, -1.5), V2(2.10442, 3.67515)),
        new TF(TF::convergeVectorCalculator(0.0025, 0.06, 0, -1.5), V2(2.08996, 3.83192)),
        new TF(TF::convergeVectorCalculator(0.0025, 0.06, 0, -1.5), V2(2.11087, 4.03625)),
        new TF(TF::convergeVectorCalculator(0.0025, 0.06, 0, -1.5), V2(2.01975, 4.32269)),
        new TF(TF::convergeVectorCalculator(0.0025, 0.06, 0, -1.5), V2(2.00000, 4.69275)),
        new TF(TF::convergeVectorCalculator(0.0025, 0.06, 0, -1.5), V2(2.00000, 4.34587)),
        new TF(TF::convergeVectorCalculator(0.0025, 0.06, 0, -1.5), V2(2.00000, 3.81794))
    })},
    {"DolphinSlash", new Trajectory(5, 20, LEDGE_GRAB_MODE_ALWAYS, false, new Trajectory::Frames{
        new TF(TF::convergeHorizontalCalculator(0.6666, 0.005, 0, -0.085), V2(2.55763, 2.79079)),
        new TF(TF::convergeHorizontalCalculator(1.0000, 0.005, 0, -0.170), V2(3.89811, 3.36551)),
        new TF(TF::convergeHorizontalCalculator(1.0000, 0.005, 0, -0.255), V2(3.78597, 3.35083)),
        new TF(TF::convergeHorizontalCalculator(1.0000, 0.005, 0, -0.340), V2(2.85201, 1.84816)),
        new TF(TF::convergeHorizontalCalculator(1.0000, 0.005, 0, -0.425), V2(2.86545, 2.05758)),
        new TF(TF::curveCalculator(V2(0.75685, 14.41555), 20, 0.5, true), V2(2.00000, 2.05758)),
        new TF(TF::curveCalculator(V2(0.71450, 15.51062), 20, 0.5, true), V2(2.00000, 2.05758)),
        new TF(TF::curveCalculator(V2(0.67334,  8.65633), 20, 0.5, true), V2(2.00000, 2.05758)),
        new TF(TF::curveCalculator(V2(0.63338,  2.42162), 20, 0.5, true), V2(2.00000, 2.05758)),
        new TF(TF::curveCalculator(V2(0.59462,  2.11897), 20, 0.5, true), V2(2.00000, 5.60402)),
        new TF(TF::curveCalculator(V2(0.55706,  1.83569), 20, 0.5, true), V2(2.00000, 5.61585)),
        new TF(TF::curveCalculator(V2(0.52069,  1.57181), 20, 0.5, true), V2(2.00000, 5.60775)),
        new TF(TF::curveCalculator(V2(0.48552,  1.32731), 20, 0.5, true), V2(2.00000, 5.48077)),
        new TF(TF::curveCalculator(V2(0.45155,  1.10218), 20, 0.5, true), V2(2.00000, 5.43769)),
        new TF(TF::curveCalculator(V2(0.41878,  0.89645), 20, 0.5, true), V2(2.00000, 5.49179)),
        new TF(TF::curveCalculator(V2(0.38720,  0.71010), 20, 0.5, true), V2(2.00000, 5.58387)),
        new TF(TF::curveCalculator(V2(0.35682,  0.54314), 20, 0.5, true), V2(2.00000, 5.69573)),
        new TF(TF::curveCalculator(V2(0.32765,  0.39556), 20, 0.5, true), V2(2.00000, 5.81503)),
        new TF(TF::curveCalculator(V2(0.29966,  0.26735), 20, 0.5, true), V2(2.00000, 5.93166)),
        new TF(TF::curveCalculator(V2(0.27288,  0.15855), 20, 0.5, true), V2(2.00000, 6.03653)),
        new TF(TF::curveCalculator(V2(0.24729,  0.06912), 20, 0.5, true), V2(2.01507, 6.13357)),
        new TF(TF::curveCalculator(V2(0.22290, -0.00093), 20, 0.5, true), V2(2.17595, 6.23814)),
        new TF(TF::driftCalculator(0.060, 2.5, 0.36, 0.012, 0.005, 2.5), V2(2.14967, 6.36180)),
        new TF(TF::driftCalculator(0.060, 2.5, 0.36, 0.012, 0.005, 2.5), V2(2.00000, 6.73160)),
        new TF(TF::driftCalculator(0.060, 2.5, 0.36, 0.012, 0.005, 2.5), V2(2.00000, 7.18624)),
        new TF(TF::driftCalculator(0.060, 2.5, 0.36, 0.012, 0.005, 2.5), V2(2.26172, 7.67057)),
        new TF(TF::driftCalculator(0.060, 2.5, 0.36, 0.012, 0.005, 2.5), V2(2.12479, 7.94352)),
        new TF(TF::driftCalculator(0.060, 2.5, 0.36, 0.012, 0.005, 2.5), V2(2.14861, 8.10809)),
        new TF(TF::driftCalculator(0.060, 2.5, 0.36, 0.012, 0.005, 2.5), V2(2.15951, 7.89794)),
        new TF(TF::driftCalculator(0.060, 2.5, 0.36, 0.012, 0.005, 2.5), V2(2.00510, 7.60360)),
        new TF(TF::driftCalculator(0.060, 2.5, 0.36, 0.012, 0.005, 2.5), V2(2.16192, 7.14771)),
        new TF(TF::driftCalculator(0.060, 2.5, 0.36, 0.012, 0.005, 2.5), V2(2.18233, 7.16368)),
        new TF(TF::driftCalculator(0.060, 2.5, 0.36, 0.012, 0.005, 2.5), V2(2.02592, 7.07705)),
        new TF(TF::driftCalculator(0.060, 2.5, 0.36, 0.012, 0.005, 2.5), V2(2.00000, 6.94927)),
        new TF(TF::driftCalculator(0.060, 2.5, 0.36, 0.012, 0.005, 2.5), V2(2.00000, 6.83761)),
        new TF(TF::driftCalculator(0.060, 2.5, 0.36, 0.012, 0.005, 2.5), V2(2.06701, 5.88492)),
        new TF(TF::driftCalculator(0.060, 2.5, 0.36, 0.012, 0.005, 2.5), V2(2.06290, 4.81172)),
        new TF(TF::driftCalculator(0.060, 2.5, 0.36, 0.012, 0.005, 2.5), V2(2.08376, 3.90223)),
        new TF(TF::driftCalculator(0.060, 2.5, 0.36, 0.012, 0.005, 2.5), V2(2.08591, 3.31740)),
        new TF(TF::driftCalculator(0.085, 2.5, 0.36, 0.050, 0.005, 2.5), V2(2.00000, 0.00000))
    })},
    {"AirDodge.CaptainFalcon", new Trajectory(0, 30, LEDGE_GRAB_MODE_AFTER, false, new Trajectory::Frames{
        new TF(TF::angleCalculator(2.79), V2(2.19198, 1.71249)),
        new TF(TF::multiplyCalculator(0.9), V2(2.70766, 1.52050)),
        new TF(TF::multiplyCalculator(0.9), V2(3.99360, 1.59842)),
        new TF(TF::multiplyCalculator(0.9), V2(3.54239, 1.89676)),
        new TF(TF::multiplyCalculator(0.9), V2(3.45259, 2.04046)),
        new TF(TF::multiplyCalculator(0.9), V2(3.46316, 2.03664)),
        new TF(TF::multiplyCalculator(0.9), V2(3.48000, 2.02148)),
        new TF(TF::multiplyCalculator(0.9), V2(3.49724, 1.99609)),
        new TF(TF::multiplyCalculator(0.9), V2(3.50850, 1.96184)),
        new TF(TF::multiplyCalculator(0.9), V2(3.50733, 1.92019)),
        new TF(TF::multiplyCalculator(0.9), V2(3.49551, 1.87271)),
        new TF(TF::multiplyCalculator(0.9), V2(3.48064, 1.82096)),
        new TF(TF::multiplyCalculator(0.9), V2(3.46339, 1.76649)),
        new TF(TF::multiplyCalculator(0.9), V2(3.44328, 1.71077)),
        new TF(TF::multiplyCalculator(0.9), V2(3.42102, 1.65517)),
        new TF(TF::multiplyCalculator(0.9), V2(3.39732, 1.60093)),
        new TF(TF::multiplyCalculator(0.9), V2(3.37299, 1.54913)),
        new TF(TF::multiplyCalculator(0.9), V2(3.34883, 1.50069)),
        new TF(TF::multiplyCalculator(0.9), V2(3.32508, 1.45579)),
        new TF(TF::multiplyCalculator(0.9), V2(3.30103, 1.41393)),
        new TF(TF::multiplyCalculator(0.9), V2(3.27614, 1.37497)),
        new TF(TF::multiplyCalculator(0.9), V2(3.24992, 1.33900)),
        new TF(TF::multiplyCalculator(0.9), V2(3.22189, 1.30637)),
        new TF(TF::multiplyCalculator(0.9), V2(3.19158, 1.27773)),
        new TF(TF::multiplyCalculator(0.9), V2(3.15862, 1.25412)),
        new TF(TF::multiplyCalculator(0.9), V2(3.15876, 1.24512)),
        new TF(TF::multiplyCalculator(0.9), V2(3.14336, 1.25249)),
        new TF(TF::multiplyCalculator(0.9), V2(3.08965, 1.26246)),
        new TF(TF::multiplyCalculator(0.9), V2(2.92751, 1.24179)),
        new TF(TF::driftCalculator(0.13, 2.9, 1.12, 0.06, 0.01, 2.9), V2(3.10285, 1.18593)),
        new TF(TF::driftCalculator(0.13, 2.9, 1.12, 0.06, 0.01, 2.9), V2(3.78826, 1.01859)),
        new TF(TF::driftCalculator(0.13, 2.9, 1.12, 0.06, 0.01, 2.9), V2(4.04064, 0.78171)),
        new TF(TF::driftCalculator(0.13, 2.9, 1.12, 0.06, 0.01, 2.9), V2(3.74718, 0.68125)),
        new TF(TF::driftCalculator(0.13, 2.9, 1.12, 0.06, 0.01, 2.9), V2(4.35537, 0.66297)),
        new TF(TF::driftCalculator(0.13, 2.9, 1.12, 0.06, 0.01, 2.9), V2(4.34483, 0.70879)),
        new TF(TF::driftCalculator(0.13, 2.9, 1.12, 0.06, 0.01, 2.9), V2(4.54382, 0.77920)),
        new TF(TF::driftCalculator(0.13, 2.9, 1.12, 0.06, 0.01, 2.9), V2(5.48604, 0.88132)),
        new TF(TF::driftCalculator(0.13, 2.9, 1.12, 0.06, 0.01, 2.9), V2(6.77667, 1.37548)),
        new TF(TF::driftCalculator(0.13, 2.9, 1.12, 0.06, 0.01, 2.9), V2(7.20824, 1.15218)),
        new TF(TF::driftCalculator(0.13, 2.9, 1.12, 0.06, 0.01, 2.9), V2(7.25941, 0.88259)),
        new TF(TF::driftCalculator(0.13, 2.9, 1.12, 0.06, 0.01, 2.9), V2(7.32811, 0.90241)),
        new TF(TF::driftCalculator(0.13, 2.9, 1.12, 0.06, 0.01, 2.9), V2(7.47852, 1.23590)),
        new TF(TF::driftCalculator(0.13, 2.9, 1.12, 0.06, 0.01, 2.9), V2(7.64001, 1.58950)),
        new TF(TF::driftCalculator(0.13, 2.9, 1.12, 0.06, 0.01, 2.9), V2(7.91261, 1.98573)),
        new TF(TF::driftCalculator(0.13, 2.9, 1.12, 0.06, 0.01, 2.9), V2(8.02165, 1.85700)),
        new TF(TF::driftCalculator(0.13, 2.9, 1.12, 0.06, 0.01, 2.9), V2(7.80980, 1.82112)),
        new TF(TF::driftCalculator(0.13, 2.9, 1.12, 0.06, 0.01, 2.9), V2(7.51936, 1.96707)),
        new TF(TF::driftCalculator(0.13, 2.9, 1.12, 0.06, 0.01, 2.9), V2(7.44695, 2.13247)),
        new TF(TF::driftCalculator(0.13, 2.9, 1.12, 0.06, 0.01, 2.9), V2(4.49938, 2.28119)),
        new TF(TF::driftCalculator(0.13, 2.9, 1.12, 0.06, 0.01, 2.9), V2(2.00000, 0.00000))
    })},
    {"AirDodge.Fox", new Trajectory(0, 30, LEDGE_GRAB_MODE_AFTER, false, new Trajectory::Frames{
        new TF(TF::angleCalculator(2.79), V2(2.16457, 3.92442)),
        new TF(TF::multiplyCalculator(0.9), V2(2.11403, 4.33013)),
        new TF(TF::multiplyCalculator(0.9), V2(2.41695, 4.77219)),
        new TF(TF::multiplyCalculator(0.9), V2(3.13535, 5.18834)),
        new TF(TF::multiplyCalculator(0.9), V2(2.65207, 5.39219)),
        new TF(TF::multiplyCalculator(0.9), V2(2.69824, 5.47057)),
        new TF(TF::multiplyCalculator(0.9), V2(2.76934, 5.56145)),
        new TF(TF::multiplyCalculator(0.9), V2(2.84549, 5.66789)),
        new TF(TF::multiplyCalculator(0.9), V2(2.92340, 5.79243)),
        new TF(TF::multiplyCalculator(0.9), V2(3.00013, 5.93674)),
        new TF(TF::multiplyCalculator(0.9), V2(3.07280, 6.10121)),
        new TF(TF::multiplyCalculator(0.9), V2(3.13826, 6.28493)),
        new TF(TF::multiplyCalculator(0.9), V2(3.19395, 6.48557)),
        new TF(TF::multiplyCalculator(0.9), V2(3.23783, 6.69954)),
        new TF(TF::multiplyCalculator(0.9), V2(3.26857, 6.89984)),
        new TF(TF::multiplyCalculator(0.9), V2(3.28562, 6.80956)),
        new TF(TF::multiplyCalculator(0.9), V2(3.28922, 6.71882)),
        new TF(TF::multiplyCalculator(0.9), V2(3.28040, 6.62864)),
        new TF(TF::multiplyCalculator(0.9), V2(3.26072, 6.54002)),
        new TF(TF::multiplyCalculator(0.9), V2(3.26341, 6.45395)),
        new TF(TF::multiplyCalculator(0.9), V2(3.29191, 6.37136)),
        new TF(TF::multiplyCalculator(0.9), V2(3.31947, 6.29320)),
        new TF(TF::multiplyCalculator(0.9), V2(3.34464, 6.22032)),
        new TF(TF::multiplyCalculator(0.9), V2(3.36732, 6.15352)),
        new TF(TF::multiplyCalculator(0.9), V2(3.37624, 6.09354)),
        new TF(TF::multiplyCalculator(0.9), V2(3.36275, 5.56469)),
        new TF(TF::multiplyCalculator(0.9), V2(3.64342, 5.39853)),
        new TF(TF::multiplyCalculator(0.9), V2(3.35376, 5.74801)),
        new TF(TF::multiplyCalculator(0.9), V2(3.20874, 5.72249)),
        new TF(TF::driftCalculator(0.23, 2.8, 0.83, 0.08, 0.02, 3.4), V2(3.32557, 5.93006)),
        new TF(TF::driftCalculator(0.23, 2.8, 0.83, 0.08, 0.02, 3.4), V2(3.59736, 6.35366)),
        new TF(TF::driftCalculator(0.23, 2.8, 0.83, 0.08, 0.02, 3.4), V2(3.64653, 6.82127)),
        new TF(TF::driftCalculator(0.23, 2.8, 0.83, 0.08, 0.02, 3.4), V2(3.45615, 6.36771)),
        new TF(TF::driftCalculator(0.23, 2.8, 0.83, 0.08, 0.02, 3.4), V2(3.10432, 5.61677)),
        new TF(TF::driftCalculator(0.23, 2.8, 0.83, 0.08, 0.02, 3.4), V2(2.81667, 5.18551)),
        new TF(TF::driftCalculator(0.23, 2.8, 0.83, 0.08, 0.02, 3.4), V2(2.85881, 5.09885)),
        new TF(TF::driftCalculator(0.23, 2.8, 0.83, 0.08, 0.02, 3.4), V2(3.00355, 4.93224)),
        new TF(TF::driftCalculator(0.23, 2.8, 0.83, 0.08, 0.02, 3.4), V2(2.92956, 4.39032)),
        new TF(TF::driftCalculator(0.23, 2.8, 0.83, 0.08, 0.02, 3.4), V2(2.72097, 3.82962)),
        new TF(TF::driftCalculator(0.23, 2.8, 0.83, 0.08, 0.02, 3.4), V2(2.40062, 3.47238)),
        new TF(TF::driftCalculator(0.23, 2.8, 0.83, 0.08, 0.02, 3.4), V2(2.26466, 3.40495)),
        new TF(TF::driftCalculator(0.23, 2.8, 0.83, 0.08, 0.02, 3.4), V2(2.04891, 3.28926)),
        new TF(TF::driftCalculator(0.23, 2.8, 0.83, 0.08, 0.02, 3.4), V2(2.00000, 2.99635)),
        new TF(TF::driftCalculator(0.23, 2.8, 0.83, 0.08, 0.02, 3.4), V2(2.00000, 2.21033)),
        new TF(TF::driftCalculator(0.23, 2.8, 0.83, 0.08, 0.02, 3.4), V2(2.00000, 1.10444)),
        new TF(TF::driftCalculator(0.23, 2.8, 0.83, 0.08, 0.02, 3.4), V2(2.00203, 0.45174)),
        new TF(TF::driftCalculator(0.23, 2.8, 0.83, 0.08, 0.02, 3.4), V2(2.24104, 0.24745)),
        new TF(TF::driftCalculator(0.23, 2.8, 0.83, 0.08, 0.02, 3.4), V2(2.35607, 0.22292)),
        new TF(TF::driftCalculator(0.23, 2.8, 0.83, 0.08, 0.02, 3.4), V2(2.52219, 0.29744)),
        new TF(TF::driftCalculator(0.23, 2.8, 0.83, 0.08, 0.02, 3.4), V2(2.00000, 0.00000))
    })},
    {"AirDodge.Falco", new Trajectory(0, 30, LEDGE_GRAB_MODE_AFTER, false, new Trajectory::Frames{
        new TF(TF::angleCalculator(2.79), V2(2.48025, 4.49483)),
        new TF(TF::multiplyCalculator(0.9), V2(2.42232, 4.95650)),
        new TF(TF::multiplyCalculator(0.9), V2(2.67130, 5.46427)),
        new TF(TF::multiplyCalculator(0.9), V2(3.59258, 5.94646)),
        new TF(TF::multiplyCalculator(0.9), V2(3.03883, 6.18312)),
        new TF(TF::multiplyCalculator(0.9), V2(3.09119, 6.27349)),
        new TF(TF::multiplyCalculator(0.9), V2(3.17378, 6.37852)),
        new TF(TF::multiplyCalculator(0.9), V2(3.26144, 6.50174)),
        new TF(TF::multiplyCalculator(0.9), V2(3.35108, 6.64609)),
        new TF(TF::multiplyCalculator(0.9), V2(3.43930, 6.81344)),
        new TF(TF::multiplyCalculator(0.9), V2(3.52273, 7.00423)),
        new TF(TF::multiplyCalculator(0.9), V2(3.59773, 7.21733)),
        new TF(TF::multiplyCalculator(0.9), V2(3.66305, 7.44995)),
        new TF(TF::multiplyCalculator(0.9), V2(3.76377, 7.69785)),
        new TF(TF::multiplyCalculator(0.9), V2(3.85439, 7.89222)),
        new TF(TF::multiplyCalculator(0.9), V2(3.93426, 7.78791)),
        new TF(TF::multiplyCalculator(0.9), V2(4.00364, 7.68351)),
        new TF(TF::multiplyCalculator(0.9), V2(4.06356, 7.58025)),
        new TF(TF::multiplyCalculator(0.9), V2(4.11572, 7.47930)),
        new TF(TF::multiplyCalculator(0.9), V2(4.16215, 7.38182)),
        new TF(TF::multiplyCalculator(0.9), V2(4.20547, 7.28889)),
        new TF(TF::multiplyCalculator(0.9), V2(4.24918, 7.20156)),
        new TF(TF::multiplyCalculator(0.9), V2(4.29091, 7.12077)),
        new TF(TF::multiplyCalculator(0.9), V2(4.33015, 7.04739)),
        new TF(TF::multiplyCalculator(0.9), V2(4.35334, 6.98218)),
        new TF(TF::multiplyCalculator(0.9), V2(4.20048, 6.48795)),
        new TF(TF::multiplyCalculator(0.9), V2(4.16304, 6.22487)),
        new TF(TF::multiplyCalculator(0.9), V2(4.02241, 6.03750)),
        new TF(TF::multiplyCalculator(0.9), V2(3.81269, 5.75291)),
        new TF(TF::driftCalculator(0.17, 3.1, 0.83, 0.07, 0.02, 3.5), V2(3.83350, 5.95455)),
        new TF(TF::driftCalculator(0.17, 3.1, 0.83, 0.07, 0.02, 3.5), V2(3.94944, 6.53748)),
        new TF(TF::driftCalculator(0.17, 3.1, 0.83, 0.07, 0.02, 3.5), V2(4.38557, 7.85526)),
        new TF(TF::driftCalculator(0.17, 3.1, 0.83, 0.07, 0.02, 3.5), V2(4.40381, 8.34714)),
        new TF(TF::driftCalculator(0.17, 3.1, 0.83, 0.07, 0.02, 3.5), V2(4.05082, 7.27694)),
        new TF(TF::driftCalculator(0.17, 3.1, 0.83, 0.07, 0.02, 3.5), V2(3.70259, 6.55734)),
        new TF(TF::driftCalculator(0.17, 3.1, 0.83, 0.07, 0.02, 3.5), V2(3.61841, 6.27119)),
        new TF(TF::driftCalculator(0.17, 3.1, 0.83, 0.07, 0.02, 3.5), V2(3.67048, 5.88859)),
        new TF(TF::driftCalculator(0.17, 3.1, 0.83, 0.07, 0.02, 3.5), V2(3.47167, 5.05809)),
        new TF(TF::driftCalculator(0.17, 3.1, 0.83, 0.07, 0.02, 3.5), V2(3.05985, 4.24657)),
        new TF(TF::driftCalculator(0.17, 3.1, 0.83, 0.07, 0.02, 3.5), V2(2.68229, 3.72496)),
        new TF(TF::driftCalculator(0.17, 3.1, 0.83, 0.07, 0.02, 3.5), V2(2.29235, 3.57172)),
        new TF(TF::driftCalculator(0.17, 3.1, 0.83, 0.07, 0.02, 3.5), V2(2.00000, 3.40918)),
        new TF(TF::driftCalculator(0.17, 3.1, 0.83, 0.07, 0.02, 3.5), V2(2.00000, 3.04416)),
        new TF(TF::driftCalculator(0.17, 3.1, 0.83, 0.07, 0.02, 3.5), V2(2.00000, 2.31472)),
        new TF(TF::driftCalculator(0.17, 3.1, 0.83, 0.07, 0.02, 3.5), V2(2.25421, 1.33933)),
        new TF(TF::driftCalculator(0.17, 3.1, 0.83, 0.07, 0.02, 3.5), V2(2.81720, 0.76454)),
        new TF(TF::driftCalculator(0.17, 3.1, 0.83, 0.07, 0.02, 3.5), V2(3.02380, 0.60799)),
        new TF(TF::driftCalculator(0.17, 3.1, 0.83, 0.07, 0.02, 3.5), V2(3.05401, 0.58041)),
        new TF(TF::driftCalculator(0.17, 3.1, 0.83, 0.07, 0.02, 3.5), V2(3.09125, 0.56492)),
        new TF(TF::driftCalculator(0.17, 3.1, 0.83, 0.07, 0.02, 3.5), V2(2.00000, 0.00000))
    })},
    {"AirDodge.Ganondorf", new Trajectory(0, 30, LEDGE_GRAB_MODE_AFTER, false, new Trajectory::Frames{
        new TF(TF::angleCalculator(2.79), V2(2.59177, 1.77899)),
        new TF(TF::multiplyCalculator(0.9), V2(3.17982, 1.62711)),
        new TF(TF::multiplyCalculator(0.9), V2(4.78549, 1.76878)),
        new TF(TF::multiplyCalculator(0.9), V2(4.75771, 2.13547)),
        new TF(TF::multiplyCalculator(0.9), V2(4.58875, 2.29307)),
        new TF(TF::multiplyCalculator(0.9), V2(4.60837, 2.27891)),
        new TF(TF::multiplyCalculator(0.9), V2(4.60377, 2.26287)),
        new TF(TF::multiplyCalculator(0.9), V2(4.58016, 2.23947)),
        new TF(TF::multiplyCalculator(0.9), V2(4.53546, 2.20339)),
        new TF(TF::multiplyCalculator(0.9), V2(4.47477, 2.15581)),
        new TF(TF::multiplyCalculator(0.9), V2(4.41235, 2.10234)),
        new TF(TF::multiplyCalculator(0.9), V2(4.34711, 2.04436)),
        new TF(TF::multiplyCalculator(0.9), V2(4.27515, 1.98326)),
        new TF(TF::multiplyCalculator(0.9), V2(4.19736, 1.92037)),
        new TF(TF::multiplyCalculator(0.9), V2(4.11468, 1.85699)),
        new TF(TF::multiplyCalculator(0.9), V2(4.02805, 1.79435)),
        new TF(TF::multiplyCalculator(0.9), V2(3.93848, 1.73355)),
        new TF(TF::multiplyCalculator(0.9), V2(3.84703, 1.67560)),
        new TF(TF::multiplyCalculator(0.9), V2(3.75473, 1.62136)),
        new TF(TF::multiplyCalculator(0.9), V2(3.66266, 1.57159)),
        new TF(TF::multiplyCalculator(0.9), V2(3.57080, 1.52602)),
        new TF(TF::multiplyCalculator(0.9), V2(3.47823, 1.48399)),
        new TF(TF::multiplyCalculator(0.9), V2(3.39172, 1.44572)),
        new TF(TF::multiplyCalculator(0.9), V2(3.36620, 1.41172)),
        new TF(TF::multiplyCalculator(0.9), V2(3.33957, 1.38282)),
        new TF(TF::multiplyCalculator(0.9), V2(3.36385, 1.36635)),
        new TF(TF::multiplyCalculator(0.9), V2(3.38365, 1.36165)),
        new TF(TF::multiplyCalculator(0.9), V2(3.37138, 1.35452)),
        new TF(TF::multiplyCalculator(0.9), V2(3.26395, 1.31420)),
        new TF(TF::driftCalculator(0.13, 2, 0.78, 0.06, 0.02, 2.6), V2(3.80246, 1.23733)),
        new TF(TF::driftCalculator(0.13, 2, 0.78, 0.06, 0.02, 2.6), V2(4.48754, 1.06043)),
        new TF(TF::driftCalculator(0.13, 2, 0.78, 0.06, 0.02, 2.6), V2(4.79173, 0.84507)),
        new TF(TF::driftCalculator(0.13, 2, 0.78, 0.06, 0.02, 2.6), V2(4.52046, 0.78000)),
        new TF(TF::driftCalculator(0.13, 2, 0.78, 0.06, 0.02, 2.6), V2(4.09344, 0.77279)),
        new TF(TF::driftCalculator(0.13, 2, 0.78, 0.06, 0.02, 2.6), V2(3.69267, 0.83317)),
        new TF(TF::driftCalculator(0.13, 2, 0.78, 0.06, 0.02, 2.6), V2(3.93455, 0.91995)),
        new TF(TF::driftCalculator(0.13, 2, 0.78, 0.06, 0.02, 2.6), V2(6.39376, 1.07628)),
        new TF(TF::driftCalculator(0.13, 2, 0.78, 0.06, 0.02, 2.6), V2(7.77193, 1.57231)),
        new TF(TF::driftCalculator(0.13, 2, 0.78, 0.06, 0.02, 2.6), V2(8.21386, 1.24905)),
        new TF(TF::driftCalculator(0.13, 2, 0.78, 0.06, 0.02, 2.6), V2(8.28296, 0.87450)),
        new TF(TF::driftCalculator(0.13, 2, 0.78, 0.06, 0.02, 2.6), V2(8.37049, 0.77017)),
        new TF(TF::driftCalculator(0.13, 2, 0.78, 0.06, 0.02, 2.6), V2(8.54539, 1.03821)),
        new TF(TF::driftCalculator(0.13, 2, 0.78, 0.06, 0.02, 2.6), V2(8.81359, 1.23709)),
        new TF(TF::driftCalculator(0.13, 2, 0.78, 0.06, 0.02, 2.6), V2(9.12193, 1.51423)),
        new TF(TF::driftCalculator(0.13, 2, 0.78, 0.06, 0.02, 2.6), V2(9.25282, 1.86319)),
        new TF(TF::driftCalculator(0.13, 2, 0.78, 0.06, 0.02, 2.6), V2(9.02305, 1.81719)),
        new TF(TF::driftCalculator(0.13, 2, 0.78, 0.06, 0.02, 2.6), V2(8.72926, 1.91005)),
        new TF(TF::driftCalculator(0.13, 2, 0.78, 0.06, 0.02, 2.6), V2(8.56718, 1.98293)),
        new TF(TF::driftCalculator(0.13, 2, 0.78, 0.06, 0.02, 2.6), V2(8.73237, 2.02636)),
        new TF(TF::driftCalculator(0.13, 2, 0.78, 0.06, 0.02, 2.6), V2(2.00000, 0.00000))
    })},
    {"AirDodge.Marth", new Trajectory(0, 30, LEDGE_GRAB_MODE_AFTER, false, new Trajectory::Frames{
        new TF(TF::angleCalculator(2.79), V2(2.00000, 3.76448)),
        new TF(TF::multiplyCalculator(0.9), V2(2.00000, 4.37263)),
        new TF(TF::multiplyCalculator(0.9), V2(2.00000, 5.42067)),
        new TF(TF::multiplyCalculator(0.9), V2(2.00000, 6.24982)),
        new TF(TF::multiplyCalculator(0.9), V2(2.22662, 6.33721)),
        new TF(TF::multiplyCalculator(0.9), V2(3.10381, 6.00069)),
        new TF(TF::multiplyCalculator(0.9), V2(3.46051, 6.00210)),
        new TF(TF::multiplyCalculator(0.9), V2(3.57051, 6.05722)),
        new TF(TF::multiplyCalculator(0.9), V2(3.66461, 6.07413)),
        new TF(TF::multiplyCalculator(0.9), V2(3.74475, 6.08877)),
        new TF(TF::multiplyCalculator(0.9), V2(3.81420, 6.10115)),
        new TF(TF::multiplyCalculator(0.9), V2(3.87570, 6.11132)),
        new TF(TF::multiplyCalculator(0.9), V2(3.93005, 6.11930)),
        new TF(TF::multiplyCalculator(0.9), V2(3.97820, 6.12518)),
        new TF(TF::multiplyCalculator(0.9), V2(4.02125, 6.12904)),
        new TF(TF::multiplyCalculator(0.9), V2(4.06059, 6.13098)),
        new TF(TF::multiplyCalculator(0.9), V2(4.09734, 6.13111)),
        new TF(TF::multiplyCalculator(0.9), V2(4.13162, 6.12955)),
        new TF(TF::multiplyCalculator(0.9), V2(4.16291, 6.12642)),
        new TF(TF::multiplyCalculator(0.9), V2(4.19032, 6.12186)),
        new TF(TF::multiplyCalculator(0.9), V2(4.21287, 6.11597)),
        new TF(TF::multiplyCalculator(0.9), V2(4.22979, 6.10891)),
        new TF(TF::multiplyCalculator(0.9), V2(4.24031, 6.10078)),
        new TF(TF::multiplyCalculator(0.9), V2(4.24310, 6.09173)),
        new TF(TF::multiplyCalculator(0.9), V2(4.23645, 6.08188)),
        new TF(TF::multiplyCalculator(0.9), V2(4.22857, 6.07135)),
        new TF(TF::multiplyCalculator(0.9), V2(4.23090, 6.06025)),
        new TF(TF::multiplyCalculator(0.9), V2(4.21719, 6.04871)),
        new TF(TF::multiplyCalculator(0.9), V2(4.18330, 6.02960)),
        new TF(TF::driftCalculator(0.085, 2.2, 0.9, 0.05, 0.005, 2.5), V2(4.12436, 5.98564)),
        new TF(TF::driftCalculator(0.085, 2.2, 0.9, 0.05, 0.005, 2.5), V2(4.03466, 5.92956)),
        new TF(TF::driftCalculator(0.085, 2.2, 0.9, 0.05, 0.005, 2.5), V2(3.90764, 5.87265)),
        new TF(TF::driftCalculator(0.085, 2.2, 0.9, 0.05, 0.005, 2.5), V2(3.73591, 5.75480)),
        new TF(TF::driftCalculator(0.085, 2.2, 0.9, 0.05, 0.005, 2.5), V2(3.51316, 5.53437)),
        new TF(TF::driftCalculator(0.085, 2.2, 0.9, 0.05, 0.005, 2.5), V2(3.45133, 5.28874)),
        new TF(TF::driftCalculator(0.085, 2.2, 0.9, 0.05, 0.005, 2.5), V2(3.49080, 5.03344)),
        new TF(TF::driftCalculator(0.085, 2.2, 0.9, 0.05, 0.005, 2.5), V2(3.49956, 4.78318)),
        new TF(TF::driftCalculator(0.085, 2.2, 0.9, 0.05, 0.005, 2.5), V2(3.50227, 4.56495)),
        new TF(TF::driftCalculator(0.085, 2.2, 0.9, 0.05, 0.005, 2.5), V2(3.33868, 4.40279)),
        new TF(TF::driftCalculator(0.085, 2.2, 0.9, 0.05, 0.005, 2.5), V2(2.95024, 4.31704)),
        new TF(TF::driftCalculator(0.085, 2.2, 0.9, 0.05, 0.005, 2.5), V2(2.41998, 4.26154)),
        new TF(TF::driftCalculator(0.085, 2.2, 0.9, 0.05, 0.005, 2.5), V2(2.00000, 4.17542)),
        new TF(TF::driftCalculator(0.085, 2.2, 0.9, 0.05, 0.005, 2.5), V2(2.00000, 4.05763)),
        new TF(TF::driftCalculator(0.085, 2.2, 0.9, 0.05, 0.005, 2.5), V2(2.00000, 3.91158)),
        new TF(TF::driftCalculator(0.085, 2.2, 0.9, 0.05, 0.005, 2.5), V2(2.01950, 3.74443)),
        new TF(TF::driftCalculator(0.085, 2.2, 0.9, 0.05, 0.005, 2.5), V2(2.07544, 3.56619)),
        new TF(TF::driftCalculator(0.085, 2.2, 0.9, 0.05, 0.005, 2.5), V2(2.09326, 3.35744)),
        new TF(TF::driftCalculator(0.085, 2.2, 0.9, 0.05, 0.005, 2.5), V2(2.08983, 3.19041)),
        new TF(TF::driftCalculator(0.085, 2.2, 0.9, 0.05, 0.005, 2.5), V2(2.08060, 3.08010)),
        new TF(TF::driftCalculator(0.085, 2.2, 0.9, 0.05, 0.005, 2.5), V2(2.00000, 0.00000))
    })},
    {"Drift.CaptainFalcon", new Trajectory(0, 0, LEDGE_GRAB_MODE_AFTER, false, new Trajectory::Frames{
        new TF(TF::driftCalculator(0.13, 2.9, 1.12, 0.06, 0.01, 2.9), V2(2, 0))
    })},
    {"Drift.Fox", new Trajectory(0, 0, LEDGE_GRAB_MODE_AFTER, false, new Trajectory::Frames{
        new TF(TF::driftCalculator(0.23, 2.8, 0.83, 0.08, 0.02, 3.4), V2(2, 0))
    })},
    {"Drift.Falco", new Trajectory(0, 0, LEDGE_GRAB_MODE_AFTER, false, new Trajectory::Frames{
        new TF(TF::driftCalculator(0.17, 3.1, 0.83, 0.07, 0.02, 3.5), V2(2, 0))
    })},
    {"Drift.Ganondorf", new Trajectory(0, 0, LEDGE_GRAB_MODE_AFTER, false, new Trajectory::Frames{
        new TF(TF::driftCalculator(0.13, 2, 0.78, 0.06, 0.02, 2.6), V2(2, 0))
    })},
    {"Drift.Marth", new Trajectory(0, 0, LEDGE_GRAB_MODE_AFTER, false, new Trajectory::Frames{
        new TF(TF::driftCalculator(0.085, 2.2, 0.9, 0.05, 0.005, 2.5), V2(2, 0))
    })}
};

#undef TF
#undef V2

static double getDistanceInner(const Trajectory* trajectory, const Vector2* target, const Vector2* stageVertex, const Range* frameRange, const Vector2* velocity, const Knockback* knockback, const InputFrames* inputFrames, const LedgeBox* ledgeBox, const bool ledge) {
    double totalDistance = TOO_LOW_RESULT;
    double actualDistance = 0;
    double actualHeight = 0;

    LedgeGrabMode ledgeGrabMode = trajectory->getLedgeGrabMode();
    size_t trajLength = trajectory->getLength();
    
    const long lastKey = inputFrames->getLargestKey();
    Vector2* prevVelocity = new Vector2(*velocity);

    for (long i = frameRange->begin(); i < frameRange->end(); ++i) {
        Trajectory::Frame* frame = trajectory->getFrame(i);
        Vector2* sInput = (*inputFrames)[i]->getStickInput(frame, velocity);

        if (*prevVelocity == *velocity && i >= lastKey && inputFrames->getDefaultValue()->getFrameType() == FRAME_INPUT_FORWARD && totalDistance != TOO_LOW_RESULT && knockback->getTotalDisplacement(1)->getMagnitude() == 0) {
            double extraDistance = 0;
            double extraHeight = frame->getEcb()->getY();
            if (ledge) {
                extraDistance = frame->getEcb()->getX() + ledgeBox->getHorizontal();
                extraHeight = ledgeBox->getTop();
                if (trajectory->doesRequireExtraHeight()) {
                    extraHeight -= 2;
                }
            }
            
            int multiplier = (int) ((target->getY() - actualHeight - extraHeight) / velocity->getY());
            Vector2* multipliedVelocity = new Vector2(*velocity * multiplier);
            actualDistance += multipliedVelocity->getX();
            
            totalDistance = actualDistance + extraDistance;
            break;
        }

        prevVelocity = new Vector2(*velocity);
        velocity = frame->calcVelocity(velocity, sInput);

        knockback = knockback->withAdvancedFrames(1);
        double actualXVelocity = velocity->getX() + knockback->getX();

        actualDistance += actualXVelocity;
        actualHeight += velocity->getY() + knockback->getY();

        if (stageVertex != NULL && actualDistance > stageVertex->getX() && actualHeight < stageVertex->getY()) {
            return TOO_LOW_RESULT;
        }
        
        double ecbY = frame->getEcb()->getY();
        double minExtraHeight = max(ledgeBox->getBottom(), ecbY);
        double extraDistance = 0;
        double extraHeight = ecbY;

        if (ledge) {
            extraDistance = ledgeBox->getHorizontal() + frame->getEcb()->getX();

            extraHeight = ledgeBox->getTop();
            if (actualXVelocity < 0 && actualHeight + minExtraHeight >= target->getY()) {
                extraHeight = minExtraHeight;
            } else if (trajectory->doesRequireExtraHeight() && actualXVelocity >= 0) {
                extraHeight -= 2;
            }
        }

        if (i >= trajectory->getAscentStart() && actualHeight + extraHeight >= target->getY() && (!ledge ||
                ledgeGrabMode == LEDGE_GRAB_MODE_ALWAYS ||
                ledgeGrabMode == LEDGE_GRAB_MODE_DURING && i <= trajLength - 2 ||
                ledgeGrabMode == LEDGE_GRAB_MODE_AFTER && i > trajLength - 2)) {
            totalDistance = actualDistance + extraDistance;
        } else if (i >= trajLength - 2 && ledge && ledgeGrabMode == LEDGE_GRAB_MODE_DURING && actualHeight + minExtraHeight > target->getY()) {
            return TOO_LOW_RESULT;
        } else if (i >= trajectory->getDescentStart() && actualHeight + extraHeight < target->getY()) {
            if (actualXVelocity < 0 && totalDistance != TOO_LOW_RESULT) {
                totalDistance = actualDistance + extraDistance;
            }
            break;
        }
    }
    
    return totalDistance;
}

static double getDistanceTraveledAboveTargetInner(const Trajectory* trajectory, const Vector2* target, const Vector2* stageVertex, const Range* frameRange, const Vector2* velocity, const Knockback* knockback, const InputFrames* inputFrames) {
    double totalDistance = TOO_LOW_RESULT;
    double actualDistance = 0;
    double actualHeight = 0;
    bool hitHeight = false;

    for (long i = frameRange->begin(); i < frameRange->end(); ++i) {
        Trajectory::Frame* frame = trajectory->getFrame(i);
        Vector2* sInput = (*inputFrames)[i]->getStickInput(frame, velocity);

        velocity = frame->calcVelocity(velocity, sInput);
        knockback = knockback->withAdvancedFrames(1);
        double actualXVelocity = velocity->getX() + knockback->getX();

        actualDistance += actualXVelocity;
        actualHeight += velocity->getY() + knockback->getY();

        if (stageVertex != NULL && actualDistance > stageVertex->getX() && actualHeight < stageVertex->getY()) {
            return TOO_LOW_RESULT;
        }
        
        double extraHeight = frame->getEcb()->getY();
        hitHeight |= actualHeight + extraHeight >= target->getY();

        if (actualHeight + extraHeight >= target->getY()) {
            totalDistance += actualXVelocity;
        } else if (i >= trajectory->getDescentStart() && actualHeight + extraHeight < target->getY()) {
            if (!hitHeight) {
                return TOO_LOW_RESULT;
            }
            break;
        }
    }

    return totalDistance;
}

static Vector2* getDisplacementAfterFramesInner(const Trajectory* trajectory, const Range* frameRange, const Vector2* velocity, const Knockback* knockback, const InputFrames* inputFrames) {
    Vector2* displacement = new Vector2(0, 0);

    for (int i = frameRange->begin(); i < frameRange->end(); ++i) {
        Trajectory::Frame* frame = trajectory->getFrame(i);
        Vector2* sInput = (*inputFrames)[i]->getStickInput(frame, velocity);

        velocity = frame->calcVelocity(velocity, sInput);
        displacement = &(*displacement + *velocity);
    }

    return new Vector2(*displacement + *(knockback->getTotalDisplacement(frameRange->length())));
}

static Vector2* getVelocityAfterFramesInner(const Trajectory* trajectory, const Range* frameRange, const Vector2* velocity, const InputFrames* inputFrames) {
    for (int i = frameRange->begin(); i < frameRange->end(); ++i) {
        Trajectory::Frame* frame = trajectory->getFrame(i);
        Vector2* sInput = (*inputFrames)[i]->getStickInput(frame, velocity);

        velocity = frame->calcVelocity(velocity, sInput);
    }

    return new Vector2(*velocity);
}

static double getStallDisplacementAngleInner(const Trajectory* trajectory, const Trajectory::Frame* driftFrame, const Range* frameRange, const Vector2* velocity, const Knockback* knockback, const InputFrames* inputFrames, const int jumpsGained, const Vector2* jumpVelocity) {
    Vector2* displacement = getDisplacementAfterFramesInner(trajectory, frameRange, velocity, knockback, inputFrames);
    
    double bestAngle = displacement->toAngle();
    if (jumpsGained <= 0) {
        return bestAngle;
    }

    double prevAngle = bestAngle;
    const Vector2* sInput = new Vector2(1, 0);

    for (int i = 0; i < MAX_NUM_FRAMES; ++i) {
        displacement = &(*displacement + *jumpVelocity);
        bestAngle = max(bestAngle, displacement->toAngle());
        if (prevAngle == bestAngle) {
            break;
        }
        prevAngle = bestAngle;
        jumpVelocity = driftFrame->calcVelocity(jumpVelocity, sInput);
    }

    return bestAngle;
}

static PyObject* getDescentDataInner(const Trajectory* strongStall, const Trajectory* weakStall, const Trajectory::Frame* driftFrame, const vector<double>* descentAltitudes, const Vector2* position, const Vector2* velocity, const bool charge, const int jumpsGained, const Vector2* jumpVelocity, const double minStallVelocity) {
    Vector2* newPosition = new Vector2(*position);
    Vector2* newVelocity = new Vector2(*velocity);
    Vector2* prevVelocity = new Vector2(*velocity);

    long numFrames = 0;
    const InputFrames* forwardFrames = new InputFrames(new FrameInput(FRAME_INPUT_FORWARD));
    const Vector2* forwardInput = new Vector2(1, 0);

    PyObject* result = PyDict_New();

    if (strongStall != NULL && weakStall != NULL) {
        int jumpsLeft = 0;
        
        const Vector2* stallVelocity = new Vector2(minStallVelocity, 0);
        const Range* frameRange = strongStall->getFullFrameRange();

        const Vector2* strongDisplacement = getDisplacementAfterFramesInner(strongStall, frameRange, stallVelocity, Knockback::ZERO, forwardFrames);
        const double strongAngle = getStallDisplacementAngleInner(strongStall, driftFrame, frameRange, stallVelocity, Knockback::ZERO, forwardFrames, jumpsGained, jumpVelocity);
        const Vector2* weakDisplacement = getDisplacementAfterFramesInner(weakStall, frameRange, stallVelocity, Knockback::ZERO, forwardFrames);
        const double weakAngle = getStallDisplacementAngleInner(weakStall, driftFrame, frameRange, stallVelocity, Knockback::ZERO, forwardFrames, jumpsGained, jumpVelocity);

        const Trajectory* currentStall;
        const Vector2* currentDisplacement;
        double currentAngle;
        if (charge) {
            currentStall = strongStall;
            currentDisplacement = strongDisplacement;
            currentAngle = strongAngle;
        } else {
            currentStall = weakStall;
            currentDisplacement = weakDisplacement;
            currentAngle = weakAngle;
        }

        for (int index = 0; index < descentAltitudes->size(); ++index) {
            while (numFrames < MAX_NUM_FRAMES) {
                Vector2* positionAfterDisplacement = new Vector2(newPosition->getX() - currentDisplacement->getX(), newPosition->getY() + currentDisplacement->getY());

                if (newVelocity->getY() < 0 && positionAfterDisplacement->getY() >= descentAltitudes->at(index) && newVelocity->getX() >= minStallVelocity && newVelocity->toAngle() <= currentAngle) {
                    newPosition = positionAfterDisplacement;
                    newVelocity = getVelocityAfterFramesInner(currentStall, frameRange, newVelocity, forwardFrames);
                    numFrames += (long) currentStall->getLength();
                    jumpsLeft += jumpsGained;

                    currentStall = weakStall;
                    currentDisplacement = weakDisplacement;
                    currentAngle = weakAngle;
                } else {
                    if (jumpsLeft > 0 && newVelocity->getY() < 0) {
                        newVelocity = new Vector2(*jumpVelocity);
                        jumpsLeft--;
                    } else {
                        newVelocity = driftFrame->calcVelocity(newVelocity, forwardInput);
                    }

                    Vector2* positionAfterVelocity = new Vector2(newPosition->getX() - newVelocity->getX(), newPosition->getY() + newVelocity->getY());
                    if (positionAfterVelocity->getY() < descentAltitudes->at(index)) {
                        break;
                    }
                    prevVelocity = new Vector2(*newVelocity);
                    newPosition = positionAfterVelocity;
                    numFrames++;
                }
            }

            if (numFrames >= MAX_NUM_FRAMES) {
                double multiplier = ilerp(position->getY(), newPosition->getY(), descentAltitudes->at(index));
                double newX = lerp(position->getX(), newPosition->getX(), multiplier);
                newPosition = new Vector2(newX, descentAltitudes->at(index));
                numFrames = (long) (numFrames * multiplier);
            }

            PyDict_SetItem(result, PyFloat_FromDouble(descentAltitudes->at(index)), PyTuple_Pack(3, newPosition->toPyTuple(), prevVelocity->toPyTuple(), PyLong_FromLong(numFrames)));
        }
    } else {
        for (int index = 0; index < descentAltitudes->size(); ++index) {
            while (numFrames < MAX_NUM_FRAMES) {
                newVelocity = driftFrame->calcVelocity(newVelocity, forwardInput);
                Vector2* positionAfterVelocity = new Vector2(newPosition->getX() - newVelocity->getX(), newPosition->getY() + newVelocity->getY());

                if (positionAfterVelocity->getY() < descentAltitudes->at(index)) {
                    break;
                }
                prevVelocity = new Vector2(*newVelocity);
                newPosition = positionAfterVelocity;
                numFrames++;
            }

            if (numFrames >= MAX_NUM_FRAMES) {
                double multiplier = ilerp(position->getY(), newPosition->getY(), descentAltitudes->at(index));
                double newX = lerp(position->getX(), newPosition->getX(), multiplier);
                newPosition = new Vector2(newX, descentAltitudes->at(index));
                numFrames = (long) (numFrames * multiplier);
            }

            PyDict_SetItem(result, PyFloat_FromDouble(descentAltitudes->at(index)), PyTuple_Pack(3, newPosition->toPyTuple(), prevVelocity->toPyTuple(), PyLong_FromLong(numFrames)));
        }
    }

    return result;
}

static Vector2* getHitStunPositionInner(const Trajectory::Frame* driftFrame, const Vector2* position, const Knockback* knockback, const int numFrames, const double stageEdge) {
    Knockback* actualKnockback = new Knockback(*knockback);
    double x = position->getX();
    double y = position->getY();
    double highestY = y;
    Vector2* velocity = new Vector2(0, 0);
    double actualYVelocity = 0;
    const Vector2* noInput = Vector2::ZERO;

    for (int i = 0; i < numFrames; ++i) {
        velocity = driftFrame->calcVelocity(velocity, noInput);
        actualYVelocity = velocity->getY() + knockback->getY();
        x += knockback->getX();
        y += actualYVelocity;
        highestY = max(y, highestY);

        if (y < -6 && highestY >= -6 && abs(x) < stageEdge && actualYVelocity < 0) {
            break;
        }

        knockback = knockback->withAdvancedFrames(1);
    }

    return new Vector2(x, y);
}

static PyObject* getDistance(PyObject* self, PyObject* args) {
    PyObject *targetObj, *stageVertexObj, *frameRangeObj, *velocityObj, *knockbackObj, *inputFramesObj, *ledgeBoxObj;
    int ledgeObj;
    const char* trajectoryKeyObj;
    if(!PyArg_ParseTuple(args, "sOOpOOOOO", &trajectoryKeyObj, &targetObj, &stageVertexObj, &ledgeObj, &frameRangeObj, &velocityObj, &knockbackObj, &inputFramesObj, &ledgeBoxObj)) {
        return NULL;
    }

    const Trajectory* trajectory = trajectoryMap.at(trajectoryKeyObj);
    const Vector2* target = new Vector2(targetObj);
    const Vector2* stageVertex = Py_IsNone(stageVertexObj) ? NULL : new Vector2(stageVertexObj);
    const Range* frameRange = new Range(frameRangeObj);
    const Vector2* velocity = new Vector2(velocityObj);
    const Knockback* knockback = new Knockback(knockbackObj);
    const InputFrames* inputFrames = new InputFrames(inputFramesObj, PyLong_AsLong, FrameInput::newFrameInput);
    const LedgeBox* ledgeBox = new LedgeBox(ledgeBoxObj);
    const bool ledge = (bool) ledgeObj;

    const double totalDistance = getDistanceInner(trajectory, target, stageVertex, frameRange, velocity, knockback, inputFrames, ledgeBox, ledge);
    return PyFloat_FromDouble(totalDistance);
}

static PyObject* getDistanceTraveledAboveTarget(PyObject* self, PyObject* args) {
    PyObject *targetObj, *stageVertexObj, *frameRangeObj, *velocityObj, *knockbackObj, *inputFramesObj;
    const char* trajectoryKeyObj;
    if(!PyArg_ParseTuple(args, "sOOOOOO", &trajectoryKeyObj, &targetObj, &stageVertexObj, &frameRangeObj, &velocityObj, &knockbackObj, &inputFramesObj)) {
        return NULL;
    }

    const Trajectory* trajectory = trajectoryMap.at(trajectoryKeyObj);
    const Vector2* target = new Vector2(targetObj);
    const Vector2* stageVertex = Py_IsNone(stageVertexObj) ? NULL : new Vector2(stageVertexObj);
    const Range* frameRange = new Range(frameRangeObj);
    const Vector2* velocity = new Vector2(velocityObj);
    const Knockback* knockback = new Knockback(knockbackObj);
    const InputFrames* inputFrames = new InputFrames(inputFramesObj, PyLong_AsLong, FrameInput::newFrameInput);

    const double totalDistance = getDistanceTraveledAboveTargetInner(trajectory, target, stageVertex, frameRange, velocity, knockback, inputFrames);
    return PyFloat_FromDouble(totalDistance);
}

static PyObject* getDisplacementAfterFrames(PyObject* self, PyObject* args) {
    PyObject *frameRangeObj, *velocityObj, *knockbackObj, *inputFramesObj;
    const char* trajectoryKeyObj;
    if(!PyArg_ParseTuple(args, "sOOOO", &trajectoryKeyObj, &frameRangeObj, &velocityObj, &knockbackObj, &inputFramesObj)) {
        return NULL;
    }

    const Trajectory* trajectory = trajectoryMap.at(trajectoryKeyObj);
    const Range* frameRange = new Range(frameRangeObj);
    const Vector2* velocity = new Vector2(velocityObj);
    const Knockback* knockback = new Knockback(knockbackObj);
    const InputFrames* inputFrames = new InputFrames(inputFramesObj, PyLong_AsLong, FrameInput::newFrameInput);

    const Vector2* displacement = getDisplacementAfterFramesInner(trajectory, frameRange, velocity, knockback, inputFrames);
    return displacement->toPyTuple();
}

static PyObject* getVelocityAfterFrames(PyObject* self, PyObject* args) {
    PyObject *frameRangeObj, *velocityObj, *inputFramesObj;
    const char* trajectoryKeyObj;
    if(!PyArg_ParseTuple(args, "sOOO", &trajectoryKeyObj, &frameRangeObj, &velocityObj, &inputFramesObj)) {
        return NULL;
    }

    const Trajectory* trajectory = trajectoryMap.at(trajectoryKeyObj);
    const Range* frameRange = new Range(frameRangeObj);
    const Vector2* velocity = new Vector2(velocityObj);
    const InputFrames* inputFrames = new InputFrames(inputFramesObj, PyLong_AsLong, FrameInput::newFrameInput);

    const Vector2* newVelocity = getVelocityAfterFramesInner(trajectory, frameRange, velocity, inputFrames);
    return newVelocity->toPyTuple();
}

static PyObject* getStallDisplacementAngle(PyObject* self, PyObject* args) {
    PyObject *frameRangeObj, *velocityObj, *knockbackObj, *inputFramesObj, *jumpVelocityObj;
    int jumpsGained;
    const char *trajectoryKeyObj, *driftKeyObj;
    if(!PyArg_ParseTuple(args, "ssOOOOiO", &trajectoryKeyObj, &driftKeyObj, &frameRangeObj, &velocityObj, &knockbackObj, &inputFramesObj, &jumpsGained, &jumpVelocityObj)) {
        return NULL;
    }

    const Trajectory* trajectory = trajectoryMap.at(trajectoryKeyObj);
    const Trajectory::Frame* driftFrame = trajectoryMap.at(driftKeyObj)->getFrame(0);
    const Range* frameRange = new Range(frameRangeObj);
    const Vector2* velocity = new Vector2(velocityObj);
    const Knockback* knockback = new Knockback(knockbackObj);
    const InputFrames* inputFrames = new InputFrames(inputFramesObj, PyLong_AsLong, FrameInput::newFrameInput);
    Vector2* jumpVelocity = new Vector2(jumpVelocityObj);

    const double bestAngle = getStallDisplacementAngleInner(trajectory, driftFrame, frameRange, velocity, knockback, inputFrames, jumpsGained, jumpVelocity);
    return PyFloat_FromDouble(bestAngle);
}

static PyObject* getDescentData(PyObject* self, PyObject* args) {
    PyObject *positionObj, *velocityObj, *jumpVelocityObj;
    int jumpsGained, chargeObj;
    double descentAltitude1, descentAltitude2, minStallVelocity;
    const char *strongStallKeyObj, *weakStallKeyObj, *driftKeyObj;
    if(!PyArg_ParseTuple(args, "zzsddOOpiOd", &strongStallKeyObj, &weakStallKeyObj, &driftKeyObj, &descentAltitude1, &descentAltitude2, &positionObj, &velocityObj, &chargeObj, &jumpsGained, &jumpVelocityObj, &minStallVelocity)) {
        return NULL;
    }

    const Trajectory* strongStall = strongStallKeyObj == NULL ? NULL : trajectoryMap.at(strongStallKeyObj);
    const Trajectory* weakStall = weakStallKeyObj == NULL ? NULL : trajectoryMap.at(weakStallKeyObj);
    const Trajectory::Frame* driftFrame = trajectoryMap.at(driftKeyObj)->getFrame(0);
    const Vector2* position = new Vector2(positionObj);
    const Vector2* velocity = new Vector2(velocityObj);
    bool charge = (bool) chargeObj;
    Vector2* jumpVelocity = new Vector2(jumpVelocityObj);
    
    vector<double>* descentAltitudes = new vector<double>();
    descentAltitudes->push_back(descentAltitude1);
    descentAltitudes->push_back(descentAltitude2);

    return getDescentDataInner(strongStall, weakStall, driftFrame, descentAltitudes, position, velocity, charge, jumpsGained, jumpVelocity, minStallVelocity);
}

static PyObject* getHitStunPosition(PyObject* self, PyObject* args) {
    PyObject *positionObj, *knockbackObj;
    int numFrames;
    double stageEdge;
    const char* driftKeyObj;
    if(!PyArg_ParseTuple(args, "sOOid", &driftKeyObj, &positionObj, &knockbackObj, &numFrames, &stageEdge)) {
        return NULL;
    }

    const Trajectory::Frame* driftFrame = trajectoryMap.at(driftKeyObj)->getFrame(0);
    const Vector2* position = new Vector2(positionObj);
    const Knockback* knockback = new Knockback(knockbackObj);

    const Vector2* newPosition = getHitStunPositionInner(driftFrame, position, knockback, numFrames, stageEdge);
    return newPosition->toPyTuple();
}

static PyObject* getMaxHeight(PyObject* self, PyObject* args) {
    const char* trajectoryKeyObj;
    if(!PyArg_ParseTuple(args, "s", &trajectoryKeyObj)) {
        return NULL;
    }

    const Trajectory* trajectory = trajectoryMap.at(trajectoryKeyObj);

    return PyFloat_FromDouble(trajectory->getMaxHeight());
}

static PyObject* getStallHeight(PyObject* self, PyObject* args) {
    const char* trajectoryKeyObj;
    if(!PyArg_ParseTuple(args, "s", &trajectoryKeyObj)) {
        return NULL;
    }

    const Trajectory* trajectory = trajectoryMap.at(trajectoryKeyObj);

    return PyFloat_FromDouble(trajectory->getStallHeight());
}

static PyObject* getHeightDisplacement(PyObject* self, PyObject* args) {
    const char* trajectoryKeyObj;
    if(!PyArg_ParseTuple(args, "s", &trajectoryKeyObj)) {
        return NULL;
    }

    const Trajectory* trajectory = trajectoryMap.at(trajectoryKeyObj);

    return PyFloat_FromDouble(trajectory->getHeightDisplacement());
}

static PyObject* getLength(PyObject* self, PyObject* args) {
    const char* trajectoryKeyObj;
    if(!PyArg_ParseTuple(args, "s", &trajectoryKeyObj)) {
        return NULL;
    }

    const Trajectory* trajectory = trajectoryMap.at(trajectoryKeyObj);

    return PyLong_FromSize_t(trajectory->getLength());
}

static PyObject* getRequiresExtraHeight(PyObject* self, PyObject* args) {
    const char* trajectoryKeyObj;
    if(!PyArg_ParseTuple(args, "s", &trajectoryKeyObj)) {
        return NULL;
    }

    const Trajectory* trajectory = trajectoryMap.at(trajectoryKeyObj);

    return PyBool_FromLong(trajectory->doesRequireExtraHeight());
}

static PyObject* getFadeBackInput(PyObject* self, PyObject* args) {
    PyObject *velocityObj;
    int frameNum, fadeBackObj;
    const char* trajectoryKeyObj;
    if(!PyArg_ParseTuple(args, "sOip", &trajectoryKeyObj, &velocityObj, &frameNum, &fadeBackObj)) {
        return NULL;
    }

    const Trajectory* trajectory = trajectoryMap.at(trajectoryKeyObj);
    const Vector2* velocity = new Vector2(velocityObj);
    const FrameInput* frameInput = new FrameInput(1 - fadeBackObj);

    Trajectory::Frame* frame = trajectory->getFrame(frameNum);
    Vector2* sInput = frameInput->getStickInput(frame, velocity);

    return sInput->toPyTuple();
}

static PyMethodDef trajectoryMethods[] = {
    {"get_distance", getDistance, METH_VARARGS, "Gets distance"},
    {"get_distance_traveled_above_target", getDistanceTraveledAboveTarget, METH_VARARGS, "Gets distance traveled above target"},
    {"get_displacement_after_frames", getDisplacementAfterFrames, METH_VARARGS, "Gets displacement after some number of frames"},
    {"get_velocity_after_frames", getVelocityAfterFrames, METH_VARARGS, "Gets velocity after some number of frames"},
    {"get_stall_displacement_angle", getStallDisplacementAngle, METH_VARARGS, "Gets the optimal angle of movement after performing a stall move"},
    {"get_descent_data", getDescentData, METH_VARARGS, "Gets the position, velocity, and frame duration of an ideal descent sequence"},
    {"get_hit_stun_position", getHitStunPosition, METH_VARARGS, "Gets the position of the player after all hitstun frames"},
    {"get_max_height", getMaxHeight, METH_VARARGS, "Gets maximum height"},
    {"get_stall_height", getStallHeight, METH_VARARGS, "Gets height used for calculating when to stall"},
    {"get_height_displacement", getHeightDisplacement, METH_VARARGS, "Gets height displacement after completion"},
    {"get_length", getLength, METH_VARARGS, "Gets number of frames"},
    {"get_requires_extra_height", getRequiresExtraHeight, METH_VARARGS, "Gets whether the recovery needs extra height to reach ledge properly"},
    {"get_fade_back_input", getFadeBackInput, METH_VARARGS, "Gets the input of a specific trajectory frame during recovery"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef trajectoryModule = {
    PyModuleDef_HEAD_INIT,
    "ctrajectory",
    NULL,
    -1,
    trajectoryMethods
};

PyMODINIT_FUNC PyInit_ctrajectory() {
    return PyModule_Create(&trajectoryModule);
}