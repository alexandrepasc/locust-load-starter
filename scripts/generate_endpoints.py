import json
import os
import sys
from re import sub
from argparse import ArgumentParser, Namespace
from typing import TextIO

import yaml

REQUESTS_ENDPOINT: str = "#  The constant with the endpoint path used in " \
                         "the class"

REQUESTS_CLASS_DOC: str = "#  This class contains a list of the functions " \
                          "for this endpoint with all the\n#  requests " \
                          "that were exported from the swagger yaml " \
                          "file. To use this you\n#  need to instantiate " \
                          "the class and pass the locust into it and " \
                          "after that we\n#  are able to start to build " \
                          "the tests."

REQUESTS_INIT_DOC: str = "#  Initialize the class with the locust instance."

REQUESTS_ID_DOC: str = "#  This request needs an id to be included in the " \
                       "endpoint path, be aware\n    #  that before " \
                       "passing take in consideration if the endpoint " \
                       "value set in\n    #  the ENDPOINT constant has or " \
                       "not the '/' at the end. In case it hasn't,\n    " \
                       "#  add the slash before the id (ex. " \
                       "id=\"/qwer-1234-asdasdasd-123\")."

PARAMETERS_DOC: str = "#  List of all the parameters exposed in the swagger" \
                      " file, with a comment\n#  referring the type, this " \
                      "can be used when creating the test requests. The\n" \
                      "#  name of this file is linked with a request " \
                      "function in the class in\n#  this folder."


#  Generate the base path in the project to store the endpoints artifacts.
def manage_endpoint_path():
    script_path: str = os.path.dirname(os.path.realpath(__file__))

    endpoints_path: str = script_path + "/../endpoints"

    if not os.path.exists(endpoints_path):
        os.mkdir(endpoints_path)

    return endpoints_path


#  Manage the command line arguments that the script supports.
def manage_arguments():
    arg_parser = ArgumentParser(
        prog="generate_endpoints.py",
        description="Use this application to map the swagger endpoints to "
                    "the load testing.")

    arg_parser.add_argument("-f", "--file", required=True,
                            help="Full path for the swagger file")
    args: Namespace = arg_parser.parse_args()

    return args.file


#  Open, read, and deserialize the yaml file.
def get_yaml_content(__file: str):
    with open(__file, "r") as stream:
        try:
            __yml: dict = yaml.safe_load(stream)
        except yaml.YAMLError as e:
            print(e)

    return __yml


#  Open, read and deserialize the json file
def get_json_content(file: str):
    with open(file, "r") as stream:
        try:
            __json: dict = json.load(stream)
        except json.JSONDecodeError as e:
            print(e)

    return __json


#  Filter the file format execute the correct function and return the dictionary
def get_content(file: str):
    if file.find(".yml") or file.find(".yaml"):
        return get_yaml_content(file)
    elif file.find(".json"):
        return get_json_content(file)
    else:
        print("File format not recognised. Supported formats \".yml\", \".yaml\" and \".json\".")
        sys.exit(1)


#  Create the folder to store the endpoint artifacts.
def create_folder(__path: str, __folder: str):
    if not os.path.exists(__path + "/" + __folder):
        os.makedirs(__path + __folder)


#  Create the class and init artifacts for the endpoint.
def create_file(__path: str, __name: str):
    if not os.path.exists(__path + "/" + __name):
        f: TextIO = open(__path + "/" + __name, "x")
        f.close()

        try:
            f = open(__path + "/__init__.py", "x")
            f.close()
        except FileExistsError:
            return


#  Generate the parameters file with all the content.
def generate_parameters_list(__path: str, __name: str, __params: dict):
    with open(f"{__path}/{__name}_parameters.py", "a") as f:
        w: str = f"{PARAMETERS_DOC}\n"

        for i in __params:
            if i["in"] == "query":
                w = w + i["name"] + " = \"" + i["name"] + "\"  # " \
                    + i["schema"]["type"] + "\n"

        f.write(w)


