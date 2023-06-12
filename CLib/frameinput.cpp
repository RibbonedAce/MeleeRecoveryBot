#include <Python.h>
#include <algorithm>
#include "frameinput.hpp"
#include "vector2.hpp"
#include "trajectory.hpp"
#include "utils.cpp"

using namespace std;

FrameInput::FrameInput(PyObject* pyObj) {
    this->stickInput = new Vector2(PyObject_GetAttrString(pyObj, "s_input"));
    this->frameType = PyLong_AsLong(PyObject_GetAttrString(PyObject_GetAttrString(pyObj, "f_type"), "value"));
}

FrameInput::FrameInput(int frameType) {
    this->stickInput = new Vector2(0, 0);
    this->frameType = frameType;
}

FrameInput::~FrameInput() {
    delete stickInput;
}

Vector2* FrameInput::getStickInput(const Trajectory::Frame* frame, const Vector2* velocity) const {
    auto comp = [&](const double a, const double b) {
        return frame->calcVelocity(velocity, new Vector2(a, 0))->getX() < frame->calcVelocity(velocity, new Vector2(b, 0))->getX(); 
    };

    vector<double>* inputs = frame->getValidInputs();
    if (frameType == FRAME_INPUT_BACKWARD) {
        return new Vector2(*min_element(inputs->begin(), inputs->end(), comp), 0);
    }
    if (frameType == FRAME_INPUT_FORWARD) {
        return new Vector2(*max_element(inputs->begin(), inputs->end(), comp), 0);
    }
    
    return stickInput;
}

int FrameInput::getFrameType() const {
    return frameType;
}

FrameInput* FrameInput::newFrameInput(PyObject* pyObj) {
    return new FrameInput(pyObj);
}