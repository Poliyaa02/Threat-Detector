import argparse

class CommandInterface:
    @staticmethod
    def parse_arguments():
        parser = argparse.ArgumentParser(
            description="Explanation of Flags"
        )

        parser.add_argument(
            "--verbose", "-v", action="store_true",
            help="Enable verbose mode"
        )

        parser.add_argument(
            "--path", "-p", dest="file_path",
            help="Specify a file path"
        )

        return parser.parse_args()
