from melee.enums import Character

from Chains.Abstract import SpacieApparition
from Utils import Trajectory, TrajectoryFrame as TF, Vector2 as V2
from Utils.enums import LEDGE_GRAB_MODE


class FalcoPhantasm(SpacieApparition):
    FULL_TRAJECTORY = Trajectory(Character.FALCO, 0, 24, LEDGE_GRAB_MODE.ALWAYS, False, [
        TF(lambda v, i: V2(TF.reduce_singular(2 / 3 * v.x, 0.05), 0), V2(2.1288, 4.01945)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.05), 0), V2(2.52756, 3.24007)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.05), 0), V2(2.48707, 2.39783)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.05), 0), V2(2.44669, 1.57153)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.05), 0), V2(2.50793, 1.56792)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.05), 0), V2(2.52137, 1.58662)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.05), 0), V2(2.53072, 1.60219)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.05), 0), V2(2.53633, 1.61497)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.05), 0), V2(2.53854, 1.62543)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.05), 0), V2(2.53774, 1.634)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.05), 0), V2(2.53423, 1.64113)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.05), 0), V2(2.52835, 1.6473)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.05), 0), V2(2.29675, 2.26603)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.05), 0), V2(2, 2.91119)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.05), 0), V2(2, 1.6679)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.05), 0), V2(3.85365, 2.93698)),
        TF.fixed(V2(16.5, 0), V2(3.82917, 2.88519)),
        TF.fixed(V2(16.5, 0), V2(3.80461, 2.8353)),
        TF.fixed(V2(16.5, 0), V2(3.78001, 2.78727)),
        TF.fixed(V2(1.93, 0), V2(3.85357, 2.93711)),
        TF.fixed(V2(1.86, 0), V2(4.12489, 5.4659)),
        TF.fixed(V2(1.79, 0), V2(4.04909, 5.54576)),
        TF.fixed(V2(1.72, 0), V2(4.05551, 5.49733)),
        TF.fixed(V2(1.65, 0), V2(4.05251, 5.37354)),
        TF.fixed(V2(1.58, -0.08), V2(4.04788, 5.22857)),
        TF.fixed(V2(1.51, -0.16), V2(4.04594, 5.11575)),
        TF.fixed(V2(1.44, -0.24), V2(4.04639, 5.037)),
        TF.fixed(V2(1.37, -0.32), V2(4.04525, 4.95768)),
        TF.fixed(V2(1.3, -0.4), V2(4.04176, 4.87577)),
        TF.fixed(V2(1.23, -0.48), V2(4.03894, 4.7894)),
        TF.fixed(V2(1.16, -0.56), V2(4.03933, 4.69693)),
        TF.fixed(V2(1.09, -0.64), V2(4.04027, 4.59695)),
        TF.fixed(V2(1.02, -0.72), V2(4.04062, 4.48837)),
        TF.fixed(V2(0.95, -0.8), V2(4.04032, 4.37038)),
        TF.fixed(V2(0.88, -0.88), V2(4.03925, 4.2426)),
        TF.fixed(V2(0.81, -0.96), V2(4.03731, 4.10508)),
        TF.fixed(V2(0.74, -1.04), V2(4.03437, 3.95841)),
        TF.fixed(V2(0.67, -1.12), V2(4.0303, 3.80382)),
        TF.fixed(V2(0.6, -1.2), V2(4.02495, 3.6433)),
        TF.fixed(V2(0.53, -1.28), V2(4.01816, 3.47978)),
        TF.fixed(V2(0.46, -1.36), V2(4.01505, 3.3173)),
        TF.fixed(V2(0.39, -1.44), V2(4.02505, 3.16124)),
        TF.fixed(V2(0.32, -1.52), V2(4.05714, 3.01864)),
        TF.fixed(V2(0.25, -1.6), V2(4.11563, 2.89843)),
        TF.fixed(V2(0.18, -1.68), V2(4.17657, 2.81184)),
        TF.fixed(V2(0.11, -1.76), V2(4.27316, 3.36983)),
        TF.fixed(V2(0.04, -1.84), V2(4.26672, 3.85816)),
        TF.fixed(V2(0, -1.92), V2(4.15292, 4.97776)),
        TF.fixed(V2(0, -2), V2(4.18509, 5.21088)),
        TF.fixed(V2(0, -2.08), V2(4.22651, 6.25313)),
        TF.fixed(V2(0, -2.16), V2(4.10917, 7.01115)),
        TF.fixed(V2(0, -2.24), V2(3.90833, 5.72179)),
        TF.fixed(V2(0, -2.32), V2(3.7981, 5.75143)),
        TF.fixed(V2(0, -2.4), V2(3.90985, 6.67566)),
        TF.fixed(V2(0, -2.48), V2(3.47979, 5.24105)),
        TF.fixed(V2(0, -2.56), V2(3.3839, 3.96497)),
        TF.fixed(V2(0, -2.64), V2(3.36013, 3.14971)),
        TF.fixed(V2(0, -2.72), V2(3.35086, 2.08666)),
        TF.fixed(V2(0, -2.8), V2(3.31787, 1.15199)),
        TF.drift(Character.FALCO)
    ])

    LONG_TRAJECTORY = Trajectory(Character.FALCO, 0, 24, LEDGE_GRAB_MODE.ALWAYS, False, FULL_TRAJECTORY.frames[:18] + FULL_TRAJECTORY.frames[19:])
    MID_TRAJECTORY = Trajectory(Character.FALCO, 0, 24, LEDGE_GRAB_MODE.ALWAYS, False, FULL_TRAJECTORY.frames[:17] + FULL_TRAJECTORY.frames[19:])
    SLOW_SHORT_TRAJECTORY = Trajectory(Character.FALCO, 0, 24, LEDGE_GRAB_MODE.ALWAYS, False, FULL_TRAJECTORY.frames[:16] + FULL_TRAJECTORY.frames[19:])
    FAST_SHORT_TRAJECTORY = Trajectory(Character.FALCO, 0, 24, LEDGE_GRAB_MODE.ALWAYS, False, FULL_TRAJECTORY.frames[:15] + FULL_TRAJECTORY.frames[19:])

    @classmethod
    def create_trajectory(cls, character):
        return cls.FULL_TRAJECTORY

    @classmethod
    def create_shorten_trajectory(cls, amount):
        if amount == 1:
            return cls.LONG_TRAJECTORY
        if amount == 2:
            return cls.MID_TRAJECTORY
        if amount == 3:
            return cls.SLOW_SHORT_TRAJECTORY
        if amount == 4:
            return cls.FAST_SHORT_TRAJECTORY
        return cls.FULL_TRAJECTORY

    @classmethod
    def _get_shorten_frame(cls):
        return 15