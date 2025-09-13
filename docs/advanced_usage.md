# Advanced Usage

## Custom TUI Configuration

Customize your TUI's appearance and behavior with YAML configuration:

```bash
# Generate configuration templates
chi-admin init . --binary-name=my-app
```

This creates:
- `.tui/chi-index.yaml` - Entry screen (menu structure and navigation)
- `.tui/panels/` - Panel layouts and widgets
- `.tui/styles.yaml` - Colors and visual theming

### Menu Customization

Edit `.tui/chi-index.yaml` to define your menu structure:

```yaml
header: "My App - Terminal UI"
menu:
  - id: "data-ops"
    title: "Data Operations"
    items:
      - id: "import"
        title: "Import Data"
        cmd: "${APP_BIN} import-data"
      - id: "export"
        title: "Export Results"
        cmd: "${APP_BIN} export --format json"
```

## Customizing Human-Readable Output

By default, CHI SDK provides automatic formatting for CLI output when not in JSON mode. You can customize this in three ways (in order of precedence):

### 1. Custom Renderer Function

Most flexible option for per-command formatting:

```python
@chi_command(
    output_model=ItemsOut,
    human_renderer=lambda data: "\n".join(
        f"📌 {item['title']} (use --tag {item['id']})" 
        for item in data.get('items', [])
    )
)
def list_tags() -> ItemsOut:
    return ItemsOut(items=[
        {"title": "urgent", "id": "urgent"},
        {"title": "normal", "id": "normal"},
    ])
```

### 2. Model `__str__` Method

Object-oriented approach for model-specific formatting:

```python
class SumOut(BaseModel):
    total: float
    count: int
    
    def __str__(self):
        return f"Sum of {self.count} numbers: {self.total}"

@chi_command(output_model=SumOut)
def sum_numbers(inp: SumIn) -> SumOut:
    return SumOut(total=sum(inp.numbers), count=len(inp.numbers))
```

### 3. Default Renderer

Automatic formatting for common patterns:
- Lists with `title`/`name` become bullet points
- Fields like `id`, `status`, `value` shown in brackets
- Single values display directly
- Multi-field dicts show as key: value pairs

## Streaming Progress

Handle long-running operations with progress streaming:

```python
from chi_sdk import emit_progress
import time

@chi_command(output_model=ResultModel)
def process_data() -> ResultModel:
    items = load_items()
    for i, item in enumerate(items):
        emit_progress(
            message=f"Processing {item.name}",
            percent=(i / len(items)) * 100,
            stage="processing",
            command="process-data"
        )
        process_item(item)
        
    return ResultModel(processed=len(items))
```

## JSON Output for Automation

All commands support JSON output for scripting:

```bash
# Get structured output
my-app --json process-data | jq '.data.processed'

# Stream progress events
my-app --json long-task | jq -c 'select(.type == "progress")'
```

## Packaging Your Application

### As a Python Package

In your `pyproject.toml`:

```toml
[project]
dependencies = [
    "chi-sdk>=0.0.5",
    "pydantic>=2.0",
    "click>=8.0"
]

[project.scripts]
my-app = "my_app.cli:main"
```

### Distributing to Users

```bash
# Users install your app
pip install my-app

# They get both CLI and TUI
my-app --help      # CLI mode
my-app ui          # TUI mode
```
