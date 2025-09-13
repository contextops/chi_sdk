# Setup

## Prerequisites

- Python 3.11+
- pip

## Installation

```bash
pip install chi-sdk
```

That's it! The TUI is included.

## Quick Start

```python
from chi_sdk import chi_command, build_cli
from pydantic import BaseModel

class HelloInput(BaseModel):
    name: str

class HelloOutput(BaseModel):
    message: str

@chi_command(input_model=HelloInput, output_model=HelloOutput)
def hello(inp: HelloInput) -> HelloOutput:
    return HelloOutput(message=f"Hello, {inp.name}!")

cli = build_cli("my-app")

if __name__ == "__main__":
    cli()
```

Run your app:
```bash
# As CLI
my-app hello --name World

# As TUI - automatic!
my-app ui
```

## Development Setup

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install development dependencies
pip install -U pip
pip install -r requirements-dev.txt

# Install SDK in development mode
pip install -e python-chi-sdk

# Run tests
pytest python-chi-sdk/tests/
```

## Customization

Generate configuration templates for your TUI:

```bash
chi-admin init . --binary-name=my-app
```

This creates `.tui/` directory with customizable YAML files for menus, panels, and styling.
