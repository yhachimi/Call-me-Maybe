from typing import Any

from pydantic import BaseModel, ValidationError
from src.parsing.parsingError import ParsingError


class Prompt(BaseModel):
    prompt: str


class FDef(BaseModel):
    name: str
    description: str
    parameters: dict[str, dict]
    returns: dict[str, str]


class INIT:
    def prompt_init(self, prompts: list[dict[str, str]]) -> list[Prompt]:
        Prompts: list[Prompt] = []
        try:
            for prompt in prompts:
                Prompts.append(Prompt(**prompt))
        except ValidationError as e:
            raise ParsingError(e)
        return Prompts

    def init_functions_def(self, Fdefs: list[dict[str, Any]]) -> list[FDef]:
        defs: list[FDef] = []

        try:
            for f_def in Fdefs:
                defs.append(FDef(**f_def))
        except ValidationError as e:
            raise ParsingError(e)
        return defs
