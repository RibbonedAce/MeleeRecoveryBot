from melee import Action, Button, melee


class GameStateUtils:
    @staticmethod
    def get_stage_edge(game_state):
        return melee.stages.EDGE_GROUND_POSITION[game_state.stage]

    @staticmethod
    def get_recent_damage(game_state, port):
        if game_state.custom["percent"] is None or game_state.custom["percent"][port] is None or \
                game_state.custom["prev_percent"] is None or game_state.custom["prev_percent"][port] is None:
            return 0

        return max(game_state.custom["percent"][port] - game_state.custom["prev_percent"][port], 0)

    @staticmethod
    def get_smashbot_custom(game_state, attribute):
        return game_state.custom[attribute][game_state.custom["smashbot_port"]]

    @staticmethod
    def get_opponent_custom(game_state, attribute):
        return game_state.custom[attribute][game_state.custom["opponent_port"]]

    def __init__(self):
        self.ledge_grab_count = {1: 0, 2: 0, 3: 0, 4: 0}
        self.tech_lockout = {1: 0, 2: 0, 3: 0, 4: 0}
        self.meteor_jump_lockout = {1: 0, 2: 0, 3: 0, 4: 0}
        self.meteor_ff_lockout = {1: 0, 2: 0, 3: 0, 4: 0}
        self.percent = {1: 0, 2: 0, 3: 0, 4: 0}
        self.prev_percent = {1: 0, 2: 0, 3: 0, 4: 0}
        self.stock_duration = {1: 0, 2: 0, 3: 0, 4: 0}

    def update_gs_custom(self, game_state, smashbot_port, opponent_port):
        # Save ports for easier access
        game_state.custom["smashbot_port"] = smashbot_port
        game_state.custom["opponent_port"] = opponent_port


        for port in [smashbot_port, opponent_port]:
            player_state = game_state.player[port]
            controller_state = player_state.controller_state

            # Tech lockout
            if controller_state.button[Button.BUTTON_L]:
                self.tech_lockout[port] = 40
            else:
                self.tech_lockout[port] -= 1
                self.tech_lockout[port] = max(0, self.tech_lockout[port])

            # Jump meteor cancel lockout
            if controller_state.button[Button.BUTTON_Y] or \
                    controller_state.main_stick[1] > 0.8:
                self.meteor_jump_lockout[port] = 40
            else:
                self.meteor_jump_lockout[port] -= 1
                self.meteor_jump_lockout[port] = max(0, self.meteor_jump_lockout[port])

            # Fire-fox meteor cancel lockout
            if controller_state.button[Button.BUTTON_B] and \
                    controller_state.main_stick[1] > 0.8:
                self.meteor_ff_lockout[port] = 40
            else:
                self.meteor_ff_lockout[port] -= 1
                self.meteor_ff_lockout[port] = max(0, self.meteor_ff_lockout[port])

            # Keep a ledge grab count
            if player_state.action == Action.EDGE_CATCHING and player_state.action_frame == 1:
                self.ledge_grab_count[port] += 1
            if player_state.on_ground:
                self.ledge_grab_count[port] = 0
            if game_state.frame == -123:
                self.ledge_grab_count[port] = 0

            # Previous percent
            if player_state.percent != self.percent[port]:
                self.prev_percent[port] = self.percent[port]

            # Current percent, only stored to check for percent change
            self.percent[port] = player_state.percent

            # How long the current stock has lasted, in frames
            self.stock_duration[port] += 1
            if player_state.action in [Action.DEAD_FLY_STAR, Action.DEAD_FLY_SPLATTER, Action.DEAD_FLY,
                                       Action.DEAD_LEFT, Action.DEAD_RIGHT, Action.DEAD_DOWN]:
                self.stock_duration[port] = 0

        game_state.custom["tech_lockout"] = self.tech_lockout
        game_state.custom["meteor_jump_lockout"] = self.meteor_jump_lockout
        game_state.custom["meteor_ff_lockout"] = self.meteor_ff_lockout
        game_state.custom["ledge_grab_count"] = self.ledge_grab_count
        game_state.custom["prev_percent"] = self.prev_percent
        game_state.custom["percent"] = self.percent
        game_state.custom["stock_duration"] = self.stock_duration