from melee.enums import Character

from Chains.Abstract import SpacieApparition
from Utils import Trajectory, TrajectoryFrame as TF, Vector2 as V2
from Utils.enums import LEDGE_GRAB_MODE


class FoxIllusion(SpacieApparition):
    FULL_TRAJECTORY = Trajectory(Character.FOX, 0, 15, LEDGE_GRAB_MODE.ALWAYS, False, [
        TF(lambda v, i: V2(TF.reduce_singular(2 / 3 * v.x, 0.05), 0), V2(2, 3.50615)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.05), 0), V2(2.30477, 2.8241)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.05), 0), V2(2.43458, 2.08694)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.05), 0), V2(2.28246, 1.36353)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.05), 0), V2(2.33513, 1.35867)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.05), 0), V2(2.34783, 1.37415)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.05), 0), V2(2.35759, 1.38735)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.05), 0), V2(2.36466, 1.39845)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.05), 0), V2(2.36927, 1.40767)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.05), 0), V2(2.37167, 1.41525)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.05), 0), V2(2.3721, 1.42145)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.05), 0), V2(2.37076, 1.4265)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.05), 0), V2(2.3679, 1.43069)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.05), 0), V2(2.36374, 1.4343)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.05), 0), V2(2.3585, 1.43758)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.05), -0.01667), V2(2.35239, 1.44083)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.05), -0.03333), V2(2.16145, 1.97665)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.05), -0.05), V2(2, 2.54279)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.05), -0.06667), V2(2, 1.45539)),
        TF(lambda v, i: V2(TF.reduce_singular(v.x, 0.05), 0), V2(3.0233, 2.56316)),
        TF.fixed(V2(18.72, 0), V2(3.00192, 2.51796)),
        TF.fixed(V2(18.72, 0), V2(2.9805, 2.47445)),
        TF.fixed(V2(18.72, 0), V2(2.95905, 2.43257)),
        TF.fixed(V2(1.93, 0), V2(3.02325, 2.56327)),
        TF.fixed(V2(1.86, 0), V2(3.64085, 4.782)),
        TF.fixed(V2(1.79, 0), V2(3.69643, 4.85575)),
        TF.fixed(V2(1.72, 0), V2(3.70336, 4.81454)),
        TF.fixed(V2(1.65, 0), V2(3.70004, 4.70577)),
        TF.fixed(V2(1.58, -0.08), V2(3.6942, 4.57793)),
        TF.fixed(V2(1.51, -0.16), V2(3.69127, 4.47876)),
        TF.fixed(V2(1.44, -0.24), V2(3.69114, 4.41003)),
        TF.fixed(V2(1.37, -0.32), V2(3.68956, 4.34082)),
        TF.fixed(V2(1.3, -0.4), V2(3.68594, 4.26933)),
        TF.fixed(V2(1.23, -0.48), V2(3.68319, 4.19396)),
        TF.fixed(V2(1.16, -0.56), V2(3.68364, 4.11326)),
        TF.fixed(V2(1.09, -0.64), V2(3.68466, 4.02602)),
        TF.fixed(V2(1.02, -0.72), V2(3.68516, 3.93124)),
        TF.fixed(V2(0.95, -0.8), V2(3.68507, 3.82826)),
        TF.fixed(V2(0.88, -0.88), V2(3.68428, 3.71671)),
        TF.fixed(V2(0.81, -0.96), V2(3.68268, 3.59665)),
        TF.fixed(V2(0.74, -1.04), V2(3.68012, 3.46857)),
        TF.fixed(V2(0.67, -1.12), V2(3.67649, 3.33354)),
        TF.fixed(V2(0.6, -1.2), V2(3.67161, 3.19239)),
        TF.fixed(V2(0.53, -1.28), V2(3.66532, 3.05036)),
        TF.fixed(V2(0.46, -1.36), V2(3.65743, 2.90823)),
        TF.fixed(V2(0.39, -1.44), V2(3.64775, 2.77161)),
        TF.fixed(V2(0.32, -1.52), V2(3.63609, 2.64659)),
        TF.fixed(V2(0.25, -1.6), V2(3.6222, 2.54095)),
        TF.fixed(V2(0.18, -1.68), V2(3.60791, 2.46444)),
        TF.fixed(V2(0.11, -1.76), V2(3.44959, 2.94891)),
        TF.fixed(V2(0.04, -1.84), V2(3.30907, 3.36998)),
        TF.fixed(V2(0, -1.92), V2(3.25845, 4.34032)),
        TF.fixed(V2(0, -2), V2(3.32169, 4.54768)),
        TF.fixed(V2(0, -2.08), V2(3.27599, 5.69292)),
        TF.fixed(V2(0, -2.16), V2(3.14473, 5.97133)),
        TF.fixed(V2(0, -2.24), V2(3.19374, 4.72139)),
        TF.fixed(V2(0, -2.32), V2(3.21177, 4.73918)),
        TF.fixed(V2(0, -2.4), V2(3.41658, 5.60891)),
        TF.fixed(V2(0, -2.48), V2(3.17428, 4.585)),
        TF.fixed(V2(0, -2.56), V2(3.09681, 3.46683)),
        TF.fixed(V2(0, -2.64), V2(3.08015, 2.74863)),
        TF.fixed(V2(0, -2.72), V2(3.06682, 1.81617)),
        TF.fixed(V2(0, -2.8), V2(3.01981, 1.00061)),
        TF.drift(Character.FOX)
    ])

    LONG_TRAJECTORY = Trajectory(Character.FOX, 0, 15, LEDGE_GRAB_MODE.ALWAYS, False, FULL_TRAJECTORY.frames[:22] + FULL_TRAJECTORY.frames[23:])
    MID_TRAJECTORY = Trajectory(Character.FOX, 0, 15, LEDGE_GRAB_MODE.ALWAYS, False, FULL_TRAJECTORY.frames[:21] + FULL_TRAJECTORY.frames[23:])
    SLOW_SHORT_TRAJECTORY = Trajectory(Character.FOX, 0, 15, LEDGE_GRAB_MODE.ALWAYS, False, FULL_TRAJECTORY.frames[:20] + FULL_TRAJECTORY.frames[23:])
    FAST_SHORT_TRAJECTORY = Trajectory(Character.FOX, 0, 15, LEDGE_GRAB_MODE.ALWAYS, False, FULL_TRAJECTORY.frames[:19] + FULL_TRAJECTORY.frames[23:])

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
        return 19
