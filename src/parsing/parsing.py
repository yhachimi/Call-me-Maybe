from typing import Any

from .parsingError import ParsingError


class Parser:
    def __init__(self, prompts: list[dict[str, Any]],
                 defenitions: list[dict[str, Any]]) -> None:
        self.prompts = prompts
        self.defenitions = defenitions

    def prompts_parser(self) -> None:
        keys = "prompt"
        for prompt in self.prompts:
            for key, value in prompt.items():
                if key != keys:
                    raise ParsingError(f"unknown key {key}")
                if not isinstance(value, str):
                    raise ParsingError("the prompt must be instance of str")
