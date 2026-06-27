run: install
	@uv run python3 -m src


linit: 
	@mypy src/.
	@flake8 src/. 

install: 
	@pip install uv
	@uv sync

clean:
	@rm -rf llm_sdk data */*__pycache__ */*/ __pycache__ 
