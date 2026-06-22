llm = https://cdn.intra.42.fr/document/document/48315/llm_sdk.zip
data = https://cdn.intra.42.fr/document/document/48314/data.zip
flage = --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
prmpts = data/input/function_calling_tests.json
defs = data/input/functions_definition.json
output = "data/output/function_calling_results.json"

run:
	@uv run python -m src --functions_definition $(defs) --input $(prmpts) --output $(output)

install:
	@pip install pdbpp 
	@pip install  mypy
	@pip install numpy
	@pip install pydantic
	@pip install  uv
	@wget $(llm)
	@wget $(data)
	@unzip data.zip 
	@unzip llm_sdk.zip



debug:
	pdb call_me_maybe.py 

clean: 
	@rm -rf __pycache__ */*__pycache__  .mypy_cache *data* */*/__pycache__  *llm_sdk* .venv*  */.venv */*llm_sdk* llm_sdk $(output)

lint:
	@flake8 && mypy . $(flage) 
