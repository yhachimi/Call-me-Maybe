RED = '\033[0;31m'
RESET = '\033[1;37m'
BLUE = "\033[34m"
GREEN = "\033[92m"
try:
    import argparse as arg
    import json
    from pathlib import Path
    from time import perf_counter, sleep
    from typing import Any

    import llm_sdk.llm_sdk as llm_model

    from .dataclase import Init
    from .system_promt import system_promt_builde
except (Exception) as e:
    print(f"⚠️ {RED}{e}{RESET}")
except KeyboardInterrupt:
    exit(0)


def animated_output(text: str, Color):
    for c in text:
        print(f"{Color}{c}{RESET}", end="", flush=True)
        sleep(0.02)
    print()


def json_reader(file: str) -> dict:
    with open(file, "r") as f:
        return json.load(f)


def creat_folder(path: str):
    p = Path(path)
    dir = p.parent
    dir.mkdir(parents=True, exist_ok=True)


def get_valid_vocab(vocab: dict[str, int]) -> list[int]:
    valid = set(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "0123456789`_.,\":-+/\\!?'()[]{}<>ĠĊ ")
    valid_ids = [id for st, id in vocab.items() if all(c in valid for c in st)]
    return valid_ids


def get_valid_output(output_json: str) -> Any:
    start = output_json.find("{")
    brackets = 0
    for i in range(len(output_json)):
        if output_json[i] == "{":
            brackets += 1
        if output_json[i] == "}":
            brackets -= 1
        if brackets == 0:
            return output_json[start:i + 1]
    return None


def get_next_id(logits: list[float], valid_ids: list[int]) -> int:
    return max(valid_ids, key=lambda i: logits[i] if i < len(
        logits) else float("-inf"))


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
        path_out = args.output
        sys_prompt = system_promt_builde(functions_definition)
        Model = llm_model.Small_LLM_Model(args.model)
        vocab = json_reader(Model.get_path_to_vocab_file())
        valid_ids = get_valid_vocab(vocab)
        name = '{"name":'
        outputs: list[dict] = []
        start = perf_counter()
        for p in prompts:
            st = f"\nUSER: {p.prompt}"
            animated_output(st, BLUE)
            gen_prompt = Model.encode(sys_prompt + st)
            gen_ids = gen_prompt[0].tolist()
            all_gen = []
            all_gen.extend(Model.encode(name)[0].tolist())
            for i in range(100):
                logits = Model.get_logits_from_input_ids(gen_ids + all_gen)
                next_id = get_next_id(logits, valid_ids)
                all_gen.append(next_id)
                json_output = get_valid_output(Model.decode(all_gen))
                if json_output:
                    break
            if json_output:
                out = json.loads(json_output)
            outputs.append(out)
            animated_output(f"Qwen3-0.6B: {json_output}", GREEN)
        end_time = perf_counter()
        total = (end_time - start) / 60
        creat_folder(args.output)
        with open(args.output, "w") as file:
            json.dump(outputs, file, indent=2)
        print(f"Output Created in {args.output}")
        print(f"Done in {total:.2f} minutes")
    except Exception as e:
        print(f"⚠️ {RED}{e}{RESET}")
    except KeyboardInterrupt:
        exit(0)
