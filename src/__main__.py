import argparse as arg
import json

from .dataclase import Init


def json_reader(file: str) -> dict:
    with open(file, "r") as f:
        return json.load(f)


RED = '\033[0;31m'
RESET = '\033[1;37m'


if __name__ == "__main__":
    try:
        parsargs = arg.ArgumentParser()
        parsargs.add_argument(
            "--output",
            default="data/output/function_calls.json")
        parsargs.add_argument(
            "--input",
            default="data/input/function_calling_tests.json")
        parsargs.add_argument("--functions_definition",
                              default="data/input/functions_definition.json")

        initializer: Init = Init()
        args = parsargs.parse_args()
        prompts = initializer.prompts_init(json_reader(args.input))
        functions_definition = initializer.defs_init(
            json_reader(args.functions_definition))
    except Exception as e:
        print(f"⚠️ {RED}{e}{RESET}")
