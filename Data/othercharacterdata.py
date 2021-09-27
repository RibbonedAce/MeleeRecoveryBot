import csv
import os
from collections import defaultdict

from melee import Character


class OtherCharacterData:
    character_data = None

    @staticmethod
    def init_data():
        if OtherCharacterData.character_data is not None:
            return

        OtherCharacterData.character_data = defaultdict(dict)

        path = os.path.dirname(os.path.realpath(__file__))
        with open(path + "/other_character_data.csv") as csv_file:
            # A list of dicts containing the data
            csv_reader = list(csv.DictReader(csv_file))
            for frame in csv_reader:
                # Pull out the character
                character = Character(int(frame["Character"]))

                OtherCharacterData.character_data[character] = {"Weight": float(frame["Weight"]),
                                                                "Ledge Box Bottom": float(frame["Ledge Box Bottom"]),
                                                                "Ledge Box Top": float(frame["Ledge Box Top"]),
                                                                "Ledge Box Horizontal": float(frame["Ledge Box Horizontal"])}

    @staticmethod
    def get_weight(character):
        return OtherCharacterData.character_data[character]["Weight"]

    @staticmethod
    def get_ledge_box_bottom(character):
        return OtherCharacterData.character_data[character]["Ledge Box Bottom"]

    @staticmethod
    def get_ledge_box_top(character):
        return OtherCharacterData.character_data[character]["Ledge Box Top"]

    @staticmethod
    def get_ledge_box_horizontal(character):
        return OtherCharacterData.character_data[character]["Ledge Box Horizontal"]