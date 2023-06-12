#include <Python.h>
#include <vector>
#include <functional>
#include <algorithm>
#include "trajectory.hpp"
#include "range.hpp"
#include "utils.cpp"

#define CONTROLLER_DEAD_INPUT (38.0 / 127.0)
#define MID_NL -999
#define VELOCITY_CALCULATOR(l) [=](const Vector2* v, const Vector2* i) {l}

using namespace std;

double calculateMaxHeight(const Trajectory::Frames* frames) {
    Vector2* velocity = new Vector2(0, 0);
    double actualHeight = 0;
    double maxHeight = 0;

    const Vector2* sInput = new Vector2(0, 1);

    for (Trajectory::Frame* frame : *frames) {
        velocity = frame->calcVelocity(velocity, sInput);
        actualHeight += velocity->getY();
        maxHeight = max(actualHeight, maxHeight);
    }

    return maxHeight;
}

double calculateStallHeight(const Trajectory::Frames* frames) {
    Vector2* velocity = new Vector2(0, 0);
    double actualHeight = 0;
    double maxHeight = 0;

    const Vector2* sInput = new Vector2(1, 0);

    for (Trajectory::Frame* frame : *frames) {
        velocity = frame->calcVelocity(velocity, sInput);
        actualHeight += velocity->getY();
        maxHeight = max(actualHeight, maxHeight);
    }

    return maxHeight;
}

double calculateHeightDisplacement(const Trajectory::Frames* frames) {
    Vector2* velocity = new Vector2(0, 0);
    double actualHeight = 0;

    const Vector2* sInput = new Vector2(0, 1);

    for (Trajectory::Frame* frame : *frames) {
        velocity = frame->calcVelocity(velocity, sInput);
        actualHeight += velocity->getY();
    }

    return actualHeight;
}

Trajectory::Trajectory(long ascentStart, long descentStart, LedgeGrabMode ledgeGrabMode, bool requiresExtraHeight, Frames* frames) {
    this->frames = frames;
    this->requiresExtraHeight = requiresExtraHeight;
    this->ascentStart = ascentStart;
    this->descentStart = descentStart;
    this->ledgeGrabMode = ledgeGrabMode;
    this->maxHeight = calculateMaxHeight(frames);
    this->stallHeight = calculateStallHeight(frames);
    this->heightDisplacement = calculateHeightDisplacement(frames);
}

Trajectory::~Trajectory() {
    for (auto frame : *frames) {
        delete frame;
    }
    delete frames;
}

bool Trajectory::doesRequireExtraHeight() const {
    return requiresExtraHeight;
}

long Trajectory::getAscentStart() const {
    return ascentStart;
}

long Trajectory::getDescentStart() const {
    return descentStart;
}

long Trajectory::getLedgeGrabMode() const {
    return ledgeGrabMode;
}

double Trajectory::getMaxHeight() const {
    return maxHeight;
}

double Trajectory::getStallHeight() const {
    return stallHeight;
}

double Trajectory::getHeightDisplacement() const {
    return heightDisplacement;
}

Trajectory::Frame* Trajectory::getFrame(const int index) const {
    return (*frames)[min(index, (int) frames->size() - 1)];
}

size_t Trajectory::getLength() const {
    return frames->size();
}
        
Range* Trajectory::getFullFrameRange() const {
    return new Range(0, (long) getLength());
}

Trajectory::Frames* Trajectory::withFrameNumbersRemoved(const int start, const int end) const {
    Trajectory::Frames* newFrames = new Trajectory::Frames(*frames);
    for (int i = start; i < end; ++i) {
        delete (*newFrames)[i];
    }
    newFrames->erase(next(newFrames->begin(), start), next(newFrames->begin(), end));

    return newFrames;
}

Trajectory::Frames* Trajectory::withReplacedFrame(Frame* newFrame, const int replacedIndex) const {
    Trajectory::Frames* newFrames = new Trajectory::Frames(*frames);
    delete (*newFrames)[replacedIndex];
    (*newFrames)[replacedIndex] = newFrame;

    return newFrames;
}

Trajectory::Frame::Frame(VelocityCalculator lambda, Vector2* ecb) {
    this->lambda = lambda;
    this->ecb = ecb;
    this->validInputs = new vector<double>(*DEFAULT_INPUTS);
}

Trajectory::Frame::Frame(VelocityCalculator lambda, Vector2* ecb, vector<double>* validInputs) {
    this->lambda = lambda;
    this->ecb = ecb;
    this->validInputs = validInputs;
}

Trajectory::Frame::Frame(Vector2* fixedVector, Vector2* ecb) {
    this->lambda = fixedCalculator(fixedVector);
    this->ecb = ecb;
    this->validInputs = new vector<double>(*DEFAULT_INPUTS);
}

Trajectory::Frame::~Frame() {
    delete ecb;
}

Vector2* Trajectory::Frame::calcVelocity(const Vector2* velocity, const Vector2* sInput) const {
    return lambda(velocity, sInput);
}

Vector2* Trajectory::Frame::getEcb() const {
    return ecb;
}

vector<double>* Trajectory::Frame::getValidInputs() const {
    return validInputs;
}

