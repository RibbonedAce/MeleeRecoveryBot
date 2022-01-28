from Utils.framedataextensions import FrameDataExtensions
from Utils.gamestateextensions import GameStateExtensions
from Utils.playerstateextensions import PlayerStateExtensions

FrameDataExtensions.init_extensions()
GameStateExtensions.init_extensions()
PlayerStateExtensions.init_extensions()

LOGGER = None