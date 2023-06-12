#ifndef LEDGEBOX_H
#define LEDGEBOX_H

#include <Python.h>

class LedgeBox {
    public:
        LedgeBox(PyObject* pyObj);
        ~LedgeBox();

        double getTop() const;
        double getBottom() const;
        double getHorizontal() const;
        
    private:
        double top;
        double bottom;
        double horizontal;
};

#endif