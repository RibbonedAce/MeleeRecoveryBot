#include <Python.h>
#include "range.hpp"

using namespace std;

Range::Range(PyObject* pyObj) {
    this->beginInt = PyLong_AsLong(PyObject_GetAttrString(pyObj, "start"));
    this->endInt = PyLong_AsLong(PyObject_GetAttrString(pyObj, "stop"));
}

Range::Range(long beginInt, long endInt) {
    this->beginInt = beginInt;
    this->endInt = endInt;
}

Range::~Range() {
    
}

long Range::begin() const {
    return beginInt;
}

long Range::end() const {
    return endInt;
}

long Range::length() const {
    return endInt - beginInt;
}