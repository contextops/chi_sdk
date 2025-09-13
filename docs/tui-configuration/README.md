# TUI Configuration Guide

This guide explains how to configure the Terminal User Interface for your CHI SDK application.

## Overview

The TUI is configured through YAML files in the `.tui/` directory of your application. These files control:
- Navigation menus
- Panel layouts
- Form configurations
- Widget properties
- Visual styling

## Core Configuration Files

### 1. `chi-index.yaml` - Navigation Menu
Defines the main menu structure and command mappings.

```yaml
# Example structure
root:
  - id: command_1
    label: "My Command"
    command: "my-command"
    panel: "panel_b.yaml"
  - id: submenu_1
    label: "Submenu"
    children:
      - id: command_2
        label: "Nested Command"
        command: "nested-command"
```

See [chi-index-example.yaml](chi-index-example.yaml) for a complete example.

### 2. `config.yaml` - Global Settings
Controls TUI behavior and appearance.

```yaml
# Example settings
title: "My Application"
theme: "dark"
refresh_rate: 60
```

See [config-example.yaml](config-example.yaml) for all available options.

### 3. Panel Configuration Files
Define layouts and widget arrangements for different screens.

Common panel types:
- **Forms** - User input screens
- **Lists** - Selection menus
- **Progress** - Long-running task displays
- **Results** - Output visualization

See [panels-example.yaml](panels-example.yaml) and [forms-example.yaml](forms-example.yaml) for examples.

## Widget Documentation

Detailed documentation for each widget type:
- [Form Widget](../widgets/form.md) - Interactive input forms
- [Menu Widget](../widgets/menu.md) - Navigation menus
- [Panel Widget](../widgets/panel.md) - Layout containers
- [Markdown Widget](../widgets/markdown.md) - Rich text display
- [JSON Viewer](../widgets/json_viewer.md) - Structured data display
- [Result Viewer](../widgets/result_viewer.md) - Command output display
- [Watchdog Widget](../widgets/watchdog.md) - Process monitoring

## Directory Structure

```
your-app/
├── .tui/
│   ├── chi-index.yaml      # Main navigation menu
│   ├── config.yaml          # Global configuration
│   ├── panels/              # Panel configurations
│   │   ├── form_*.yaml      # Form panels
│   │   ├── list_*.yaml      # List panels
│   │   └── panel_*.yaml     # Custom panels
│   ├── bin/                 # TUI binary (auto-created)
│   └── docs/                # In-app documentation
├── src/                     # Your Python code
└── pyproject.toml
```

## Creating Your Configuration

1. **Initialize TUI configuration:**
   ```bash
   chi-admin init . --binary-name=my-app
   ```

2. **Customize the generated files:**
   - Edit `.tui/chi-index.yaml` to define your menu structure
   - Modify `.tui/config.yaml` for global settings
   - Create panel files in `.tui/panels/` for each screen

3. **Test your configuration:**
   ```bash
   my-app ui
   ```

## YAML Schema Reference

For complete YAML schema documentation, see [widgets_spec.md](../widgets_spec.md).

## Best Practices

1. **Keep panel files focused** - One screen per file
2. **Use meaningful IDs** - Makes debugging easier
3. **Comment your YAML** - Explain complex configurations
4. **Test incrementally** - Add features one at a time
5. **Version control** - Track `.tui/` directory in git

## Examples

### Simple Form Panel
```yaml
# .tui/panels/form_hello.yaml
type: form
title: "Hello Form"
fields:
  - name: "name"
    label: "Your Name"
    type: "text"
    required: true
  - name: "age"
    label: "Your Age"
    type: "number"
    min: 0
    max: 150
```

### List with Actions
```yaml
# .tui/panels/list_actions.yaml
type: list
title: "Select Action"
items:
  - id: "create"
    label: "Create New"
    command: "create-item"
  - id: "edit"
    label: "Edit Existing"
    command: "edit-item"
  - id: "delete"
    label: "Delete"
    command: "delete-item"
    confirm: true
```

## Troubleshooting

### TUI doesn't start
- Check YAML syntax: `yamllint .tui/*.yaml`
- Verify chi-tui binary: `chi-admin ensure-chi`
- Check logs: Look for error messages in terminal

### Commands not working
- Verify command names match your CLI: `my-app --help`
- Check chi-index.yaml command mappings
- Ensure your CLI implements `--chi-expose-bundle`

### Layout issues
- Review panel type compatibility
- Check widget nesting rules
- Validate against schema in widgets_spec.md

## Additional Resources

- [CHI TUI Source Code](https://github.com/contextops/chi_tui)
- [Example Application](https://github.com/contextops/chi_tui/tree/main/example-app)
- [Widget Development Guide](../widgets_spec.md)