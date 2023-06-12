#ifndef RANGE_H
#define RANGE_H

#include <Python.h>

class Range {
    public:
        Range(PyObject* pyObj);
        Range(long beginInt, long endInt);
        ~Range();
        
        long begin() const;
        long end() const;
        long length() const;

    private:
        long beginInt;
        long endInt;
};

#endif