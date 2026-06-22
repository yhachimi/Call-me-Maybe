*This project has been created as part of the 42 curriculum by yhachimi.*

# Call Me Maybe

## Description

Call Me Maybe is a function-calling system built on top of a small language model (Qwen3-0.6B). The goal of the project is to convert natural language requests into structured function calls while guaranteeing valid JSON output.

Instead of answering a user's question directly, the system identifies the most appropriate function and extracts the required arguments according to a predefined schema.

For example:

Input:

```text
What is the sum of 40 and 2?
```

Output:

```json
{
  "prompt": "What is the sum of 40 and 2?",
  "name": "fn_add_numbers",
  "parameters": {
    "a": 40,
    "b": 2
  }
}
```

The project focuses on constrained decoding, ensuring that generated outputs are always valid, parseable, and compliant with the expected schema.

---

# Features

* Function selection using an LLM
* Structured argument extraction
* Guaranteed JSON output
* Schema validation using Pydantic
* Graceful error handling
* Configurable input and output files
* Support for custom function definitions
* Reliable processing with Qwen3-0.6B

---

# Project Structure

```text
 data
│   └──  input
│       ├──  function_calling_tests.json
│       └──  functions_definition.json
├──  data.zip
├──  llm_sdk
│   ├──  llm_sdk
│   │   └──  __init__.py
│   ├──  pyproject.toml
│   └──  uv.lock
├──  llm_sdk.zip
├──  Makefile
├──  pyproject.toml
├──  README.md
├── 󱧼 src
│   ├──  __init__.py
│   ├──  __main__.py
│   ├──  line
│   ├──  parsing
│   │   ├──  __init__.py
│   │   ├──  parsing.py
│   │   └──  parsingError.py
│   ├──  pic
│   │   └──  logo
│   └──  utilis
│       ├──  __init__.py
│       ├──  constrict_decoding.py
│       ├──  dataclass.py
│       ├──  line
│       └──  prompts_system_build.py
└──  uv.lock
```

---

# Instructions

## Installation

Install all dependencies:

```bash
make install
```

or

```bash
uv sync
```

## Run

Run using default files:

```bash
uv run python -m src
```

Run with custom files:

```bash
uv run python -m src \
    --functions_definition data/input/function_definitions.json \
    --input data/input/function_calling_tests.json \
    --output data/output/function_calling_results.json
```

## Debug

```bash
make debug
```

## Lint

```bash
make lint
```

## Clean

```bash
make clean
```

---

# Algorithm Explanation

## Function Selection

The natural language prompt is first converted into tokens using the tokenizer provided by the SDK.

The tokenized input is passed to the Qwen3-0.6B model through:

```python
get_logits_from_input_ids()
```

The model evaluates the prompt and predicts which available function best matches the user's intent.

The final function selection is based on the model's output probabilities.

---

## Constrained Decoding

The most important aspect of this project is constrained decoding.

A language model normally generates text by selecting the most probable token at each step. This often leads to malformed JSON or outputs that do not respect the required schema.

To avoid this issue:

1. The model generates logits for all possible tokens.
2. The decoder determines which tokens are valid according to:

   * JSON syntax
   * Current generation state
   * Function schema requirements
3. Invalid tokens are removed from consideration.
4. Only valid tokens can be selected.

This guarantees:

* Valid JSON
* Required fields always present
* Correct argument types
* Schema compliance

As a result, every generated output can be parsed successfully.

---

# Design Decisions

## Why Qwen3-0.6B?

The project specification requires support for Qwen3-0.6B.

Despite its small size, it provides sufficient language understanding while demonstrating how constrained decoding can significantly improve reliability.

## Why Pydantic?

Pydantic was chosen because it provides:

* Runtime validation
* Strong typing
* Clear error messages
* Schema enforcement

This simplifies validation of generated outputs.

## Why JSON?

JSON is widely used for communication between applications and provides a structured format that is easy to validate and process.

---

# Performance Analysis

## Accuracy

The system aims to achieve:

* More than 90% function selection accuracy
* More than 90% argument extraction accuracy

## Reliability

Constrained decoding guarantees:

* 100% parseable JSON
* Schema-compliant outputs
* Consistent generation

## Speed

The project processes all prompts in a few minutes on standard hardware and remains within the limits defined by the subject.

---

# Challenges Faced

## Generating Valid JSON

Small language models frequently generate malformed JSON.

This challenge was solved using constrained decoding, which prevents invalid tokens from being generated.

## Schema Enforcement

Ensuring that arguments matched expected types required integrating schema validation during generation and output validation through Pydantic.

## Error Handling

The system must never crash unexpectedly.

Robust exception handling was implemented for:

* Missing files
* Invalid JSON files
* Invalid schemas
* Runtime failures

---

# Testing Strategy

The implementation was tested using:

## Functional Tests

* Function selection
* Argument extraction
* Output generation

## Edge Cases

* Empty prompts
* Large numbers
* Special characters
* Missing arguments
* Ambiguous requests

## Error Handling Tests

* Missing input files
* Corrupted JSON files
* Invalid schemas

## Output Validation

Every generated output was checked to ensure:

* Valid JSON syntax
* Correct schema
* Correct data types

---

# Example Usage

Input:

```json
[
  {
    "prompt": "Greet John"
  }
]
```

Function Definition:

```json
[
  {
    "name": "fn_greet",
    "description": "Generate a greeting.",
    "parameters": {
      "name": {
        "type": "string"
      }
    }
  }
]
```

Output:

```json
[
  {
    "prompt": "Greet John",
    "name": "fn_greet",
    "parameters": {
      "name": "John"
    }
  }
]
```

---

# Resources

## Documentation

* Python Documentation
* Pydantic Documentation
* JSON Specification
* Qwen Model Documentation

## Learning Resources

* Introduction to Function Calling in LLMs
* Constrained Decoding Techniques
* Structured Generation for Language Models
* Tokenization and Language Model Inference

## AI Usage

AI tools were used as learning assistants for:

* Understanding constrained decoding concepts
* Exploring implementation strategies
* Reviewing documentation
* Improving technical writing

All code, design decisions, and implementation details were reviewed, understood, and validated before inclusion in the project.

