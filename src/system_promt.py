from .dataclase import Functions_Defs


def system_promt_builde(functions_defs: list[Functions_Defs]) -> str:
    with open("src/prompt.txt", "r") as file:
        sys_prompt: list[str] = file.read().splitlines()

    for dfs in functions_defs:
        name = f"   -{dfs.name}"
        parms = ", ".join([f"{key}: {value}" for key,
                          value in dfs.parameters.items()])
        sys_prompt.append(f"{name}: {parms}: {dfs.description}")

    msg = '{"name": "<fn>", "parameters": {<parameters>}}'
    output = f'\nOutput ONLY valid JSON: {msg}'
    sys_prompt.append(output)
    return "\n".join(sys_prompt)