#  Add the content to the class file.
def build_file_content(__dic: dict, __file: str, __path: str, __ep: str,
                       __class_name: str):
    if os.path.exists(__file):
        with open(__file, "a") as f:

            cn: str = sub(r"(-)+", " ", __class_name).title().replace(" ", "")
            cn = sub(r"(_)+", " ", cn).title().replace(" ", "")

            w: str = f"from http.cookiejar import CookieJar\n\n" \
                     f"import locust\n\n" \
                     f"{REQUESTS_ENDPOINT}\n" \
                     f"ENDPOINT: str = \"{__ep}\"\n\n\n" \
                     f"{REQUESTS_CLASS_DOC}\n" \
                     f"class {cn}:\n" \
                     f"    {REQUESTS_INIT_DOC}\n" \
                     f"    def __init__(self, loc: locust.user.users):\n" \
                     f"        self.loc = loc\n"
            f.write(w)

            for mk, mi in __dic.items():
                try:
                    aux: str = mi["operationId"]
                except TypeError:
                    continue

                aux = snake_case(aux)

                oid: str = mk + "_" + aux

                if "parameters" in mi:
                    param: str = "              " \
                                 "params: dict[str, any] = None,\n"

                    param_entry: str = "            params=params,\n"

                    generate_parameters_list(__path, oid, mi["parameters"])
                else:
                    param: str = ""

                    param_entry: str = ""

                wm: str = f"\n" \
                          f"    def {oid}(self,\n" \
                          f"{param}" \
                          f"              headers: dict[str, any] = None,\n" \
                          f"              cookies: CookieJar = None,\n" \
                          f"              auth: tuple[str, str] = None,\n" \
                          f"              json: any = None,\n" \
                          f"              data: dict[str, any] = None,\n" \
                          f"              files: dict[str, any] = None,\n" \
                          f"              redirect: bool = False,\n" \
                          f"              verify: bool = True):\n\n" \
                          f"        response = self.loc.client.{mk}(\n" \
                          f"            ENDPOINT,\n" \
                          f"{param_entry}" \
                          f"            headers=headers,\n" \
                          f"            cookies=cookies,\n" \
                          f"            auth=auth,\n" \
                          f"            json=json,\n" \
                          f"            data=data,\n" \
                          f"            files=files,\n" \
                          f"            name=\"{oid}\",\n" \
                          f"            allow_redirects=redirect,\n" \
                          f"            verify=verify\n" \
                          f"        )\n\n" \
                          f"        return response\n"
                f.write(wm)


#  Generate the methods to handle the support for endpoint path parameter
def append_path_parameter_content(__file_path: str, __file_name: str,
                                  __dict: dict):
    if os.path.exists(__file_path + "/" + __file_name):
        with open(__file_path + "/" + __file_name, "a") as f:
            for mk, mi in __dict.items():
                try:
                    aux: str = mi["operationId"]
                except TypeError:
                    continue

                aux = snake_case(aux)

                oid: str = mk + "_" + aux + "_id"

                if "parameters" in mi:
                    param: str = "              " \
                                 "params: dict[str, any] = None,\n"

                    param_entry: str = "            params=params,\n"

                    generate_parameters_list(__file_path, oid,
                                             mi["parameters"])
                else:
                    param: str = ""

                    param_entry: str = ""

                wm: str = f"\n" \
                          f"    {REQUESTS_ID_DOC}\n" \
                          f"    def {oid}(self,\n" \
                          f"              id: str,\n" \
                          f"{param}" \
                          f"              headers: dict[str, any] = None,\n" \
                          f"              cookies: CookieJar = None,\n" \
                          f"              auth: tuple[str, str] = None,\n" \
                          f"              json: any = None,\n" \
                          f"              data: dict[str, any] = None,\n" \
                          f"              files: dict[str, any] = None,\n" \
                          f"              redirect: bool = False,\n" \
                          f"              verify: bool = True):\n\n" \
                          f"        response = self.loc.client.{mk}(\n" \
                          f"            ENDPOINT + id,\n" \
                          f"{param_entry}" \
                          f"            headers=headers,\n" \
                          f"            cookies=cookies,\n" \
                          f"            auth=auth,\n" \
                          f"            json=json,\n" \
                          f"            data=data,\n" \
                          f"            files=files,\n" \
                          f"            name=\"{oid}\",\n" \
                          f"            allow_redirects=redirect,\n" \
                          f"            verify=verify\n" \
                          f"        )\n\n" \
                          f"        return response\n"
                f.write(wm)


#  Manage the creation of the artifacts and write their content.
def generate_artifacts(__content: dict, __path: str):
    for x, y in __content["paths"].items():
        xs: str = sub(r"(-)+", " ", x).replace(" ", "_")

        if x[len(x) - 1] == "/":
            __file_name: str = xs.split("/")[len(x.split("/")) - 2] + ".py"
            __class_name: str = x.split("/")[len(x.split("/")) - 2]
        else:
            __file_name: str = xs.split("/")[len(x.split("/")) - 1] + ".py"
            __class_name: str = x.split("/")[len(x.split("/")) - 1]

        if not str.__contains__(__file_name, "{"):
            create_folder(__path, xs)

            __file_path: str = __path + xs

            create_file(__file_path, __file_name)

            build_file_content(y, __file_path + "/" + __file_name,
                               __file_path, xs, __class_name)
        else:
            if xs[len(xs) - 1] == "/":
                xs = xs[:len(xs) - 1]
                xs = xs[:xs.rfind("/")]
            else:
                xs = xs[:xs.rfind("/")]

            __file_name: str = xs.split("/")[len(xs.split("/")) - 1] + ".py"
            append_path_parameter_content(__path + xs, __file_name, y)


#  Convert string into snake case
def snake_case(s):
    # Replace hyphens with spaces, then apply regular expression substitutions for title case conversion
    # and add an underscore between words, finally convert the result to lowercase
    return '_'.join(
        sub('([A-Z][a-z]+)', r' \1',
            sub('([A-Z]+)', r' \1',
                s.replace('-', ' '))).split()).lower()


#  Main function that will be executed.
if __name__ == "__main__":
    __path: str = manage_endpoint_path()

    __file: str = manage_arguments()

    __content: dict = get_content(__file)

    generate_artifacts(__content, __path)
