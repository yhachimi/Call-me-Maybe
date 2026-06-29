RED = '\033[0;31m'
RESET = '\033[1;37m'

try:
    import argparse as arg
    import json

    import llm_sdk.llm_sdk as llm_model

    from .dataclase import Init
    from .system_promt import system_promt_builde
except Exception as e:
    print(f"⚠️ {RED}{e}{RESET}")


def json_reader(file: str) -> dict:
    with open(file, "r") as f:
        return json.load(f)


def get_valid_vocab(vocab: dict[str, int]) -> list[int]:
    valid = set(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "0123456789`_.,\":-+/\\!?'()[]{}<>ĠĊ ")
    valid_ids = [id for st, id in vocab.items() if all(c in valid for c in st)]
    return valid_ids


def get_valid_output(output_json: str) -> str:
    start = output_json.index("{")
    brackets = 0 
    for c in output_json:
        if c == "{":
                  brackets += 1
        if c == "}":
                    brackets -= 1

def get_next_id(logits: list[float], valid_ids: list[int]) -> int:
              return max(valid_ids, key=lambda i: logits[i] if i < len(logits) else float("-inf"))

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
        Model = llm_model.Small_LLM_Model(args.model)
        vocab = json_reader(Model.get_path_to_vocab_file())
        valid_ids = get_valid_vocab(vocab)
        name = "{'name'"
        print(len(valid_ids))
        for p in prompts:
            st = f"\nUSER: {p.prompt}"
            gen_prompt = Model.encode(sys_prompt + st)
            gen_ids = gen_prompt[0].tolist()
            all_gen = []
            all_gen.extend(Model.encode(name)[0].tolist())
            for i in range(50):
                logits = Model.get_logits_from_input_ids(gen_ids + all_gen)
                next_id = get_next_id(logits, valid_ids)
                all_gen.append(next_id)
                json_output = Model.decode(all_gen)
                print(text)
    except Exception as e:
        print(f"⚠️ {RED}{e}{RESET}")
