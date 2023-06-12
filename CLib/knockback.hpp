#ifndef KNOCKBACK_H
#define KNOCKBACK_H

#include <Python.h>
#include "vector2.hpp"

class Knockback {
    public:
        Knockback(PyObject* pyObj);
        ~Knockback();

        double getX() const;
        double getY() const;
        Knockback* withAdvancedFrames(int numFrames) const;
        Vector2* getTotalDisplacement(int numFrames) const;
        
        static const Knockback* const ZERO;

    private:
        Knockback(Vector2* vector);

        Vector2* vector;
};

#endif