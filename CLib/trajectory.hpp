#ifndef TRAJECTORY_H
#define TRAJECTORY_H

#include <Python.h>
#include <vector>
#include <functional>
#include "vector2.hpp"
#include "range.hpp"

#define LEDGE_GRAB_MODE_ALWAYS 0
#define LEDGE_GRAB_MODE_DURING 1
#define LEDGE_GRAB_MODE_AFTER  2

using namespace std;

typedef const double CDB;
typedef long LedgeGrabMode;
typedef function<Vector2* (const Vector2* velocity, const Vector2* sInput)> VelocityCalculator;

class Trajectory {
    public:
        class Frame {
            public:
                Frame(VelocityCalculator lambda, Vector2* ecb);
                Frame(VelocityCalculator lambda, Vector2* ecb, vector<double>* validInputs);
                Frame(Vector2* fixedVector, Vector2* ecb);
                ~Frame();

                Vector2* calcVelocity(const Vector2* velocity, const Vector2* sInput) const;
                Vector2* getEcb() const;
                vector<double>* getValidInputs() const;

                static VelocityCalculator defaultHorizontalCalculator(CDB midVel, CDB prevMidVel, CDB accel, CDB maxDev, CDB vertVel);
                static VelocityCalculator driftCalculator(CDB gravity, CDB terminalVelocity, CDB airVelocity, CDB mobility, CDB drag, CDB fastFallVelocity);
                static VelocityCalculator multiplyCalculator(CDB multiplier);
                static VelocityCalculator addCalculator(CDB addition);
                static VelocityCalculator convergeHorizontalCalculator(CDB multiplier, CDB amount, CDB singularity, CDB vertVel);
                static VelocityCalculator convergeVectorCalculator(CDB horiAmount, CDB vertAmount, CDB horiSingularity, CDB vertSingularity);
                static VelocityCalculator angleCalculator(CDB magnitude);
                static VelocityCalculator curveCalculator(const Vector2* baseVector, CDB maxDegrees, CDB inputThreshold, bool curveBounces);
                static VelocityCalculator repeatCalculator();

            private:
                VelocityCalculator lambda;
                Vector2* ecb;
                vector<double>* validInputs;

                static VelocityCalculator fixedCalculator(const Vector2* fixedVector);
                static const vector<double>* const DEFAULT_INPUTS;
        };

        typedef vector<Frame*> Frames;

        Trajectory(long ascentStart, long descentStart, LedgeGrabMode ledgeGrabMode, bool requiresExtraHeight, Frames* frames);
        ~Trajectory();

        long getAscentStart() const;
        long getDescentStart() const;
        LedgeGrabMode getLedgeGrabMode() const;
        bool doesRequireExtraHeight() const;
        double getMaxHeight() const;
        double getStallHeight() const;
        double getHeightDisplacement() const;
        Frame* getFrame(const int index) const;
        size_t getLength() const;
        Range* getFullFrameRange() const;
        Trajectory::Frames* withFrameNumbersRemoved(const int start, const int end) const;
        Trajectory::Frames* withReplacedFrame(Frame* newFrame, const int replacedIndex) const;

    private:
        long ascentStart;
        long descentStart;
        LedgeGrabMode ledgeGrabMode;
        bool requiresExtraHeight;
        Frames* frames;
        double maxHeight;
        double stallHeight;
        double heightDisplacement;
};

#endif