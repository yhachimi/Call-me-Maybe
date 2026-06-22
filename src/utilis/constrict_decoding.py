from typing import Any

RED = '\033[0;31m'
RESET = '\033[1;37m'
BLUE = '\033[0;34m'
GREEN = '\033[0;32m'
try:
    from llm_sdk.llm_sdk import Small_LLM_Model
except Exception as e:
    print(f"🚨 {RED}{e}{RESET}")
    exit(0)


def get_next_token(logits: list[float], valid_ids: set[int]) -> float:
    return max(valid_ids, key=lambda i: logits[i] if i < len(
        logits) else float("-inf"))


def name_decoder(**kargs: Any) -> Any:
    Model: Small_LLM_Model = kargs["model"]
    name = kargs["name"]
    gen_ids = kargs["gen_ids"]
    all_gen = kargs["all_gen"]
    valid_ids = kargs["valid_ids"]
    next_ids = []
    all_gen.extend(Model.encode(name)[0].tolist())
    for i in range(50):
        logits = Model.get_logits_from_input_ids(gen_ids + all_gen)
        next_id = get_next_token(logits, valid_ids)
        next_ids.append(next_id)
        text = Model.decode(all_gen)
        all_gen.append(next_id)
        if "}}" in text:
            break
    clean_json = Model.decode(all_gen)
    return clean_json
