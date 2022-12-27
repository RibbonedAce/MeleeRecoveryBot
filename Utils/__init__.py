from Utils.angle import Angle
from Utils.controlstick import ControlStick
from Utils.framedataextensions import FrameDataExtensions
from Utils.frameinput import FrameInput
from Utils.gamestateextensions import GameStateExtensions
from Utils.hillclimb import HillClimb
from Utils.knockback import Knockback
from Utils.ledgebox import LedgeBox
from Utils.logutils import LogUtils
from Utils.mathutils import MathUtils
from Utils.playerstateextensions import PlayerStateExtensions
from Utils.recoverytarget import RecoveryTarget
from Utils.trajectory import Trajectory
from Utils.trajectoryframe import TrajectoryFrame
from Utils.vector2 import Vector2

FrameDataExtensions.init_extensions()
GameStateExtensions.init_extensions()
PlayerStateExtensions.init_extensions()