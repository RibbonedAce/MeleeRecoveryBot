#include <Python.h>
#include <algorithm>
#include "vector2.hpp"
#include "knockback.hpp"
#include "utils.cpp"

#define DECELERATION 0.051

using namespace std;

Knockback::Knockback(PyObject* pyObj) {
    this->vector = new Vector2(PyObject_GetAttrString(pyObj, "vector"));
}

Knockback::Knockback(Vector2* vector) {
    this->vector = vector;
}

Knockback::~Knockback() {
    delete vector;
}

double Knockback::getX() const {
    return vector->getX();
}

double Knockback::getY() const {
    return vector->getY();
}

Knockback* Knockback::withAdvancedFrames(int numFrames) const {
    return new Knockback(vector->withMagnitude(max(vector->getMagnitude() - DECELERATION * numFrames, 0.0)));
}

Vector2* Knockback::getTotalDisplacement(int numFrames) const {
    double magnitude = vector->getMagnitude();
    double endMagnitude = max(magnitude - DECELERATION * numFrames, 0.0);
    return vector->withMagnitude(linearSum(magnitude, endMagnitude, -DECELERATION));
}

const Knockback* const Knockback::ZERO = new Knockback(new Vector2(0, 0));