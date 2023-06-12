#ifndef C_UTILS
#define C_UTILS

#include <iostream>
#include <cmath>
#include <type_traits>

#define DEG_2_RAD 0.01745329251
#define RAD_2_DEG 57.2957795131

using namespace std;

// THIS WILL SLOW DOWN THE BOT A LOT, ONLY SET TO TRUE FOR DEBUGGING C++ CRASHES
static bool shouldLog = true;

template<typename T> static void logCode(T text) {
    if (shouldLog) {
        cout << "C++: " << text << endl;
    }
}   

static double lerp(const double a, const double b, const double x) {
    return a * (1 - x) + b * x;
}

static double ilerp(const double a, const double b, const double c) {
    return (c - a) / (b - a);
}

static double sign(const double x) {
    return (x > 0) - (x < 0);
}

static double linearSum(const double start, const double end, const double increase) {
    double mEnd = end / abs(increase);
    double mStart = start / abs(increase);
    return ((mEnd + 1) * mEnd / 2 - (mStart + 1) * mStart / 2) * increase;
}

static double cosDegrees(const double degrees) {
    return cos(degrees * DEG_2_RAD);
}

static double sinDegrees(const double degrees) {
    return sin(degrees * DEG_2_RAD);
}

#endif