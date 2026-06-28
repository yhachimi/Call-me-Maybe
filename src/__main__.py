RED = '\033[0;31m'
RESET = '\033[1;37m'

try:
    import argparse as arg
    import json

    from .dataclase import Init
    from .system_promt import system_promt_builde
    from llm_sdk.llm_sdk import Small_LLM_Model
except Exception as e:
    print(f"⚠️ {RED}{e}{RESET}")


def json_reader(file: str) -> dict:
    with open(file, "r") as f:
        return json.load(f)


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

        parsargs.add_argument("--model", default="Qwen/Qwen3-0.6B")

        initializer: Init = Init()
        args = parsargs.parse_args()
        prompts = initializer.prompts_init(json_reader(args.input))
        functions_definition = initializer.defs_init(
            json_reader(args.functions_definition))
        sys_prompt = system_promt_builde(functions_definition)
        Model = Small_LLM_Model(args.model)
    except Exception as e:
        print(f"⚠️ {RED}{e}{RESET}")
