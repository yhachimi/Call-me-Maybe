import json
from typing import Any

from ..parsing import ParsingError
from .dataclass import FDef

RED = '\033[0;31m'
RESET = '\033[1;37m'
BLUE = '\033[0;34m'
GREEN = '\033[0;32m'
try:
    from llm_sdk.llm_sdk import Small_LLM_Model
except Exception as e:
    print(f"🚨 {RED}{e}{RESET}")
    exit(0)


def build_valid_json_tokens(vocab: Any) -> set[int]:
    safe_data = set(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "0123456789`_.,\":-+/\\!?'()[]{}<>ĠĊ ")
    valid = set()
    for tok_str, tok_id in vocab.items():
        if tok_str and all(c in safe_data for c in tok_str):
            valid.add(tok_id)
    return valid


def loead_vocab_data(model: Small_LLM_Model) -> Any:
    vocab_path = model.get_path_to_tokenizer_file()
    with open(vocab_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    vocab = data.get("model", {}).get("vocab", {})
    return vocab


def build_system_prompts(defenetions: list[FDef]) -> str:
    lines = []
    try:
        with open("src/line", "r") as file:
            lines = file.read().splitlines()
    except (FileNotFoundError, PermissionError) as e:
        raise ParsingError(e)

    for d in defenetions:
        typ = "type"
        parms = ", ".join(
                f"{parm}: {d.parameters[parm][typ]}"
                for parm in d.parameters)
        lines.append(f"  -{d.name}({parms}): {d.description}")

    msg = '{"name": "<fn>", "parameters": {<parameters>}}'
    output = f'\nOutput ONLY valid JSON: {msg}'
    ln = 'Use ONLY parameter names defined in the selected function"'
    lines.append(output)
    lines.append(ln)
    return "\n".join(lines)
