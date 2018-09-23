import argparse
from src.statistics_creator import StatisticsCreator

class ArgumentReader:
    def __init__(self):
        self.controller = None
        self.args = self.register_arguments()

    def set_controller(self, controller):
        self.controller = controller

    # Created by Jake
    def register_arguments(self):
        # Create your commands in here
        parser = argparse.ArgumentParser()
        # Created by Braeden
        parser.add_argument(
            "-f",
            "--file",
            nargs="+",
            help="Multiple file input for parse")
        # Created By Jake Reddock
        parser.add_argument(
            "-s",
            "--statistics",
            action='store_true',
            help="Print Statistics for classes uploaded")
        # Created By Michael Huang
        parser.add_argument(
            "-o",
            "--output",
            help="Setting name of the output location")
        return parser.parse_args()

    # Created By Jake Reddock
    def parse_arguments(self):
        if self.args.statistics:
            self.controller.statistics = StatisticsCreator("statistics")
            self.controller.statistics.create_tables()
            print("Statistics collecting is turned on")

        if self.args.file is not None:
            self.controller.files = self.args.file
            print("Files selected: ")
            print(*self.controller.files, sep="\n")

        if self.args.output is not None:
            self.controller.output = self.args.output
            print("Now setting names of output files")
