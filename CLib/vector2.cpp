#include <Python.h>
#include <cmath>
#include "vector2.hpp"
#include "utils.cpp"

using namespace std;

Vector2::Vector2(PyObject* pyObj) {
    this->x = PyFloat_AsDouble(PyObject_GetAttrString(pyObj, "x"));
    this->y = PyFloat_AsDouble(PyObject_GetAttrString(pyObj, "y"));
}

Vector2::Vector2(const double x, const double y) {
    this->x = x;
    this->y = y;
}

Vector2::~Vector2() {

}

double Vector2::getX() const {
    return x;
}

double Vector2::getY() const {
    return y;
}

double Vector2::toAngle() const {
    return atan2(y, x) * RAD_2_DEG;
}

double Vector2::getMagnitude() const {
    return pow(pow(x, 2) + pow(y, 2), 0.5);
}

double Vector2::getAngleBetween(const Vector2* other) const {
    return this->toAngle() - other->toAngle();
}

PyObject* Vector2::toPyTuple() const {
    return PyTuple_Pack(2, PyFloat_FromDouble(x), PyFloat_FromDouble(y));
}

Vector2* Vector2::withMagnitude(const double magnitude) const {
    if (getMagnitude() == 0) {
        return new Vector2(*ZERO);
    }
    return new Vector2(*toUnit() * magnitude);
}

Vector2* Vector2::withAngle(const double angle) const {
    return fromAngle(angle, getMagnitude());
}

Vector2* Vector2::toUnit() const { 
    return new Vector2(*this / getMagnitude());
}

Vector2* Vector2::rotatedBy(const double angle) const {
    return withAngle(toAngle() + angle);
}

Vector2 Vector2::operator+(const Vector2& other) const {
    return Vector2(this->x + other.x, this->y + other.y);
}

Vector2 Vector2::operator+(const double other) const {
    return *withMagnitude(getMagnitude() + other);
}

Vector2 Vector2::operator-(const Vector2& other) const {
    return Vector2(this->x - other.x, this->y - other.y);
}

Vector2 Vector2::operator-(const double other) const {
    return Vector2(this->x - other, this->y - other);
}

Vector2 Vector2::operator*(const double other) const {
    return Vector2(this->x * other, this->y * other);
}

Vector2 Vector2::operator/(const double other) const {
    return Vector2(this->x / other, this->y / other);
}

bool Vector2::operator==(const Vector2& other) const {
    return this->x == other.x && this->y == other.y;
}

Vector2* Vector2::fromAngle(const double angle, const double magnitude) {
    return new Vector2(cosDegrees(angle) * magnitude, sinDegrees(angle) * magnitude);
}

const Vector2* const Vector2::ZERO = new Vector2(0, 0);
