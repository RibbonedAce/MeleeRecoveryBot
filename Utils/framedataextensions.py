import csv
from collections import defaultdict, OrderedDict

from melee import Action, Character, FrameData


class FrameDataExtensions:
    @staticmethod
    def init_extensions():
        FrameData.INSTANCE = FrameData()
        FrameData.ATTACK_DATA = FrameDataExtensions.__init_attack_data()
        FrameData.CHARACTER_DATA = FrameDataExtensions.__init_character_data()

        FrameData.INSTANCE.get_weight = FrameDataExtensions.__get_weight
        FrameData.INSTANCE.get_ledge_box_bottom = FrameDataExtensions.__get_ledge_box_bottom
        FrameData.INSTANCE.get_ledge_box_top = FrameDataExtensions.__get_ledge_box_top
        FrameData.INSTANCE.get_ledge_box_horizontal = FrameDataExtensions.__get_ledge_box_horizontal
        FrameData.INSTANCE.get_air_friction = FrameDataExtensions.__get_air_friction
        FrameData.INSTANCE.get_gravity = FrameDataExtensions.__get_gravity
        FrameData.INSTANCE.get_friction = FrameDataExtensions.__get_friction
        FrameData.INSTANCE.get_fast_fall_speed = FrameDataExtensions.__get_fast_fall_speed
        FrameData.INSTANCE.get_terminal_velocity = FrameDataExtensions.__get_terminal_velocity
        FrameData.INSTANCE.get_air_mobility = FrameDataExtensions.__get_air_mobility
        FrameData.INSTANCE.get_air_speed = FrameDataExtensions.__get_air_speed

    @staticmethod
    def __init_attack_data():
        # Read extra attack data
        attack_data = defaultdict(lambda: defaultdict(list))

        def action_sort(o):
            return o[0]

        with open("Data/attack_data.csv") as csv_file:
            # A list of dicts containing the data
            csv_reader = list(csv.DictReader(csv_file))
            # Build a series of nested dicts for faster read access
            for frame in csv_reader:
                # Pull out the character, action, and frame
                character = Character(int(frame["Character"]))
                action = Action(int(frame["Action"]))
                action_frame = int(frame["Frame"])

                attack_data[character][action].append((action_frame,
                                                       {"Damage": float(frame["Damage"]),
                                                        "Angle": float(frame["Angle"]),
                                                        "KBGrowth": int(frame["KBGrowth"]),
                                                        "SetKB": int(frame["SetKB"]),
                                                        "BaseKB": int(frame["BaseKB"]),
                                                        "IASA": int(frame["IASA"]),
                                                        "LandingLag": int(frame["LandingLag"]),
                                                        "Effect": frame["Effect"],
                                                        "WeightDependent": bool(frame["WeightDependent"])}))

                attack_data[character][action].sort(key=action_sort, reverse=True)

        return attack_data

    @staticmethod
    def __init_character_data():
        # Read extra character data
        character_data = defaultdict(dict)

        with open("Data/other_character_data.csv") as csv_file:
            # A list of dicts containing the data
            csv_reader = list(csv.DictReader(csv_file))
            for line in csv_reader:
                # Pull out the character
                character = Character(int(line["Character"]))
                del line["Character"]

                # Convert all fields to numbers
                for key, value in line.items():
                    line[key] = float(value)
                character_data[character] = OrderedDict(list(FrameData.INSTANCE.characterdata.get(character, OrderedDict()).items()) + list(line.items()))
                
        return character_data

    @staticmethod
    def __get_weight(character):
        return FrameData.CHARACTER_DATA[character]["Weight"]

    @staticmethod
    def __get_ledge_box_bottom(character):
        return FrameData.CHARACTER_DATA[character]["Ledge Box Bottom"]

    @staticmethod
    def __get_ledge_box_top(character):
        return FrameData.CHARACTER_DATA[character]["Ledge Box Top"]

    @staticmethod
    def __get_ledge_box_horizontal(character):
        return FrameData.CHARACTER_DATA[character]["Ledge Box Horizontal"]

    @staticmethod
    def __get_air_friction(character):
        return FrameData.CHARACTER_DATA[character]["AirFriction"]

    @staticmethod
    def __get_gravity(character):
        return FrameData.CHARACTER_DATA[character]["Gravity"]

    @staticmethod
    def __get_friction(character):
        return FrameData.CHARACTER_DATA[character]["Friction"]

    @staticmethod
    def __get_fast_fall_speed(character):
        return FrameData.CHARACTER_DATA[character]["FastFallSpeed"]

    @staticmethod
    def __get_terminal_velocity(character):
        return FrameData.CHARACTER_DATA[character]["TerminalVelocity"]

    @staticmethod
    def __get_air_mobility(character):
        return FrameData.CHARACTER_DATA[character]["AirMobility"]

    @staticmethod
    def __get_air_speed(character):
        return FrameData.CHARACTER_DATA[character]["AirSpeed"]