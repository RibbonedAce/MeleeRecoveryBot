#ifndef VECTOR2_H
#define VECTOR2_H

#include <Python.h>

class Vector2 {
    public:
        Vector2(PyObject* pyObj);
        Vector2(const double x, const double y);
        ~Vector2();

        double getX() const;
        double getY() const;
        double toAngle() const;
        double getMagnitude() const;
        double getAngleBetween(const Vector2* other) const;
        PyObject* toPyTuple() const;
        Vector2* withMagnitude(const double magnitude) const;
        Vector2* withAngle(const double angle) const;
        Vector2* toUnit() const;
        Vector2* rotatedBy(const double angle) const;

        Vector2 operator+(const Vector2& other) const;
        Vector2 operator+(const double other) const;
        Vector2 operator-(const Vector2& other) const;
        Vector2 operator-(const double other) const;
        Vector2 operator*(const double other) const;
        Vector2 operator/(const double other) const;
        bool operator==(const Vector2& other) const;

        static Vector2* fromAngle(const double angle, const double magnitude);

        static const Vector2* const ZERO;

    private:
        double x;
        double y;
};

#endif