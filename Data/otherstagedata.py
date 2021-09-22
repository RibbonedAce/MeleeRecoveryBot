import csv
import os
from collections import defaultdict

from melee import Stage


class OtherStageData:
    stage_data = None

    @staticmethod
    def init_data():
        if OtherStageData.stage_data is not None:
            return

        OtherStageData.stage_data = defaultdict(dict)

        path = os.path.dirname(os.path.realpath(__file__))
        with open(path + "/other_stage_data.csv") as csv_file:
            # A list of dicts containing the data
            csv_reader = list(csv.DictReader(csv_file))
            for stage in csv_reader:
                stage_name = Stage(int(stage["Stage"]))

                OtherStageData.stage_data[stage_name] = {"Top BlastZone": float(stage["Top BlastZone"]),
                                                    "Bottom BlastZone": float(stage["Bottom BlastZone"]),
                                                    "Left BlastZone": float(stage["Left BlastZone"]),
                                                    "Right BlastZone": float(stage["Right BlastZone"])}

    @staticmethod
    def get_left_blast_zone(stage):
        return OtherStageData.stage_data[stage]["Left BlastZone"]

    @staticmethod
    def get_right_blast_zone(stage):
        return OtherStageData.stage_data[stage]["Right BlastZone"]
