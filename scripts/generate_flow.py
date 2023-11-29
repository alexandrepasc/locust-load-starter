import json
import os
from argparse import ArgumentParser, Namespace
from re import sub
from typing import TextIO

SCRIPT_FULL_PATH: str = os.path.dirname(os.path.realpath(__file__))
TASKS_SUB_FOLDER: str = "/../tasks"


#  Generate the tasks path in case it doesn't exist
def manage_tasks_path():
    tasks_path: str = SCRIPT_FULL_PATH + TASKS_SUB_FOLDER

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

    arg_parser.add_argument("-e", "--endpoints", required=True,
                            help="Full path of the endpoints list folder")

    args: Namespace = arg_parser.parse_args()

    if args.endpoints[-1] == "/":
        args.endpoints = args.endpoints[0:-1]

    return args.file, args.endpoints


#  Open, read, and deserialize the har file.
def get_har_content(__file: str):
    with open(__file, "r") as f:
        try:
            __har: dict = json.loads(f.read())
        except json.JSONDecoder as e:
            print(e)

    return __har


#  Create the flow file to add the tasks with the flow as name. If the file already exists add a number to the end of
#  the name, ex. flow_2. The file will be created in the tasks folder in the parent of the script folder.
def create_flow_file():
    for i in range(1, 101):
        ff: str = f"/task_{i}.py"
        if not os.path.exists(SCRIPT_FULL_PATH + TASKS_SUB_FOLDER + ff):
            f: TextIO = open(SCRIPT_FULL_PATH + TASKS_SUB_FOLDER + ff, "x")
            f.write("from locust import TaskSet, task\n\n")
            f.close()
            return ff


#  Finds the endpoint path from the endpoints folder and returns true if it exists, false if not.
def find_path(item: str, ep_path: str):
    if os.path.isdir(ep_path + "/" + item):
        return True
    return False


#  Look for the api calls urls, match them with the endpoints list, and write the imports to the flow file.
def generate_imports(__content: dict, __path: str, eps: str, flow_file: str):
    write_aux: str = ""

    for ci in __content["log"]["entries"]:
        print(ci["request"])
        ci_aux: list = ci["request"]["url"].split("?")
        ci_aux: list = ci_aux[0].split("/")

        path_aux: str = ""
        for i in ci_aux:
            if i == "":
                continue

            xs: str = sub(r"(-)+", " ", i).replace(" ", "_")

            if find_path(path_aux + "/" + xs, eps):
                path_aux = path_aux + "/" + xs

        print(path_aux)

        aux_import: list[str] = path_aux.split("/")
        aux_root: list[str] = eps.split("/")

        w: str = ""
        for ia in aux_import:
            if ia == "":
                continue
            w: str = f"{w}.{ia}"

        if w != "":
            if write_aux.find(w) == -1:
                write_aux = write_aux + f"from {aux_root[-1]}{w} import *\n"

    with open(SCRIPT_FULL_PATH + TASKS_SUB_FOLDER + flow_file, "a") as f:
        f.write(write_aux)
        f.close()


if __name__ == "__main__":
    __path: str = manage_tasks_path()

    __file, eps = manage_arguments()

    __content: dict = get_har_content(__file)

    flow_file: str = create_flow_file()

    generate_imports(__content, __path, eps, flow_file)
