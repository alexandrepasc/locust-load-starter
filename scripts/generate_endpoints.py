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


def generate_parameters_dict(__path: str, __name: str, __params: dict):
    # print(__params)
    with open(f"{__path}/{__name}-parameters.py", "a") as f:
        w: str = ""

        for i in __params:
            print(f"{i}\n\n")
            print(i["name"])
            # for pk, pi in i.items():
            #     print(pi)
            if i["in"] == "query":
                match i["schema"]["type"]:
                    case "string":
                        __type: str = "str"
                    case "number":
                        __type: str = "int"
                    case "boolean":
                        __type: str = "bool"

                w = w + i["name"] + f": {__type}\n"

        f.write(w)


def build_file_content(__dic: dict, __file: str, __path: str, __ep: str,
                       __class_name: str):

    if os.path.exists(__file):
        with open(__file, "a") as f:

            cn: str = sub(r"(-)+", " ", __class_name).title().replace(" ", "")

            w: str = f"from http.cookiejar import CookieJar\n\n" \
                     f"import locust\n\n" \
                     f"ENDPOINT = \"{__ep}\"\n\n\n" \
                     f"class {cn}:\n" \
                     f"    def __init__(self, loc: locust.user.users):\n" \
                     f"        self.loc = loc\n"
            f.write(w)

            for mk, mi in __dic.items():
                oid: str = mk + "_" + mi["operationId"]

                if "parameters" in mi:
                    param: str = "              " \
                                 "params: dict[str, any] = None,\n"

                    param_entry: str = "            params=params,\n"

                    generate_parameters_dict(__path, oid, mi["parameters"])
                else:
                    param: str = ""

                    param_entry: str = ""

                wm: str = f"\n" \
                          f"    def {oid}(self,\n" \
                          f"{param}" \
                          f"              headers: dict[str, any] = None,\n" \
                          f"              cookies: CookieJar = None,\n" \
                          f"              redirect: bool = False):\n\n" \
                          f"        response = self.loc.client.{mk}(\n" \
                          f"            ENDPOINT,\n" \
                          f"{param_entry}" \
                          f"            headers=headers,\n" \
                          f"            cookies=cookies,\n" \
                          f"            name=\"{oid}\",\n" \
                          f"            allow_redirects=redirect\n" \
                          f"        )\n\n" \
                          f"        return response\n"
                f.write(wm)


def generate_artifacts(__content: dict, __path: str):

    for x, y in __content["paths"].items():
        create_folder(__path, x)

        __file_path = __path + x
        __file_name = x.split("/")[len(x.split("/")) - 2] + ".py"

        create_file(__file_path, __file_name)

        build_file_content(y, __file_path + "/" + __file_name,
                           __file_path, x,
                           x.split("/")[len(x.split("/")) - 2])


if __name__ == "__main__":
    __path: str = manage_endpoint_path()

    __file: str = manage_arguments()

    __content: dict = get_yaml_content(__file)

    generate_artifacts(__content, __path)
