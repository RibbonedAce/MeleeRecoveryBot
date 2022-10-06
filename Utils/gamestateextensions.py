import csv
from collections import defaultdict

from melee import Action, Button, GameState, melee, Stage


class GameStateExtensions:
    @staticmethod
    def init_extensions():
        GameState.LEDGE_GRAB_COUNT = {1: 0, 2: 0, 3: 0, 4: 0}
        GameState.TECH_LOCKOUT = {1: 0, 2: 0, 3: 0, 4: 0}
        GameState.METEOR_JUMP_LOCKOUT = {1: 0, 2: 0, 3: 0, 4: 0}
        GameState.METEOR_SPECIAL_LOCKOUT = {1: 0, 2: 0, 3: 0, 4: 0}
        GameState.STALL_CHARGE = {1: True, 2: True, 3: True, 4: True}
        GameState.PERCENT = {1: 0, 2: 0, 3: 0, 4: 0}
        GameState.PREV_PERCENT = {1: 0, 2: 0, 3: 0, 4: 0}
        GameState.STOCK_DURATION = {1: 0, 2: 0, 3: 0, 4: 0}
        GameState.INCURRED_HITLAG = {1: 0, 2: 0, 3: 0, 4: 0}
        GameState.STAGE_DATA = GameStateExtensions.__init_stage_data()
        GameState.SMASHBOT_PORT = 0
        GameState.OPPONENT_PORT = 0

        GameState.get_stage_edge = GameStateExtensions.__get_stage_edge
        GameState.get_left_blast_zone = GameStateExtensions.__get_left_blast_zone
        GameState.get_right_blast_zone = GameStateExtensions.__get_right_blast_zone
        GameState.get_stage_ride_vertex = GameStateExtensions.__get_stage_ride_vertex
        GameState.update_custom = GameStateExtensions.__update_custom

    @staticmethod
    def __init_stage_data():
        stage_data = defaultdict(dict)

        with open("Data/other_stage_data.csv") as csv_file:
            # A list of dicts containing the data
            csv_reader = list(csv.DictReader(csv_file))
            for stage in csv_reader:
                stage_name = Stage(int(stage["Stage"]))

                stage_data[stage_name] = {"TopBlastZone": float(stage["TopBlastZone"]),
                                          "BottomBlastZone": float(stage["BottomBlastZone"]),
                                          "LeftBlastZone": float(stage["LeftBlastZone"]),
                                          "RightBlastZone": float(stage["RightBlastZone"]),
                                          "RideVertexX": float(stage["RideVertexX"]),
                                          "RideVertexY": float(stage["RideVertexY"])}

        return stage_data

    @staticmethod
    def __get_left_blast_zone(game_state):
        return GameState.STAGE_DATA[game_state.stage]["LeftBlastZone"]

    @staticmethod
    def __get_right_blast_zone(game_state):
        return GameState.STAGE_DATA[game_state.stage]["RightBlastZone"]

    @staticmethod
    def __get_stage_edge(game_state):
        return melee.stages.EDGE_GROUND_POSITION[game_state.stage]

    @staticmethod
    def __get_stage_ride_vertex(game_state):
        return GameState.STAGE_DATA[game_state.stage]["RideVertexX"], GameState.STAGE_DATA[game_state.stage]["RideVertexY"]

    @staticmethod
    def __update_custom(game_state, smashbot_port, opponent_port):
        # Save ports for easier access
        GameState.SMASHBOT_PORT = smashbot_port
        GameState.OPPONENT_PORT = opponent_port

        for port in (smashbot_port, opponent_port):
            player_state = game_state.player[port]
            controller_state = player_state.controller_state

            # Tech lockout
            if controller_state.button[Button.BUTTON_L]:
                GameState.TECH_LOCKOUT[port] = 40
            else:
                GameState.TECH_LOCKOUT[port] = max(0, GameState.TECH_LOCKOUT[port] - 1)

            # Jump meteor cancel lockout
            if controller_state.button[Button.BUTTON_Y] or \
                    controller_state.main_stick[1] > 0.8:
                GameState.METEOR_JUMP_LOCKOUT[port] = 40
            else:
                GameState.METEOR_JUMP_LOCKOUT[port] = max(0, GameState.METEOR_JUMP_LOCKOUT[port] - 1)

            # Recovery meteor cancel lockout
            if controller_state.button[Button.BUTTON_B] and \
                    controller_state.main_stick[1] > 0.8:
                GameState.METEOR_SPECIAL_LOCKOUT[port] = 40
            else:
                GameState.METEOR_SPECIAL_LOCKOUT[port] = max(0, GameState.METEOR_SPECIAL_LOCKOUT[port] - 1)

            # Stall charge
            if player_state.action == Action.SWORD_DANCE_1_AIR:
                GameState.STALL_CHARGE[port] = False
            elif player_state.action in {Action.LANDING, Action.LANDING_SPECIAL} or GameState.STOCK_DURATION[port] < 30:
                GameState.STALL_CHARGE[port] = True

            # Keep a ledge grab count
            if player_state.action == Action.EDGE_CATCHING and player_state.action_frame == 1:
                GameState.LEDGE_GRAB_COUNT[port] += 1
            if player_state.on_ground:
                GameState.LEDGE_GRAB_COUNT[port] = 0
            if game_state.frame == -123:
                GameState.LEDGE_GRAB_COUNT[port] = 0

            # Previous percent
            if player_state.percent != GameState.PERCENT[port]:
                GameState.PREV_PERCENT[port] = GameState.PERCENT[port]

            # Current percent, only stored to check for percent change
            GameState.PERCENT[port] = player_state.percent

            # How long the current stock has lasted, in frames
            GameState.STOCK_DURATION[port] += 1
            if player_state.action in {Action.DEAD_FLY_STAR, Action.DEAD_FLY_SPLATTER, Action.DEAD_FLY,
                                       Action.DEAD_LEFT, Action.DEAD_RIGHT, Action.DEAD_DOWN}:
                GameState.STOCK_DURATION[port] = 0

            # Incurred hitlag, in frames
            if player_state.hitlag_left == 0 or player_state.hitlag_left > GameState.INCURRED_HITLAG[port]:
                GameState.INCURRED_HITLAG[port] = player_state.hitlag_left