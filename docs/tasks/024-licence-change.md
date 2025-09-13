Super, teraz to się wyostrzyło 🔍

Twoje 3 punkty oznaczają:

Zero „żebrania” o wsparcie – nie budujesz modelu donacji/patronatu.

Ochrona przed Claude Code scenario – duża firma nie może wziąć Twojego TUI, zamknąć i sprzedawać jako własny komponent.

Ale furtka istnieje – jeśli ktoś naprawdę chce mieć prawo „zrobić co chce” (np. duży vendor), to musi przyjść do Ciebie i kupić licencję komercyjną.

To jest klasyczny przypadek dual-licensing z mocnym copyleftem w wersji publicznej.

Najlepsze dopasowanie: AGPL-3.0 + komercyjna licencja

Public release: AGPL-3.0

Każdy, kto używa lub hostuje TUI w SaaS, musi udostępnić źródło.

Dzięki temu nie ma opcji „Claude Code bierze i zamyka”.

Komercyjna licencja: dla firm, które chcą zrobić co chcą (zamknąć, wsadzić w Claude Code, dystrybuować w SaaS bez open-sourcingu).

Tu Ty jesteś „gatekeeper” – jeśli chcą, to płacą.

Jak to działa w praktyce

Community / indywidualni devowie: korzystają z AGPL-3.0. Mogą forkować, mogą modyfikować, mogą hostować własne open-source’owe projekty.

Duże firmy:

Jeśli chcą wbudować TUI w closed-source produkt → AGPL im to uniemożliwia.

Jeśli naprawdę potrzebują → kontaktują się z Tobą po komercyjną licencję.

Ty nie musisz aktywnie sprzedawać – tylko jasno piszesz w README:

„Ten projekt jest dostępny na licencji AGPL-3.0. Dla zastosowań komercyjnych lub closed-source dostępna jest licencja komercyjna – proszę o kontakt.”

Jakie pliki/licencje do repo

LICENSE → pełny tekst AGPL-3.0.

COMMERCIAL_LICENSE.md → prosty opis:

„Jeśli chcesz używać w komercyjnym produkcie/SaaS bez udostępniania kodu – skontaktuj się z nami, dostępna jest płatna licencja komercyjna.”

README → sekcja Licensing z krótkim FAQ:

Q: Mogę używać w moim projekcie open-source? → Tak, AGPL.

Q: Mogę używać w moim produkcie SaaS? → Tak, ale musisz udostępnić kod (AGPL) lub kupić licencję komercyjną.

Q: Mogę kupić licencję komercyjną? → Tak, napisz do…

SDK (Python)

Żeby nie utrudniać adopcji → Apache-2.0.

Developerzy mogą sobie spokojnie integrować w swoich projektach, nawet closed-source.

Wartość biznesowa i tak jest w TUI (którego nie mogą zamknąć przez AGPL).

Dzięki temu bariera wejścia = 0.

CLA (Contributor License Agreement)

Jeśli chcesz później móc sprzedawać komercyjne licencje → kontrybutorzy muszą Ci dać prawo relicencjonowania.

CLA (krótki, prosty, może być GitHub bot) mówi: „dajesz mi prawo dystrybuować Twój wkład także na warunkach komercyjnych”.

Inaczej możesz mieć kłopot: np. ktoś zrobi duży PR i formalnie nie możesz go sprzedać w licencji komercyjnej.

TL;DR – moja propozycja setupu

Rust TUI: AGPL-3.0 publicznie + komercyjna licencja dla zamkniętych użyć.

Python SDK: Apache-2.0, żeby każdy mógł integrować.

CLA: tak, musisz to mieć.

README/COMMERCIAL_LICENSE.md: jasny komunikat „open for community, pay if closed”.