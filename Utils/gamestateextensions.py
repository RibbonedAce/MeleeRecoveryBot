import csv
from collections import defaultdict

from melee import Action, Button, GameState, melee, Stage


class GameStateExtensions:
    @staticmethod
    def init_extensions():
        GameState.LEDGE_GRAB_COUNT = {1: 0, 2: 0, 3: 0, 4: 0}
        GameState.TECH_LOCKOUT = {1: 0, 2: 0, 3: 0, 4: 0}
        GameState.METEOR_JUMP_LOCKOUT = {1: 0, 2: 0, 3: 0, 4: 0}
        GameState.METEOR_FF_LOCKOUT = {1: 0, 2: 0, 3: 0, 4: 0}
        GameState.PERCENT = {1: 0, 2: 0, 3: 0, 4: 0}
        GameState.PREV_PERCENT = {1: 0, 2: 0, 3: 0, 4: 0}
        GameState.STOCK_DURATION = {1: 0, 2: 0, 3: 0, 4: 0}
        GameState.STAGE_DATA = GameStateExtensions.__init_stage_data()

        GameState.get_stage_edge = GameStateExtensions.__get_stage_edge
        GameState.get_recent_damage = GameStateExtensions.__get_recent_damage
        GameState.get_smashbot_custom = GameStateExtensions.__get_smashbot_custom
        GameState.get_opponent_custom = GameStateExtensions.__get_opponent_custom
        GameState.update_custom = GameStateExtensions.__update_custom
        GameState.get_left_blast_zone = GameStateExtensions.__get_left_blast_zone
        GameState.get_right_blast_zone = GameStateExtensions.__get_right_blast_zone

    @staticmethod
    def __init_stage_data():
        stage_data = defaultdict(dict)

        with open("Data/other_stage_data.csv") as csv_file:
            # A list of dicts containing the data
            csv_reader = list(csv.DictReader(csv_file))
            for stage in csv_reader:
                stage_name = Stage(int(stage["Stage"]))

                stage_data[stage_name] = {"Top BlastZone": float(stage["Top BlastZone"]),
                                          "Bottom BlastZone": float(stage["Bottom BlastZone"]),
                                          "Left BlastZone": float(stage["Left BlastZone"]),
                                          "Right BlastZone": float(stage["Right BlastZone"])}

        return stage_data

    @staticmethod
    def __get_left_blast_zone(game_state):
        return GameState.STAGE_DATA[game_state.stage]["Left BlastZone"]

    @staticmethod
    def __get_right_blast_zone(game_state):
        return GameState.STAGE_DATA[game_state.stage]["Right BlastZone"]

    @staticmethod
    def __get_stage_edge(game_state):
        return melee.stages.EDGE_GROUND_POSITION[game_state.stage]

    @staticmethod
    def __get_recent_damage(game_state, port):
        if game_state.custom["percent"] is None or game_state.custom["percent"][port] is None or \
                game_state.custom["prev_percent"] is None or game_state.custom["prev_percent"][port] is None:
            return 0

        return max(game_state.custom["percent"][port] - game_state.custom["prev_percent"][port], 0)

    @staticmethod
    def __get_smashbot_custom(game_state, attribute):
        return game_state.custom[attribute][game_state.custom["smashbot_port"]]

    @staticmethod
    def __get_opponent_custom(game_state, attribute):
        return game_state.custom[attribute][game_state.custom["opponent_port"]]

    @staticmethod
    def __update_custom(game_state, smashbot_port, opponent_port):
        # Save ports for easier access
        game_state.custom["smashbot_port"] = smashbot_port
        game_state.custom["opponent_port"] = opponent_port

        for port in [smashbot_port, opponent_port]:
            player_state = game_state.player[port]
            controller_state = player_state.controller_state

            # Tech lockout
            if controller_state.button[Button.BUTTON_L]:
                GameState.TECH_LOCKOUT[port] = 40
            else:
                GameState.TECH_LOCKOUT[port] -= 1
                GameState.TECH_LOCKOUT[port] = max(0, GameState.TECH_LOCKOUT[port])

            # Jump meteor cancel lockout
            if controller_state.button[Button.BUTTON_Y] or \
                    controller_state.main_stick[1] > 0.8:
                GameState.METEOR_JUMP_LOCKOUT[port] = 40
            else:
                GameState.METEOR_JUMP_LOCKOUT[port] -= 1
                GameState.METEOR_JUMP_LOCKOUT[port] = max(0, GameState.METEOR_JUMP_LOCKOUT[port])

            # Fire-fox meteor cancel lockout
            if controller_state.button[Button.BUTTON_B] and \
                    controller_state.main_stick[1] > 0.8:
                GameState.METEOR_FF_LOCKOUT[port] = 40
            else:
                GameState.METEOR_FF_LOCKOUT[port] -= 1
                GameState.METEOR_FF_LOCKOUT[port] = max(0, GameState.METEOR_FF_LOCKOUT[port])

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
            if player_state.action in [Action.DEAD_FLY_STAR, Action.DEAD_FLY_SPLATTER, Action.DEAD_FLY,
                                       Action.DEAD_LEFT, Action.DEAD_RIGHT, Action.DEAD_DOWN]:
                GameState.STOCK_DURATION[port] = 0

        game_state.custom["tech_lockout"] = GameState.TECH_LOCKOUT
        game_state.custom["meteor_jump_lockout"] = GameState.METEOR_JUMP_LOCKOUT
        game_state.custom["meteor_ff_lockout"] = GameState.METEOR_FF_LOCKOUT
        game_state.custom["ledge_grab_count"] = GameState.LEDGE_GRAB_COUNT
        game_state.custom["prev_percent"] = GameState.PREV_PERCENT
        game_state.custom["percent"] = GameState.PERCENT
        game_state.custom["stock_duration"] = GameState.STOCK_DURATION