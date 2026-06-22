import json
import time as te
from argparse import ArgumentParser
from pathlib import Path
from typing import Any

from .parsing import Parser, ParsingError
from .utilis import (INIT, FDef, Prompt, build_system_prompts,
                     build_valid_json_tokens, loead_vocab_data, name_decoder)

RED = '\033[0;31m'
RESET = '\033[1;37m'
BLUE = '\033[0;34m'
GREEN = '\033[0;32m'


def check_present_file(file: str) -> None:
    try:
        with open(file, "r"):
            pass

    except FileNotFoundError as e:
        raise ParsingError(e)


def exctarct_clean_json(clean_json: str) -> str:
    start = clean_json.find("{")

    i = 0
    braces_counter = 0
    while i < len(clean_json):
        if clean_json[i] == "{":
            braces_counter += 1
        if clean_json[i] == "}":
            braces_counter -= 1
        if braces_counter == 0:
            break
        i += 1

    return clean_json[start: i + 1]


def creat_dir(ouput_path: str) -> None:
    p = Path(ouput_path)
    directory = p.parent
    directory.mkdir(parents=True, exist_ok=True)


def loed_json_data(file: str) -> list[dict[str, Any]]:
    data: list[dict[str, Any]] = []
    try:
        with open(file, "r") as f:
            data = json.load(f)
            if not data:
                raise ParsingError("json  file cannot be empty")
    except (UnicodeDecodeError, json.JSONDecodeError) as e:
        raise ParsingError(e)
    return data


def show_logo(logo: str) -> None:
    check_present_file(logo)
    try:
        with open(logo) as f:
            Logo = f.read().splitlines()
            for line in Logo:
                print(f"{BLUE}{line}{RESET}")
                te.sleep(0.2)

    except Exception as e:
        raise ParsingError(e)


def get_next_token(logits: list[float], valid_ids: set[int]) -> float:
    return max(valid_ids, key=lambda i: logits[i] if i < len(
        logits) else float("-inf"))


if __name__ == "__main__":
    try:
        try:
            from llm_sdk.llm_sdk import Small_LLM_Model
        except ModuleNotFoundError as e:
            raise ParsingError(e)
        show_logo("src/pic/logo")
        print("🚀 Loead System ...")
        prompts_path: str = "data/input/function_calling_tests.json"
        functions_def: str = "data/input/functions_definition.json"
        output: str = "data/output/function_calling_results.json"
        argparser = ArgumentParser(
            description="Translate  naturale prompts into functions calls..")
        argparser.add_argument(
            "--functions_definition",
            type=str,
            default=functions_def)
        argparser.add_argument("--input", type=str, default=prompts_path)
        argparser.add_argument("--output", type=str, default=output)
        argparser.add_argument("--model", type=str, default="Qwen/Qwen3-0.6B")
        args = argparser.parse_args()
        prompts_path = args.input
        model = args.model
        functions_def = args.functions_definition
        output = args.output
        print("📁 loading definitions and prompts ...")
        check_present_file(prompts_path)
        check_present_file(functions_def)
        prompts: list[dict[str, Any]] = loed_json_data(prompts_path)
        definitions: list[dict[str, Any]] = loed_json_data(functions_def)
        parser = Parser(prompts, definitions)
        parser.prompts_parser()
        initialaizer = INIT()
        print("⚙️ initialaize the prompts class ...")
        Prompts: list[Prompt] = initialaizer.prompt_init(prompts)
        print("⚙️ initialaize  the definitions class ...")
        Definitions: list[FDef] = initialaizer.init_functions_def(definitions)
        print("🔧 building the model prompts ...")
        sytem_prompts: str = build_system_prompts(Definitions)
        print("Ⓜ️ loading model...")
        try:
            Model = Small_LLM_Model(model_name=model)
        except OSError as e:
            raise ParsingError(e)
        print("🗒 loading tokens vocabalery ...")
        try:
            vocab = loead_vocab_data(Model)
        except Exception as e:
            raise ParsingError(e)
        valid_ids = build_valid_json_tokens(vocab)
        llm_results: list[Any] = []
        print("💾 start prossecing prompts ...")
        steps: dict[str, Any] = {}
        steps["name"] = "{\"name\": \""
        parsers: list[Any] = []
        start_time = te.perf_counter()
        for pr in Prompts:
            print(f"⏳ Analysing and processing prompt: {pr.prompt}")
            user = f"Prompt: {pr.prompt}\nAssistant:"
            full_prompt = f"{sytem_prompts}\n{user}"
            ids_inputs = Model.encode(full_prompt)
            gen_ids = ids_inputs[0].tolist()
            all_gen: list = []
            clean_json: Any = name_decoder(
                name=steps["name"],
                all_gen=all_gen,
                valid_ids=valid_ids,
                gen_ids=gen_ids,
                model=Model)
            clean_json = exctarct_clean_json(clean_json)

            parsed = json.loads(clean_json)
            parsed["prompt"] = pr.prompt
            if not clean_json:
                parsed = {
                    "prompt": pr.prompt,
                    "name": "none",
                    "parameters": "none"}
            if parsed.get("name", "none") != "none":
                print(f"✅ {parsed['name']}({parsed['parameters']})")
            else:
                print("❌ Could Not genrate functions calls")
            parsers.append({
                "prompt": pr.prompt,
                "name": parsed.get("name"),
                "parameters": parsed.get("parameters")})
        end_time = te.perf_counter()
        print("📃 genrate the output file ...")
        creat_dir(output)
        total_in_second = end_time - start_time
        total_in_minutes = total_in_second / 60
        result = f"{total_in_minutes:.2f} minutes"
        with open(output, "w") as f:
            json.dump(parsers, f, indent=2)
        print(f"✅ output genrated successfully in {result}")

    except (ParsingError, KeyboardInterrupt) as e:
        print(f"🚨 {RED}{e}{RESET}")