VelocityCalculator Trajectory::Frame::defaultHorizontalCalculator(CDB midVel, CDB prevMidVel, CDB accel, CDB maxDev, CDB vertVel) {
    return VELOCITY_CALCULATOR(
        double normalizedInput = 0;
        if (abs(i->getX()) > CONTROLLER_DEAD_INPUT) {
            normalizedInput = i->getX();
        }

        double rawDev = v->getX() - prevMidVel + normalizedInput * accel;
        double currentDev = min(abs(rawDev), maxDev) * sign(rawDev);
        if (abs(sign(normalizedInput) - sign(currentDev)) <= 1 && abs(normalizedInput) * maxDev < abs(currentDev)) {
            currentDev = normalizedInput * maxDev;
        }

        return new Vector2(midVel + currentDev, vertVel);
    );
}

VelocityCalculator Trajectory::Frame::driftCalculator(CDB gravity, CDB terminalVelocity, CDB airVelocity, CDB mobility, CDB drag, CDB fastFallVelocity) {
    return VELOCITY_CALCULATOR(
        double velX = v->getX();
        double velY = v->getY();
        double inpX = i->getX();
        double inpY = i->getY();

        double normalizedInput = max(ilerp(CONTROLLER_DEAD_INPUT, 1, abs(inpX)), 0.0) * sign(inpX);
        double normalizedDrag = min(abs(velX), drag) * -sign(velX);
        double normalizedVelocity = airVelocity * inpX;
        double normalizedMobility = lerp(mobility / 2, mobility, abs(normalizedInput)) * sign(normalizedInput);

        double x;
        if (normalizedInput > 0 && velX > normalizedVelocity) {
            x = max(velX + normalizedDrag, normalizedVelocity);
        } else if (normalizedInput > 0 && velX <= normalizedVelocity) {
            x = min(velX + normalizedMobility, normalizedVelocity);
        } else if (normalizedInput < 0 && velX < normalizedVelocity) {
            x = min(velX + normalizedDrag, normalizedVelocity);
        } else if (normalizedInput < 0 && velX >= normalizedVelocity) {
            x = max(velX + normalizedMobility, normalizedVelocity);
        } else {
            x = velX + normalizedDrag;
        }

        double y;
        if (inpY < -0.5 && velY <= 0) {
            y = -fastFallVelocity;
        } else if (velY <= -terminalVelocity) {
            y = velY;
        } else {
            y = max(velY - gravity, -terminalVelocity);
        }

        return new Vector2(x, y);
    );
}

VelocityCalculator Trajectory::Frame::multiplyCalculator(CDB multiplier) {
    return VELOCITY_CALCULATOR(
        return new Vector2(*v * multiplier);
    );
}

VelocityCalculator Trajectory::Frame::addCalculator(CDB addition) {
    return VELOCITY_CALCULATOR(
        return new Vector2(*v + addition);
    );
}

VelocityCalculator Trajectory::Frame::convergeHorizontalCalculator(CDB multiplier, CDB amount, CDB singularity, CDB vertVel) {
    return VELOCITY_CALCULATOR(
        double horiVel = v->getX() * multiplier;
        horiVel += min(sign(singularity - horiVel) * amount, singularity - horiVel, [](CDB a, CDB b) {return abs(a) < abs(b);});
        return new Vector2(horiVel, vertVel);
    );
}

VelocityCalculator Trajectory::Frame::convergeVectorCalculator(CDB horiAmount, CDB vertAmount, CDB horiSingularity, CDB vertSingularity) {
    return VELOCITY_CALCULATOR(
        auto comp = [](CDB a, CDB b) {return abs(a) < abs(b);};
        double horiVel = v->getX() + min(sign(horiSingularity - v->getX()) * horiAmount, horiSingularity - v->getX(), comp);
        double vertVel = v->getY() + min(sign(vertSingularity - v->getY()) * vertAmount, vertSingularity - v->getY(), comp);
        return new Vector2(horiVel, vertVel);
    );
}

VelocityCalculator Trajectory::Frame::angleCalculator(CDB magnitude) {
    return VELOCITY_CALCULATOR(
        return i->withMagnitude(magnitude);
    );
}

VelocityCalculator Trajectory::Frame::repeatCalculator() {
    return VELOCITY_CALCULATOR(
        return new Vector2(*v);
    );
}

VelocityCalculator Trajectory::Frame::curveCalculator(const Vector2* baseVector, CDB maxDegrees, CDB inputThreshold, bool curveBounces) {
    return VELOCITY_CALCULATOR(
        double newDegrees = baseVector->toAngle() + max(ilerp(inputThreshold, 1, abs(i->getX())), 0.0) * sign(i->getX()) * -maxDegrees;
        if (newDegrees > 90 && curveBounces) {
            newDegrees = 180 - newDegrees;
        }

        return Vector2::fromAngle(newDegrees, baseVector->getMagnitude());
    );
}

VelocityCalculator Trajectory::Frame::fixedCalculator(const Vector2* fixedVector) {
    return VELOCITY_CALCULATOR(
        return new Vector2(*fixedVector);
    );
}

const vector<double>* const Trajectory::Frame::DEFAULT_INPUTS = new vector<double>{-1, -0.3, 0, 0.3, 1};