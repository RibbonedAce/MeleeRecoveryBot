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

                OtherCharacterData.character_data[character] = {"Weight": float(frame["Weight"])}

    @staticmethod
    def get_weight(character):
        return OtherCharacterData.character_data[character]["Weight"]
