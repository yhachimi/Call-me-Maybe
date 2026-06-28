from pydantic import BaseModel


class Prompt(BaseModel):
    prompt: str


class Functions_Defs(BaseModel):
    name: str
    description: str
    parameters: dict
    returns: dict


class Init:
    def defs_init(self, func_defs: dict) -> list[Functions_Defs]:
        defs = []

        for d in func_defs:
            defs.append(Functions_Defs(**d))

        return defs

    def prompts_init(self, prompts: dict) -> list[Prompt]:
        Prompts = []
        for p in prompts:
            Prompts.append(Prompt(**p))

        return Prompts
