from melee.enums import ProjectileType, Action, Character

from Strategies.onlyrecover import OnlyRecover
from Utils.gamestateutils import GameStateUtils


class ESAgent:
    """
    Expert system agent for SmashBot.
    This is the "manually programmed" TAS-looking agent.
    """

    def __init__(self, dolphin, smashbot_port, opponent_port, controller, difficulty=4):
        self.smashbot_port = smashbot_port
        self.opponent_port = opponent_port
        self.controller = controller
        self.logger = dolphin.logger
        self.difficulty = difficulty

        self.gs_utils = GameStateUtils()
        self.strategy = OnlyRecover(self.logger,
                                    self.controller,
                                    self.difficulty)

    def act(self, game_state):
        known_projectiles = []
        for projectile in game_state.projectiles:
            # Held turnips
            if projectile.type == ProjectileType.TURNIP and projectile.type == 0:
                continue
            if projectile.type not in [ProjectileType.UNKNOWN_PROJECTILE, ProjectileType.PEACH_PARASOL,
                                       ProjectileType.FOX_LASER, ProjectileType.SHEIK_CHAIN,
                                       ProjectileType.SHEIK_SMOKE]:
                known_projectiles.append(projectile)
        game_state.projectiles = known_projectiles

        self.gs_utils.update_gs_custom(game_state, self.smashbot_port, self.opponent_port)

        opponent_state = game_state.player[self.opponent_port]

        # Let's treat Counter-Moves as invulnerable. So we'll know to not attack during that time
        # We consider Counter to start a frame early and a frame late
        if 4 <= opponent_state.action_frame <= 30 and \
                (opponent_state.character in [Character.ROY, Character.MARTH] and
                 opponent_state.action in [Action.MARTH_COUNTER, Action.MARTH_COUNTER_FALLING] or
                 opponent_state.character == Character.PEACH and
                 opponent_state.action in [Action.UP_B_GROUND, Action.DOWN_B_STUN]):
            game_state.player[self.opponent_port].invulnerable = True
            game_state.player[self.opponent_port].invulnerability_left = max(29 - opponent_state.action_frame,
                                                                             opponent_state.invulnerability_left)

        self.strategy.step(game_state,
                           game_state.player[self.smashbot_port],
                           game_state.player[self.opponent_port])
