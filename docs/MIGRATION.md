# Configuration Layout

The TUI reads configuration exclusively from a directory pointed to by `CHI_TUI_CONFIG_DIR`. The entry file is `chi-index.yaml` inside that directory. All relative paths in YAML resolve against `CHI_TUI_CONFIG_DIR`.

## Discovery (when CHI_TUI_CONFIG_DIR is not set)
If `CHI_TUI_CONFIG_DIR` is not provided, the TUI auto-discovers `chi-index.yaml` in the following locations:

1. `./chi-index.yaml`
2. `./.tui/chi-index.yaml`
3. Ancestors: `<ancestor>/.tui/chi-index.yaml` (walking up to the filesystem root)
4. `~/.tui/chi-index.yaml`

When found, `CHI_TUI_CONFIG_DIR` is set to the directory containing `chi-index.yaml`.

## Recommended Project Structure

```
project/
  .tui/
    chi-index.yaml   # entry screen (menu, options)
    panels/          # reusable panel specs
    styles.yaml      # optional styles
```

## Horizontal Menu (optional)
Add horizontal tabs (F1–F12) to any screen:

```yaml
horizontal_menu:
  - id: "home"
    title: "Home"
  - id: "settings"
    title: "Settings"
    config: "settings.yaml"  # path relative to CHI_TUI_CONFIG_DIR
```
