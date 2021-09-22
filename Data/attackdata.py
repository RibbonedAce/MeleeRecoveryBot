import csv
import os
from collections import defaultdict

from melee import Character, Action


class AttackData:
    attack_data = None

    @staticmethod
    def init_data():
        if AttackData.attack_data is not None:
            return

        AttackData.attack_data = defaultdict(lambda: defaultdict(list))

        def action_sort(o):
            return o[0]

        path = os.path.dirname(os.path.realpath(__file__))
        with open(path + "/attack_data.csv") as csv_file:
            # A list of dicts containing the data
            csv_reader = list(csv.DictReader(csv_file))
            # Build a series of nested dicts for faster read access
            for frame in csv_reader:
                # Pull out the character, action, and frame
                character = Character(int(frame["Character"]))
                action = Action(int(frame["Action"]))
                action_frame = int(frame["Frame"])

                AttackData.attack_data[character][action].append((action_frame,
                                                                  {"Damage": float(frame["Damage"]),
                                                                   "Angle": float(frame["Angle"]),
                                                                   "KB Growth": int(frame["KB Growth"]),
                                                                   "Set KB": int(frame["Set KB"]),
                                                                   "Base KB": int(frame["Base KB"]),
                                                                   "IASA": int(frame["IASA"]),
                                                                   "Landing Lag": int(frame["Landing Lag"]),
                                                                   "Effect": frame["Effect"],
                                                                   "Weight Dependent": bool(frame["Weight Dependent"])}))

                AttackData.attack_data[character][action].sort(key=action_sort, reverse=True)

    @staticmethod
    def get_attack(opponent_state):
        # Find the attack that matches the action state and frame of the opponent
        for attack in AttackData.attack_data[opponent_state.character][opponent_state.action]:
            if opponent_state.action_frame >= attack[0]:
                return attack[1]
        return None