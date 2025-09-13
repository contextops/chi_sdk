"""Human-readable output renderer for CLI commands."""

from typing import Any
import json
import click


def render_human_output(data: Any) -> None:
    """
    Render command output in a human-readable format.

    This function intelligently formats different data types:
    - Strings are printed as-is
    - Lists with 'items' key are formatted as bullet points
    - Single-field dicts show just the value
    - Multi-field dicts show as key: value pairs
    - Complex structures fall back to formatted JSON

    Args:
        data: The data to render (typically a dict from Pydantic model)
    """
    if isinstance(data, str):
        click.echo(data)
    elif isinstance(data, dict):
        _render_dict(data)
    elif isinstance(data, list):
        _render_list(data)
    else:
        # Default JSON output for other types
        click.echo(json.dumps(data, indent=2, ensure_ascii=False))


def _render_dict(data: dict) -> None:
    """Render a dictionary in human-readable format."""
    # Special handling for ItemsOut-like structures
    if "items" in data and isinstance(data["items"], list):
        items = data["items"]
        if items:
            _render_items_list(items)
        else:
            click.echo("No items found.")
    elif len(data) == 1:
        # Single field dict - just show the value
        key, value = next(iter(data.items()))
        if isinstance(value, str):
            click.echo(value)
        else:
            click.echo(json.dumps(value, ensure_ascii=False))
    else:
        # Multi-field dict - show as key: value pairs
        for key, value in data.items():
            if isinstance(value, (str, int, float, bool)):
                click.echo(f"{key}: {value}")
            else:
                click.echo(f"{key}: {json.dumps(value, ensure_ascii=False)}")


def _render_list(data: list) -> None:
    """Render a list in human-readable format."""
    if not data:
        click.echo("No items found.")
        return

    # Check if all items are simple strings
    if all(isinstance(item, str) for item in data):
        for item in data:
            click.echo(f"• {item}")
    # Check if all items are dicts with title/name
    elif all(isinstance(item, dict) for item in data):
        _render_items_list(data)
    else:
        # Mixed or complex items - use JSON
        click.echo(json.dumps(data, indent=2, ensure_ascii=False))


def _render_items_list(items: list) -> None:
    """Render a list of item dictionaries."""
    # If items have 'title' or 'name', display as a simple list
    if all(
        isinstance(item, dict) and ("title" in item or "name" in item) for item in items
    ):
        last_command = None
        for item in items:
            title = item.get("title") or item.get("name") or str(item)
            parts = [f"• {title}"]

            # Add other important fields
            if "value" in item:
                parts.append(f"[{item['value']}]")
            if "status" in item:
                parts.append(f"[{item['status']}]")
            if "id" in item:
                parts.append(f"[id:{item['id']}]")

            click.echo(" ".join(parts))

            # Track the last command for hint
            if "command" in item:
                last_command = item["command"]

        # Show hint for the last command if available
        if last_command:
            click.echo()  # Empty line for spacing
            click.echo(click.style(f"Hint: {last_command}", dim=True))
    else:
        # Fallback to JSON for complex items
        click.echo(json.dumps({"items": items}, indent=2, ensure_ascii=False))
