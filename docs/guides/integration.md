# Integration Guide

This guide shows how to add CHI SDK to your existing Python CLI project.

## Installation

Add CHI SDK to your project:

```bash
pip install chi-sdk
```

Or add to your `pyproject.toml`:

```toml
[project]
dependencies = [
    "chi-sdk>=0.0.5",
    "pydantic>=2.0",
    "click>=8.0",
]
```

## Step 1: Convert Your Commands

Transform your existing Click commands to use CHI SDK decorators:

### Before (Plain Click)

```python
import click

@click.command()
@click.option('--name', required=True, help='User name')
@click.option('--shout', is_flag=True, help='Uppercase the greeting')
def hello(name, shout):
    """Say hello to someone."""
    greeting = f"Hello, {name}!"
    if shout:
        greeting = greeting.upper()
    click.echo(greeting)
```

### After (CHI SDK)

```python
from chi_sdk import chi_command, build_cli
from pydantic import BaseModel, Field

class HelloInput(BaseModel):
    name: str = Field(..., description="User name")
    shout: bool = Field(False, description="Uppercase the greeting")

class HelloOutput(BaseModel):
    greeting: str

@chi_command(
    input_model=HelloInput,
    output_model=HelloOutput,
    description="Say hello to someone"
)
def hello(inp: HelloInput) -> HelloOutput:
    greeting = f"Hello, {inp.name}!"
    if inp.shout:
        greeting = greeting.upper()
    return HelloOutput(greeting=greeting)

# Build the CLI with all registered commands
cli = build_cli("my-app")

if __name__ == "__main__":
    cli()
```

## Step 2: Test Your Integration

Your CLI works exactly as before, plus new features:

```bash
# Traditional CLI usage
my-app hello --name Alice

# JSON output for automation
my-app --json hello --name Alice

# Automatic TUI!
my-app ui
```

## Step 3: Customize the TUI (Optional)

Generate configuration templates:

```bash
chi-admin init . --binary-name=my-app
```

This creates:
- `.tui/chi-index.yaml` - Entry screen and menu structure
- `.tui/panels/` - Panel layouts  
- `.tui/styles.yaml` - Visual theming

Edit these YAML files to customize your TUI's appearance and behavior.

## Migrating Multiple Commands

For CLIs with many commands, use a systematic approach:

```python
from chi_sdk import chi_command, build_cli
from pydantic import BaseModel, Field
from typing import List

# Define models for each command
class ImportInput(BaseModel):
    file_path: str = Field(..., description="Path to import file")
    format: str = Field("csv", description="File format")

class ImportOutput(BaseModel):
    records_imported: int
    status: str

@chi_command(input_model=ImportInput, output_model=ImportOutput)
def import_data(inp: ImportInput) -> ImportOutput:
    # Your existing import logic
    records = do_import(inp.file_path, inp.format)
    return ImportOutput(records_imported=len(records), status="success")

class ExportInput(BaseModel):
    output_path: str = Field(..., description="Where to save")
    include_headers: bool = Field(True, description="Include headers")

class ExportOutput(BaseModel):
    records_exported: int
    file_size: int

@chi_command(input_model=ExportInput, output_model=ExportOutput)
def export_data(inp: ExportInput) -> ExportOutput:
    # Your existing export logic
    count, size = do_export(inp.output_path, inp.include_headers)
    return ExportOutput(records_exported=count, file_size=size)

# Build CLI with all commands
cli = build_cli("data-tool")
```

## Best Practices

### 1. Use Descriptive Field Descriptions

These become help text in both CLI and TUI:

```python
class ConfigInput(BaseModel):
    host: str = Field(..., description="Database host address")
    port: int = Field(5432, description="Database port", ge=1, le=65535)
    timeout: float = Field(30.0, description="Connection timeout in seconds")
```

### 2. Handle Progress for Long Operations

```python
from chi_sdk import emit_progress

@chi_command(output_model=ProcessOutput)
def process_large_dataset() -> ProcessOutput:
    items = load_items()
    for i, item in enumerate(items):
        emit_progress(
            message=f"Processing {item.id}",
            percent=(i / len(items)) * 100,
            stage="processing"
        )
        process_item(item)
    return ProcessOutput(processed=len(items))
```

### 3. Validate Input with Pydantic

```python
from pydantic import validator

class UserInput(BaseModel):
    email: str = Field(..., description="User email")
    age: int = Field(..., description="User age", ge=0, le=150)
    
    @validator('email')
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('Invalid email address')
        return v
```

## Troubleshooting

### Check Your Setup

```bash
chi-admin doctor
```

### Common Issues

**Issue**: "chi-tui not found"
**Solution**: Install CHI SDK: `pip install chi-sdk`

**Issue**: TUI doesn't show my commands
**Solution**: Make sure you're using `@chi_command` decorator and `build_cli()`

**Issue**: Custom YAML not loading
**Solution**: Ensure `CHI_TUI_CONFIG_DIR` points to your `.tui` directory and that `chi-index.yaml` exists inside it. All relative paths in YAML resolve against `CHI_TUI_CONFIG_DIR`.

## Next Steps

- Read the [Basic Usage](../basic_usage.md) guide
- Explore [Advanced Usage](../advanced_usage.md) for customization
- Check out [example-apps/](../../example-apps/) for complete examples
