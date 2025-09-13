## Logika ładowania konfiguracji (YAML)

Poniżej zebrana jest aktualna (stan: bieżący kod) logika wyszukiwania i ładowania konfiguracji TUI.

### Stan obecny (uproszczony — wdrożone)

- Kotwica: `CHI_TUI_CONFIG_DIR` wskazuje katalog bazowy; wewnątrz oczekiwany jest `chi-index.yaml`.
- Główna funkcja: `rust-tui/src/ui.rs` → `load_config()`.
- Gdy `CHI_TUI_CONFIG_DIR` nie jest ustawione, TUI szuka `chi-index.yaml` w:
  - `CWD/chi-index.yaml`
  - `CWD/.tui/chi-index.yaml`
  - przodkach: `<ancestor>/.tui/chi-index.yaml`
  - `~/.tui/chi-index.yaml`
  Po znalezieniu ustawia `CHI_TUI_CONFIG_DIR` na katalog z plikiem.
- Przełączanie ekranów (F1–F12): `rust-tui/src/ui.rs` → `load_config_from_path()` — ścieżki względne zawsze względem `CHI_TUI_CONFIG_DIR`.
- Dodatkowe YAML-e (panel/menu/markdown): ścieżki relative → względem `CHI_TUI_CONFIG_DIR`, absolute → bez zmian. Błędy YAML zawierają lokalizację.

Przykłady zmiennych środowiskowych:
- `CHI_TUI_CONFIG_DIR=/abs/path/to/.tui`
- Ustawiane przez TUI: `CHI_TUI_CONFIG_DIR` (po autodetekcji).

Pliki źródłowe (kluczowe miejsca):
- `rust-tui/src/ui.rs` (funkcje: `load_config`, `load_config_from_path`, `init_logo_and_header`)
- `rust-tui/src/services/loader.rs` (`spawn_load_panel_yaml`)
- `rust-tui/src/chi_core/registry.rs` (rozwiązywanie widżetów/ścieżek)

### Uwagi operacyjne

- Zakładamy, że `chi-tui` jest w PATH (np. po `chi-admin ensure-chi`).
- Aplikacja może wystawiać podkomendę `ui` (zalecane): `your-app ui`.
- Alternatywnie: `CHI_APP_BIN=your-app chi-tui`.
