import os
from argparse import ArgumentParser, Namespace
from datetime import datetime

script_path: str = os.path.dirname(os.path.realpath(__file__))

reports_path: str = f"{script_path}/reports"

date: str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

if not os.path.exists(reports_path):
    os.mkdir(reports_path)

arg_parser: ArgumentParser = ArgumentParser(
        prog="run_tests.py",
        description="Run this script to execute the test and generate the "
                    "report with a the timestamp and the execution "
                    "configuration.\nCan use this to run tests unattended "
                    "a still have the necessary information to generate "
                    "the result report.")

arg_parser.add_argument("-u", "--users", required=True,
                        help="Peak number of concurrent locust users")
arg_parser.add_argument("-r", "--spawn-rate", required=True,
                        help="Rate of spawn users per second")
arg_parser.add_argument("-t", "--time", required=True,
                        help="The time that the test will run "
                             "(300s, 5m, 1h, 1h30m)")
arg_parser.add_argument("-f", "--file", required=True,
                        help="Full path for the locust test file")
arg_parser.add_argument("-H", "--host", required=True,
                        help="Host to load test")

args: Namespace = arg_parser.parse_args()

test_name: str = args.file

if test_name.find("/") != -1:
    test_name = test_name[test_name.rfind("/"):]
    test_name = test_name.split("/")[1]

test_name = test_name.split(".py")[0]

report_name: str = f"report_{test_name}_u{args.users}" \
                   f"_r{args.spawn_rate}_t{args.time}_{date}"

locust_command: str = f"locust -u {args.users} -r {args.spawn_rate} " \
                      f"-t {args.time} -H {args.host} -f {args.file} " \
                      f"--headless " \
                      f"--html {reports_path}/{report_name}.html " \
                      f"--csv {reports_path}/{report_name} " \
                      f"--csv-full-history"

print(locust_command)

os.system(locust_command)
