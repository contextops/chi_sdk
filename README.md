# CHI SDK

Build beautiful Terminal User Interfaces for your Python CLI applications without rewriting your code.

## Installation

```bash
pip install chi-sdk
```

## Features

- 🎯 **Decorator-based** - Add TUI capabilities with simple decorators
- 🔒 **Type-safe** - Pydantic models for input/output validation
- 🚀 **Fast** - High-performance TUI included (no additional downloads)
- 📦 **Batteries included** - Works out of the box
- 🔄 **Dual-mode** - Same code works as CLI and TUI

## Quick Example

```python
from chi_sdk import chi_command, build_cli, emit_ok
from pydantic import BaseModel, Field
from typing import List

class TodoInput(BaseModel):
    task: str = Field(..., description="Task description")
    priority: int = Field(1, ge=1, le=5, description="Priority (1-5)")

class TodoOutput(BaseModel):
    id: int
    task: str
    priority: int
    status: str

@chi_command(
    input_model=TodoInput,
    output_model=TodoOutput,
    description="Add a new todo item"
)
def add_todo(inp: TodoInput) -> TodoOutput:
    # Your business logic here
    return TodoOutput(
        id=1,
        task=inp.task,
        priority=inp.priority,
        status="pending"
    )

# Build and run your CLI
if __name__ == "__main__":
    cli = build_cli("todo-app")
    cli()
```

## Usage

### As a CLI
```bash
todo-app add-todo --task "Write documentation" --priority 5
```

### As a TUI
```bash
# Just add 'ui' - it's automatic!
todo-app ui
```

### With JSON output (for scripting)
```bash
todo-app --json add-todo --task "Write documentation" --priority 5
```

## Key Concepts

### Commands
Decorate your functions with `@chi_command` to make them available in both CLI and TUI modes.

### Models
Use Pydantic models to define input and output schemas. This ensures type safety and automatic validation.

### Emitters
Use `emit_ok()`, `emit_error()`, and `emit_progress()` to send structured responses that the TUI can display beautifully.

## API Reference

### Decorators

- `@chi_command()` - Register a command with typed I/O

### Functions

- `build_cli()` - Create a Click CLI from registered commands
- `emit_ok()` - Emit a success response
- `emit_error()` - Emit an error response
- `emit_progress()` - Emit progress updates for long-running tasks

### Utilities

#### Automatic `ui` subcommand

Every CLI built with CHI SDK automatically gets a `ui` subcommand:

```bash
my-app ui  # Launches the TUI
```

#### `chi-admin` - TUI Configuration & Tools

```bash
# Generate TUI configuration files with examples
chi-admin init . --binary-name=my-app
# Creates:
#   .tui/chi-index.yaml - Navigation entry (menu)
#   .tui/panel_b.yaml   - Panel configuration
#   .tui/styles.yaml    - Visual customization
#   .tui/bin/my-app-ui - Standalone launcher

# Check if everything is set up correctly
chi-admin doctor
```

The generated YAML files include detailed comments to help you customize your TUI.

#### Ensure TUI binary (`chi-tui`)

```bash
# Build from local Rust sources
chi-admin ensure-chi --compile

# Or download a prebuilt binary
chi-admin ensure-chi --download
```

#### `chi-tui` - Direct TUI launcher

```bash
CHI_APP_BIN=my-app chi-tui
```

## Examples

See the [example-apps](../example-apps/) directory for complete working examples:

- `example-app` - Interactive reference implementation with:
  - F1-F6 navigation for different feature categories
  - Comprehensive widget demos (lists, forms, panels, progress)
  - Built-in documentation and guides
  - Copy-paste ready patterns for your own apps

## License

Apache 2.0 - See [LICENSE](LICENSE) for details.

The included TUI binary has its own license (AGPL 3.0).

## Headless Smoke (CI-friendly)

You can run the TUI headlessly for quick smoke checks in CI:

```bash
# Run headless for N ticks and print a summary
CHI_TUI_HEADLESS=1 CHI_TUI_TICKS=20 CHI_TUI_SMOKE_SUMMARY=1 \
your-app ui

# Auto-enter a specific menu item by id (from your .tui/chi-index.yaml)
CHI_TUI_HEADLESS=1 CHI_TUI_HEADLESS_ENTER_ID=watchdog_stats \
your-app ui
```

Environment variables:
- `CHI_TUI_HEADLESS=1` — enable headless (non-interactive) mode
- `CHI_TUI_TICKS=<n>` — number of render ticks to run before exit
- `CHI_TUI_SMOKE_SUMMARY=1` — print a compact JSON summary to stdout
- `CHI_TUI_HEADLESS_ENTER_ID=<menu_id>` — auto-enter a menu item by id

Tip: when running via the binary directly, ensure the backend is set:

```bash
chi-admin ensure-chi --download
CHI_APP_BIN=your-app CHI_TUI_HEADLESS=1 CHI_TUI_TICKS=20 chi-tui
```
