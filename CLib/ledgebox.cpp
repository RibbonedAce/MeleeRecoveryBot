#include <Python.h>
#include "ledgebox.hpp"

using namespace std;

LedgeBox::LedgeBox(PyObject* pyObj) {
    this->top = PyFloat_AsDouble(PyObject_GetAttrString(pyObj, "top"));
    this->bottom = PyFloat_AsDouble(PyObject_GetAttrString(pyObj, "bottom"));
    this->horizontal = PyFloat_AsDouble(PyObject_GetAttrString(pyObj, "horizontal"));
}

LedgeBox::~LedgeBox() {

}

double LedgeBox::getTop() const {
    return top;
}

double LedgeBox::getBottom() const {
    return bottom;
}

double LedgeBox::getHorizontal() const {
    return horizontal;
}