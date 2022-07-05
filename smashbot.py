#!/usr/bin/python3
import argparse
import cProfile
import os
import signal
import sys
from pstats import SortKey

import melee

from difficultysettings import DifficultySettings
from esagent import ESAgent
from Utils.logutils import LogUtils


def check_port(value):
    i_value = int(value)
    if i_value < 1 or i_value > 4:
        raise argparse.ArgumentTypeError("%s is an invalid controller port. \
        Must be 1, 2, 3, or 4." % value)
    return i_value

def get_character(value):
    return melee.enums.Character(int(value))

def is_dir(dir_name):
    """Checks if a path is an actual directory"""
    if not os.path.isdir(dir_name):
        msg = "{0} is not a directory".format(dir_name)
        raise argparse.ArgumentTypeError(msg)
    else:
        return dir_name


parser = argparse.ArgumentParser(description='Example of libmelee in action')
parser.add_argument('--port', '-p', type=check_port,
                    help='The controller port your AI will play on',
                    default=2)
parser.add_argument('--opponent', '-o', type=check_port,
                    help='The controller port the opponent will play on',
                    default=1)
parser.add_argument('--bot', '-b',
                    help='Opponent is a second instance of SmashBot',
                    default=False)
parser.add_argument('--debug', '-d', action='store_true',
                    help='Debug mode. Creates a CSV of all game state')
parser.add_argument('--difficulty', '-i', type=int, default=-1,
                    help='Manually specify difficulty level of SmashBot')
parser.add_argument('--dolphinexecutable', '-e', type=is_dir,
                    help='Manually specify Dolphin executable')
parser.add_argument('--stage', '-s', default="FD",
                    help='Specify which stage to select')
parser.add_argument('--profile', '-f', action='store_true',
                    help='Log profiling statistics about function call times')
parser.add_argument('--character', '-c', type=get_character,
                    help='Character that SmashBot will pick' +
                         '\nMARIO = 0' +
                         '\nFOX = 1' +
                         '\nCPTFALCON = 2' +
                         '\nDK = 3' +
                         '\nKIRBY = 4' +
                         '\nBOWSER = 5' +
                         '\nLINK = 6' +
                         '\nSHEIK = 7' +
                         '\nNESS = 8' +
                         '\nPEACH = 9' +
                         '\nPOPO = 10' +
                         '\nNANA = 11' +
                         '\nPIKACHU = 12' +
                         '\nSAMUS = 13' +
                         '\nYOSHI = 14' +
                         '\nJIGGLYPUFF = 15' +
                         '\nMEWTWO = 16' +
                         '\nLUIGI = 17' +
                         '\nMARTH = 18' +
                         '\nZELDA = 19' +
                         '\nYLINK = 20' +
                         '\nDOC = 21' +
                         '\nFALCO = 22' +
                         '\nPICHU = 23' +
                         '\nGAMEANDWATCH = 24' +
                         '\nGANONDORF = 25' +
                         '\nROY = 26',
                    default=1)

stage_dict = {
    "FD": melee.enums.Stage.FINAL_DESTINATION,
    "BF": melee.enums.Stage.BATTLEFIELD,
    "YS": melee.enums.Stage.YOSHIS_STORY,
    "FOD": melee.enums.Stage.FOUNTAIN_OF_DREAMS,
    "DL": melee.enums.Stage.DREAMLAND,
    "PS": melee.enums.Stage.POKEMON_STADIUM
}

args = parser.parse_args()

if args.debug:
    LogUtils.LOGGER = melee.logger.Logger()

# Options here are:
#    GCN_ADAPTER will use your WiiU adapter for live human-controlled play
#    UNPLUGGED is pretty obvious what it means
#    STANDARD is a named pipe input (bot)
opponent_type = melee.enums.ControllerType.STANDARD
if not args.bot:
    opponent_type = melee.enums.ControllerType.GCN_ADAPTER

# Create our console object. This will be the primary object that we will interface with
console = melee.console.Console(path=args.dolphinexecutable,
                                logger=LogUtils.LOGGER)

controller_one = melee.controller.Controller(console=console, port=args.port)
controller_two = melee.controller.Controller(console=console,
                                             port=args.opponent,
                                             type=opponent_type)

# initialize our agent
agent1 = ESAgent(args.port, args.opponent, controller_one, args.difficulty)
agent2 = None
if args.bot:
    controller_two = melee.controller.Controller(console=console, port=args.opponent)
    agent2 = ESAgent(args.opponent, args.port, controller_two, args.difficulty)

# Initialize difficulty
DifficultySettings.initialize_difficulty(args.difficulty)

def signal_handler(signal, frame):
    console.stop()
    if args.debug:
        LogUtils.LOGGER.writelog()
        print("")  # because the ^C will be on the terminal
        print("Log file created: " + LogUtils.LOGGER.filename)
    print("Shutting down cleanly...")
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

# Run dolphin
console.run()

# Connect to the console
print("Connecting to console...")
if not console.connect():
    print("ERROR: Failed to connect to the console.")
    print("\tIf you're trying to autodiscover, local firewall settings can " +
          "get in the way. Try specifying the address manually.")
    sys.exit(-1)
print("Connected")

# Plug our controller in
controller_one.connect()
controller_two.connect()

def smashbot_loop():
    # Main loop
    while True:
        # "step" to the next frame
        game_state = console.step()

        # What menu are we in?
        if game_state.menu_state == melee.enums.Menu.IN_GAME:
            try:
                agent1.act(game_state)
                if agent2:
                    agent2.act(game_state)
            except Exception as error:
                agent1.controller.empty_input()
                if agent2:
                    agent2.controller.empty_input()
                if LogUtils.LOGGER:
                    LogUtils.simple_log("Exception thrown:", repr(error))
                else:
                    raise error
            LogUtils.simple_log("Goals:", agent1.strategy)
            if LogUtils.LOGGER:
                LogUtils.LOGGER.logframe(game_state)
                LogUtils.LOGGER.writeframe()
        elif game_state.menu_state == melee.enums.Menu.CHARACTER_SELECT:
            melee.menuhelper.MenuHelper.choose_character(args.character, game_state, controller_one)
            if LogUtils.LOGGER:
                LogUtils.LOGGER.skipframe()

if args.profile:
    cProfile.run("smashbot_loop()", sort=SortKey.CUMULATIVE)
else:
    smashbot_loop()
