# CHI SDK

Build beautiful Terminal User Interfaces for your Python CLI applications without rewriting your code.

## What is CHI SDK?

CHI SDK is a Python framework that lets you create CLI applications that can run in two modes:
- **CLI mode** - Traditional command-line interface
- **TUI mode** - Rich Terminal User Interface with forms, menus, and visualizations

The TUI is powered by a separate Rust application ([chi_tui](https://github.com/contextops/chi_tui)) that communicates with your Python code via JSON protocol. You write Python, users get a beautiful interface.

## Installation

```bash
pip install chi-sdk
```

This installs:
- The Python SDK for building commands
- Pre-built TUI binary (downloaded on first use)
- `chi-admin` tool for configuration

## Features

- 🎯 **Decorator-based** - Add TUI capabilities with simple decorators
- 🔒 **Type-safe** - Pydantic models for input/output validation
- 🚀 **Fast** - High-performance Rust TUI (separate binary)
- 📦 **Zero configuration** - Works out of the box
- 🔄 **Dual-mode** - Same code works as CLI and TUI
- 🎨 **Customizable** - YAML-based UI configuration

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
# Traditional command-line interface
todo-app add-todo --task "Write documentation" --priority 5
```

### As a TUI
```bash
# Launch the Terminal User Interface
todo-app ui

# The TUI provides:
# - Interactive forms for command inputs
# - Real-time output visualization
# - Navigation between commands
# - Progress indicators for long-running tasks
```

### With JSON output (for scripting)
```bash
# Machine-readable output for automation
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

### How the TUI Works

When you run `my-app ui`, the following happens:

1. **TUI Binary Launch** - The Rust-based TUI application starts
2. **Command Discovery** - TUI calls your Python app with `--chi-expose-bundle` to discover available commands
3. **User Interaction** - TUI presents forms and menus based on your command schemas
4. **Command Execution** - When user submits a form, TUI calls your Python app with the command and arguments
5. **Result Display** - TUI beautifully renders the output from your Python code

### Utilities

#### Automatic `ui` subcommand

Every CLI built with CHI SDK automatically gets a `ui` subcommand that launches the TUI:

```bash
my-app ui  # Launches the Terminal User Interface
```

#### `chi-admin` - TUI Configuration & Tools

```bash
# Generate TUI configuration files with examples
chi-admin init . --binary-name=my-app
# Creates:
#   .tui/chi-index.yaml - Command menu structure
#   .tui/panel_b.yaml   - Panel layouts
#   .tui/styles.yaml    - Visual customization
#   .tui/bin/my-app-ui - Standalone launcher script

# Check if everything is set up correctly
chi-admin doctor
```

The generated YAML files include detailed comments explaining each option.

#### TUI Binary Management

The TUI is a separate Rust binary ([source code](https://github.com/contextops/chi_tui)) that can be:

```bash
# Downloaded automatically (recommended)
chi-admin ensure-chi --download

# Or built from source if you have Rust installed
chi-admin ensure-chi --compile

# Build from GitHub source
git clone https://github.com/contextops/chi_tui
cd chi_tui
cargo build --release
cp target/release/chi-tui ~/.local/bin/
```

#### Direct TUI launch

```bash
# Launch TUI directly (useful for debugging)
CHI_APP_BIN=my-app chi-tui
```

## Architecture

```
┌─────────────────┐         JSON Protocol          ┌──────────────┐
│   Python App    │ ◄──────────────────────────► │   Rust TUI   │
│   (chi-sdk)     │         Commands/Results       │  (chi_tui)   │
└─────────────────┘                                └──────────────┘
       Your Code                                    Separate Binary
```

- **Python SDK** (this repo) - Decorators, models, and CLI builder
- **Rust TUI** ([chi_tui](https://github.com/contextops/chi_tui)) - High-performance terminal interface
- **Communication** - JSON-based protocol between Python and Rust

## Examples

For a complete working example, check out the [chi_tui repository](https://github.com/contextops/chi_tui) which includes an example application demonstrating:
- Interactive forms and menus
- Progress indicators
- Multiple panel layouts
- Custom styling

You can run the example directly from the chi_tui repo:
```bash
git clone https://github.com/contextops/chi_tui
cd chi_tui/example-app
./example-app-wrapper ui
```

## Related Projects

- **[chi_tui](https://github.com/contextops/chi_tui)** - The Rust TUI application that powers the interface
- **[example-app](https://github.com/contextops/chi_tui/tree/main/example-app)** - Full-featured example application

## License

Apache 2.0 - See [LICENSE](LICENSE) for details.

The TUI binary ([chi_tui](https://github.com/contextops/chi_tui)) is licensed under AGPL 3.0.

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
