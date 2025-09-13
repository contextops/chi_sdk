# About CHI SDK

CHI SDK lets you add beautiful Terminal UIs to your Python CLIs without rewriting any code. Just decorate your functions with `@chi_command` and get an automatic `ui` subcommand.

## Why CHI SDK?

- **Zero Learning Curve**: Keep writing Python with Click and Pydantic
- **Automatic TUI**: Every CLI gets a `ui` subcommand out of the box
- **Type Safety**: Pydantic models ensure data correctness
- **No Duplicated Logic**: Your Python code remains the single source of truth
- **Production Ready**: Fast, responsive UI powered by native code

## Ideal For

- Teams with existing Python CLIs wanting a modern TUI
- Data analysis tools and scientific computing applications
- DevOps dashboards and monitoring tools
- Internal tools and admin interfaces
- Any CLI that would benefit from an interactive interface

## How It Works

1. Write your CLI commands with Pydantic models for input/output
2. Use `build_cli()` to create your Click application
3. Run `your-app ui` to launch the TUI
4. The TUI automatically generates forms from your Pydantic schemas
5. User interactions call your Python commands behind the scenes
