from melee import Character

from Chains.Abstract import DescendingBoot
from Chains.Ganondorf import DarkDive
from Utils import Trajectory, TrajectoryFrame as TF, Vector2 as V2
from Utils.enums import LEDGE_GRAB_MODE


class WizardsFoot(DescendingBoot):
    TRAJECTORY = Trajectory(Character.GANONDORF, 0, 12, LEDGE_GRAB_MODE.AFTER, False, [
        TF.fixed(V2(-0.35189, 0.22472), V2(6.50301, 3.0182)),
        TF.fixed(V2(-0.40711, 0.30867), V2(5.89899, 6.6287)),
        TF.fixed(V2(-0.23662, 0.37356), V2(4.92789, 6.44625)),
        TF.fixed(V2(0.27398, 0.4194), V2(4.8374, 6.32632)),
        TF.fixed(V2(0.27398, 0.44617), V2(4.82417, 6.24238)),
        TF.fixed(V2(0.27398, 0.45389), V2(4.83505, 6.19056)),
        TF.fixed(V2(0.27398, 0.44256), V2(4.85714, 6.16749)),
        TF.fixed(V2(0.27398, 0.41216), V2(4.87964, 6.17036)),
        TF.fixed(V2(0.27398, 0.36271), V2(4.89534, 6.19673)),
        TF.fixed(V2(0.27398, 0.2942), V2(4.90103, 6.24451)),
        TF.fixed(V2(0.27398, 0.20664), V2(4.897, 6.31183)),
        TF.fixed(V2(0.27398, 0.10002), V2(4.90068, 6.39701)),
        TF.fixed(V2(0.27398, -0.02566), V2(4.89714, 6.498839)),
        TF.fixed(V2(0.27398, -0.1704), V2(4.69592, 5.71409)),
        TF.fixed(V2(0.27398, -0.33419), V2(4.50022, 4.75557)),
        TF.fixed(V2(0.27398, -0.51704), V2(3.99406, 3.96149)),
        TF.fixed(V2(1.36439, -3.24753), V2(3.9698, 3.94133)),
        TF.fixed(V2(1.36439, -3.24753), V2(3.94554, 3.91728)),
        TF.fixed(V2(1.36439, -3.24753), V2(3.92132, 3.88939)),
        TF.fixed(V2(1.36439, -3.24753), V2(3.89713, 3.8577)),
        TF.fixed(V2(1.36439, -3.24753), V2(3.873, 3.82227)),
        TF.fixed(V2(1.36439, -3.24753), V2(3.84897, 3.87314)),
        TF.fixed(V2(1.36439, -3.24753), V2(3.82506, 3.74035)),
        TF.fixed(V2(1.36439, -3.24753), V2(3.80128, 3.69395)),
        TF.fixed(V2(1.36439, -3.24753), V2(3.77766, 3.644)),
        TF.fixed(V2(1.36439, -3.24753), V2(3.75423, 3.59053)),
        TF.fixed(V2(1.36439, -3.24753), V2(3.731, 3.5336)),
        TF.fixed(V2(1.36439, -3.24753), V2(3.70798, 3.47325)),
        TF.fixed(V2(1.36439, -3.24753), V2(3.68521, 3.40953)),
        TF.fixed(V2(1.34439, -2), V2(4.7524, 3.40953)),
        TF.fixed(V2(1.32439, -2), V2(4.19373, 3.40953)),
        TF.fixed(V2(1.30439, -2), V2(3.51887, 3.40953)),
        TF.fixed(V2(1.28439, -2), V2(3.1158, 3.40953)),
        TF.fixed(V2(1.26439, -2), V2(2.7909, 3.40953)),
        TF.fixed(V2(1.24439, -2), V2(2.91934, 3.40953)),
        TF.fixed(V2(1.22439, -2), V2(3.43505, 3.40953)),
        TF.fixed(V2(1.20439, -2), V2(3.46271, 3.40953)),
        TF.fixed(V2(1.18439, -2), V2(3.55484, 3.40953)),
        TF.fixed(V2(1.16439, -2), V2(3.4309, 0.47813)),
        TF.fixed(V2(1.14439, -2), V2(3.6636, 2.1399)),
        TF.fixed(V2(1.12439, -2), V2(3.70756, 2.3526)),
        TF.fixed(V2(1.10439, -2), V2(3.59766, 2.07626)),
        TF.fixed(V2(1.08439, -2), V2(3.61294, 0)),
        TF.fixed(V2(1.06439, -2), V2(3.66642, 0)),
        TF.fixed(V2(1.04439, -2), V2(3.67429, 2.80553)),
        TF.fixed(V2(1.02439, -2), V2(4.07691, 3.74294)),
        TF.fixed(V2(1.00439, -2), V2(4.40622, 3.94857)),
        TF.fixed(V2(0.98439, -2), V2(4.49535, 4.4421)),
        TF.fixed(V2(0.96439, -2), V2(4.28782, 2.76543)),
        TF.fixed(V2(0.94439, -2), V2(4.29752, 2.09176)),
        TF.fixed(V2(0.92439, -2), V2(4.45649, 1.30682)),
        TF.fixed(V2(0.90439, -2), V2(4.7667, 4.06219)),
        TF.fixed(V2(0.88439, -2), V2(6.71039, 1.31285)),
        TF.fixed(V2(0.86439, -2), V2(7.0051, 1.74813)),
        TF.fixed(V2(0.84439, -2), V2(7.26999, 2.1866)),
        TF.fixed(V2(0.82439, -2), V2(7.17744, 2.56257)),
        TF.fixed(V2(0.80439, -2), V2(6.96919, 2.36125)),
        TF.fixed(V2(0.78439, -2), V2(4.73248, 2.18873))
    ])

    @classmethod
    def create_trajectory(cls, stall_charge):
        return cls.TRAJECTORY

    @classmethod
    def _get_recovery_height(cls):
        return DarkDive.TRAJECTORY.max_height

    @classmethod
    def _get_stall_height_loss(cls):
        return cls.TRAJECTORY.height_displacement

    @classmethod
    def _get_stall_duration(cls):
        return len(cls.TRAJECTORY.frames)
