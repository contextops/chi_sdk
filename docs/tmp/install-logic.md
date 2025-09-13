Instalacja i dostępność binarki TUI (upraszczone)

Cel: uproszczony przepływ instalacji oraz uruchamiania bez specjalnych skrótów typu „run-demo”.

Co instalujemy przez pip
- `pip install chi-sdk` — instaluje Python SDK i narzędzie `chi-admin`.

Zapewnienie binarki `chi-tui` w PATH
- `chi-admin ensure-chi` — narzędzie, które:
  - najpierw próbuje kompilacji z lokalnych źródeł Rust (wykrywa `rust-tui/` w repo albo źródła dołączone do pakietu),
  - jeśli kompilacja się nie powiedzie, próbuje pobrać gotową binarkę z wydań GitHub,
  - po sukcesie kopiuje binarkę do katalogu użytkownika i podpowiada, czy jest w `PATH`.

Warianty ręczne:
- `chi-admin ensure-chi --compile` — wymuś kompilację z lokalnych źródeł Rust i instalację do katalogu użytkownika.
- `chi-admin ensure-chi --download` — pobierz binarkę i zainstaluj do katalogu użytkownika.

Uruchamianie TUI (zamiast „run-demo”)
- Z poziomu Twojej aplikacji: `your-app ui` (wbudowana podkomenda `ui`).
- Albo wprost binarką: `CHI_APP_BIN=your-app chi-tui`.

Więcej o autodetekcji i ładowaniu konfiguracji: zobacz `docs/tmp/loading-logic.md`.
