# Basic Usage

## Creating Commands

Define your commands using Pydantic models and the `@chi_command` decorator:

```python
from chi_sdk import chi_command, build_cli
from pydantic import BaseModel, Field
from typing import List

class SumInput(BaseModel):
    numbers: List[float] = Field(..., description="Numbers to sum")

class SumOutput(BaseModel):
    total: float
    count: int

@chi_command(input_model=SumInput, output_model=SumOutput)
def sum_numbers(inp: SumInput) -> SumOutput:
    return SumOutput(total=sum(inp.numbers), count=len(inp.numbers))
```

## Running Your App

### CLI Mode

Your app works as a standard CLI:

```bash
# Regular CLI usage
my-app sum-numbers --numbers 1 --numbers 2 --numbers 3

# Get JSON output for automation
my-app --json sum-numbers --numbers 1 --numbers 2
```

### TUI Mode

Every app automatically gets a TUI:

```bash
# Launch the interactive TUI
my-app ui
```

The TUI will:
- Display a menu of all your commands
- Auto-generate forms from your Pydantic models
- Show results in a beautiful interface
- Handle validation and error display

## Progress Tracking

For long-running tasks, emit progress updates:

```python
from chi_sdk import emit_progress

@chi_command(output_model=ResultModel)
def long_task() -> ResultModel:
    for i in range(100):
        emit_progress(
            message=f"Processing item {i+1}/100",
            percent=(i+1),
            stage="processing"
        )
        # Do work...
    return ResultModel(status="complete")
