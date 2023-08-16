import json
import os
from argparse import ArgumentParser, Namespace


#  Generate the tasks path in case is doesn't exist
def manage_tasks_path():
    script_path: str = os.path.dirname(os.path.realpath(__file__))

    tasks_path: str = script_path + "/../tasks"

    if not os.path.exists(tasks_path):
        os.mkdir(tasks_path)

    return tasks_path


#  Manage the command line arguments that the script supports.
def manage_arguments():
    arg_parser = ArgumentParser(
        prog="generate_flow.py",
        description="Use this application to map the har sequence of calls "
                    "to a locust task.")

    arg_parser.add_argument("-f", "--file", required=True,
                            help="Full path for the har file path")
    args: Namespace = arg_parser.parse_args()

    return args.file


#  Open, read, and unserialize the har file.
def get_har_content(__file: str):
    with open(__file, "r") as f:
        try:
            __har: dict = json.loads(f.read())
        except json.JSONDecoder as e:
            print(e)

    return __har


def generate_artifacts(__content: dict, __path: str):
    for ci in __content["log"]["entries"]:
        print(ci["request"])


if __name__ == "__main__":
    __path: str = manage_tasks_path()

    __file: str = manage_arguments()

    __content: dict = get_har_content(__file)

    generate_artifacts(__content, __path)
