from melee import Character

from Chains.Abstract import DescendingBoot
from Chains.CaptainFalcon.falcondive import FalconDive
from Utils import Trajectory, TrajectoryFrame as TF, Vector2 as V2
from Utils.enums import LEDGE_GRAB_MODE


class FalconKick(DescendingBoot):
    TRAJECTORY = Trajectory(Character.CPTFALCON, 0, 12, LEDGE_GRAB_MODE.AFTER, False, [
        TF.fixed(V2(-0.31605, 0.20183), V2(4.47041, 3.04274)),
        TF.fixed(V2(-0.36565, 0.27723), V2(5.03334, 6.24597)),
        TF.fixed(V2(-0.21252, 0.33551), V2(4.68771, 6.77937)),
        TF.fixed(V2(0.24607, 0.37668), V2(4.63432, 6.64106)),
        TF.fixed(V2(0.24607, 0.40073), V2(4.60378, 6.54073)),
        TF.fixed(V2(0.24607, 0.40766), V2(4.5931, 6.47538)),
        TF.fixed(V2(0.24607, 0.39748), V2(4.59826, 6.44247)),
        TF.fixed(V2(0.24607, 0.37018), V2(4.61455, 6.43979)),
        TF.fixed(V2(0.24607, 0.32577), V2(4.63691, 6.46545)),
        TF.fixed(V2(0.24607, 0.26424), V2(4.6606, 6.51788)),
        TF.fixed(V2(0.24607, 0.18559), V2(4.67868, 6.59574)),
        TF.fixed(V2(0.24607, 0.08983), V2(4.68728, 6.6978)),
        TF.fixed(V2(0.24607, -0.02305), V2(4.68022, 6.82293)),
        TF.fixed(V2(0.24607, -0.15304), V2(4.3131, 6.02108)),
        TF.fixed(V2(0.24607, -0.30015), V2(4.20284, 4.39322)),
        TF.fixed(V2(0.24607, -0.46438), V2(4.566, 2.97842)),
        TF.fixed(V2(1.22542, -3.81748), V2(4.59141, 3.00264)),
        TF.fixed(V2(1.22542, -3.81748), V2(4.58768, 2.9976)),
        TF.fixed(V2(1.22542, -3.81748), V2(4.56623, 2.97099)),
        TF.fixed(V2(1.22542, -3.81748), V2(4.53775, 2.93158)),
        TF.fixed(V2(1.22542, -3.81748), V2(4.51244, 2.88816)),
        TF.fixed(V2(1.22542, -3.81748), V2(4.50006, 2.84911)),
        TF.fixed(V2(1.22542, -3.81748), V2(4.50323, 2.81308)),
        TF.fixed(V2(1.22542, -3.81748), V2(4.50811, 2.7735)),
        TF.fixed(V2(1.22542, -3.81748), V2(4.51366, 2.73073)),
        TF.fixed(V2(1.22542, -3.81748), V2(4.51908, 2.68511)),
        TF.fixed(V2(1.22542, -3.81748), V2(4.52399, 2.63698)),
        TF.fixed(V2(1.22542, -3.81748), V2(4.52802, 2.58667)),
        TF.fixed(V2(1.22542, -3.81748), V2(4.53086, 2.53454)),
        TF.fixed(V2(1.21542, -2.9), V2(4.65802, 2.53454)),
        TF.fixed(V2(1.20542, -2.9), V2(4.08289, 2.53454)),
        TF.fixed(V2(1.19542, -2.9), V2(3.34848, 2.53454)),
        TF.fixed(V2(1.18542, -2.9), V2(2.71397, 2.53454)),
        TF.fixed(V2(1.17542, -2.9), V2(2.41572, 2.53454)),
        TF.fixed(V2(1.16542, -2.9), V2(2.65804, 2.53454)),
        TF.fixed(V2(1.15542, -2.9), V2(2.97446, 2.53454)),
        TF.fixed(V2(1.14542, -2.9), V2(3.01314, 2.53454)),
        TF.fixed(V2(1.13542, -2.9), V2(2.86655, 2.53454)),
        TF.fixed(V2(1.12542, -2.9), V2(2.78992, 0.775)),
        TF.fixed(V2(1.11542, -2.9), V2(2.7871, 1.90425)),
        TF.fixed(V2(1.10542, -2.9), V2(2.8775, 2.67024)),
        TF.fixed(V2(1.09542, -2.9), V2(2.89241, 2.57416)),
        TF.fixed(V2(1.08542, -2.9), V2(2.95931, 0)),
        TF.fixed(V2(1.07542, -2.9), V2(2.94094, 0)),
        TF.fixed(V2(1.06542, -2.9), V2(3.0728, 2.57142)),
        TF.fixed(V2(1.05542, -2.9), V2(3.67239, 3.36185)),
        TF.fixed(V2(1.04542, -2.9), V2(4.00201, 3.54652)),
        TF.fixed(V2(1.03542, -2.9), V2(4.02197, 4.01226)),
        TF.fixed(V2(1.02542, -2.9), V2(3.82286, 2.51706)),
        TF.fixed(V2(1.01542, -2.9), V2(3.80428, 2.04388)),
        TF.fixed(V2(1.00542, -2.9), V2(3.90124, 1.68863)),
        TF.fixed(V2(0.99542, -2.9), V2(4.24667, 1.48116)),
        TF.fixed(V2(0.98542, -2.9), V2(4.58267, 1.7746)),
        TF.fixed(V2(0.97542, -2.9), V2(4.79899, 2.27834)),
        TF.fixed(V2(0.96542, -2.9), V2(4.89793, 2.78949)),
        TF.fixed(V2(0.95542, -2.9), V2(4.72794, 2.98927)),
        TF.fixed(V2(0.94542, -2.9), V2(4.32374, 2.65326)),
        TF.fixed(V2(0.93542, -2.9), V2(3.94088, 2.23287))
    ])

    @classmethod
    def create_trajectory(cls, stall_charge):
        return cls.TRAJECTORY

    @classmethod
    def _get_recovery_height(cls):
        return FalconDive.TRAJECTORY.max_height

    @classmethod
    def _get_stall_height_loss(cls):
        return cls.TRAJECTORY.height_displacement

    @classmethod
    def _get_stall_duration(cls):
        return len(cls.TRAJECTORY.frames)
