import os
from re import sub
from argparse import ArgumentParser, Namespace
from typing import TextIO

import yaml


def manage_endpoint_path():
    script_path: str = os.path.dirname(os.path.realpath(__file__))

    endpoints_path: str = script_path + "/../endpoints"

    if not os.path.exists(endpoints_path):
        os.mkdir(endpoints_path)

    return endpoints_path


def manage_arguments():
    arg_parser = ArgumentParser(
        prog="generate_endpoints.py",
        description="Use this application to map the swagger endpoints to "
                    "the load testing.")

    arg_parser.add_argument("-f", "--file",
                            help="Full path for the swagger file path")
    args: Namespace = arg_parser.parse_args()

    return args.file


def get_yaml_content(__file: str):
    with open(__file, "r") as stream:
        try:
            __yml: dict = yaml.safe_load(stream)
        except yaml.YAMLError as e:
            print(e)

    return __yml


def create_folder(__path: str, __folder: str):

    if not os.path.exists(__path + "/" + __folder):
        os.makedirs(__path + __folder)


def create_file(__path: str, __name: str):
    if not os.path.exists(__path + "/" + __name):
        f: TextIO = open(__path + "/" + __name, "x")
        f.close()

        f = open(__path + "/__init__.py", "x")
        f.close()


# def build_file_content(__dic: dict, __file: str, __ep: str,
#                        __class_name: str, __method: str):
#     if os.path.exists(__file):
#         with open(__file, "a") as f:
#             oid: str = __method + "_" + __dic["operationId"]
#
#             cn: str = sub(r"(-)+", " ", __class_name).title().replace(" ", "")
#
#             w: str = f"from locust import TaskSet\n\n" \
#                      f"ENDPOINT = \"{__ep}\"\n\n\n" \
#                      f"class {cn}(TaskSet):\n" \
#                      f"    def {oid}(self):\n\n" \
#                      f"        response = self.client.get(\n" \
#                      f"            ENDPOINT,\n" \
#                      f"            name=\"{oid}\"\n" \
#                      f"        )\n\n" \
#                      f"        return response" \
#                      f"\n"
#
#             f.write(w)


def build_file_content(__dic: dict, __file: str, __ep: str,
                       __class_name: str):
    if os.path.exists(__file):
        with open(__file, "a") as f:

            cn: str = sub(r"(-)+", " ", __class_name).title().replace(" ", "")

            w: str = f"from locust import TaskSet\n\n" \
                     f"ENDPOINT = \"{__ep}\"\n\n\n" \
                     f"class {cn}(TaskSet):"
            f.write(w)

            for mk, mi in __dic.items():
                oid: str = mk + "_" + mi["operationId"]
                wm: str = f"\n" \
                          f"    def {oid}(self):\n\n" \
                          f"        response = self.client.{mk}(\n" \
                          f"            ENDPOINT,\n" \
                          f"            name=\"{oid}\"\n" \
                          f"        )\n\n" \
                          f"        return response\n"
                f.write(wm)


def generate_artifacts(__content: dict, __path: str):

    for x, y in __content["paths"].items():
        create_folder(__path, x)

        __file_path = __path + x
        __file_name = x.split("/")[len(x.split("/")) - 2] + ".py"

        create_file(__file_path, __file_name)

        build_file_content(y, __file_path + "/" + __file_name, x,
                           x.split("/")[len(x.split("/")) - 2])
        # for mk, mi in y.items():
        #     print(mk)
        #     print(mi["operationId"])
        #     build_file_content(mi, __file_path + "/" + __file_name,
        #                        x, x.split("/")[len(x.split("/")) - 2], mk)


if __name__ == "__main__":
    __path: str = manage_endpoint_path()

    __file: str = manage_arguments()

    __content: dict = get_yaml_content(__file)

    generate_artifacts(__content, __path)
