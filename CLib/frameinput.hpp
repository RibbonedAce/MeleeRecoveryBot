#ifndef FRAMEINPUT_H
#define FRAMEINPUT_H

#include <Python.h>
#include "vector2.hpp"
#include "trajectory.hpp"

#define FRAME_INPUT_BACKWARD 0
#define FRAME_INPUT_FORWARD  1
#define FRAME_INPUT_DIRECT   2

class FrameInput {
    public:
        FrameInput(PyObject* pyObj);
        FrameInput(int frameType);
        ~FrameInput();

        Vector2* getStickInput(const Trajectory::Frame* frame, const Vector2* velocity) const;
        int getFrameType() const;
        
        static FrameInput* newFrameInput(PyObject* pyObj);

    private:
        Vector2* stickInput;
        int frameType;
};

#endif