
## Open Questions
>> - Env var name: migrate from `EXAMPLE_APP_BIN` to `CHI_APP_BIN`? Provide compatibility shim?
chi-sdk jeszcze nie ma żadnych userów, nigdy nie zostało upublicznione to doskonały moment na cleanup porządny - bez warstwy kompatybilności
>> Zgoda. Standaryzujemy na `CHI_APP_BIN` i usuwamy `EXAMPLE_APP_BIN` bez shimu.
>> Działania: aktualizuję TUI i przykłady na `CHI_APP_BIN`; wrapper i `chi-admin` ustawiają to samo; README/tests dostosuję w tej iteracji.

>> - Wrapper install location: keep in `.tui/bin/` or also symlink to a user‑local bin (e.g., `~/.local/bin`)?
".tui/bin" jakoś źle pachnie. czy prawdziwa "binarka" nie powinna się ładować tam gdzie powinny się ładować wszystkie inne binarki w scenariuszu "pip install <pakiet>" ?
jakie są najlepsze praktyki
>> Najlepsza praktyka: binarka via wheel (`chi-tui-bin`) i console_script na PATH w aktywnej venv.
>> MVP (do czasu wheels): zapis binarki w cache użytkownika (Linux: `~/.cache/chi-tui`, macOS: `~/Library/Caches/chi-tui`, Windows: `%LOCALAPPDATA%\chi-tui`).
>> Wrapper jako skrypt konsolowy w bieżącej venv (`<venv>/bin/mypro-ui` lub `Scripts\\mypro-ui.exe`). Opcjonalnie `chi-admin link --user` doda symlink do `~/.local/bin`. Unikamy `.tui/bin` dla samych binarek.

>> - Minimal `config.yaml` shape — do chcemy tam również flagi startowe TUI?
nie rozumiem pytania
>> Doprecyzowanie: czy `.tui/config.yaml` ma trzymać ustawienia uruchomienia TUI. Propozycja minimalna:
>> - `app_bin: "mypro"` — nazwa backendu (fallback wobec `CHI_APP_BIN`).
>> - `extra_env: { CHI_TUI_JSON: "1" }` — opcjonalne nadpisania env.
>> - `nav_yaml: null` — opcjonalna ścieżka do własnego `nav.yaml`.
>> - (opcjonalnie) `ui_defaults: { wrap: true, theme: system }`.
>> Jeżeli wolisz ultra‑minimalnie, zostawimy tylko `app_bin` + `extra_env`.


>> - Czy `download` powinien zapisywać binarkę w repo (`.tui/bin`) czy w cache użytkownika?
będzie zależało od odp. na powyższe
>> Skoro unikamy `.tui/bin` dla binarek: zapis do cache użytkownika (patrz ścieżki wyżej).
>> Wrapper wskazuje binarkę z cache; `doctor` potrafi sprawdzić/wymusić ponowny download. Po wejściu w wheels cache nie będzie potrzebny.
