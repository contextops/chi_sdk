

01-RAW:

Jako python developer przeglądam dokumentację i nadal nie wiem dokładnie jak tego używać. 

Projet ten tworzony był z myślą o dwóch use-case'ach:


CASE-1:
Jestem python dev, chcę dorobić TUI do mojej aplikacji. 
Nie chcę kompilować rust (potrzebujemy git automatyzacji do prebuilded whl pod wszystkie systemy)
Chcę dodać repo do wymagań, zainstalować a następnie:


zrobić w terminalu:

> cd /home/user/code/<my-project>
> chi-tui admin init . --binary-name=mypro --config=/home/user/code/.tui/


to zrobi "hocki klocki" tak aby:
1) zainstaluje bin pod mój system (win/libux/man)
2) default nazwa funkcjonowała jako "mypro[.exe]" (alias? rename?)
3) utworzy katalog ".tui", a w nim config.yaml, README.md (z instrukcją użycia)

by ostatecznie móc:

> mypro ui

CASE-1-B:
Tak samo, ale instaluje chi-sdk[dev], co otwiera mi drogę aby:
> chi-tui admin init . --binary-name=mypro --config=/home/user/code/.tui/ --include-src

które dodatkowo utworzy: banner.rs, background.rs, custom_hooks.rs w ".tui"
i pozwoli potem:

> chi-tui admin rebuild (wymaga toolingu rust, chyba ze to tez damy rade zautomatyzowac instalacje, o ile to dobra praktyka. ew. instrukcje w .tui/README.md)




CASE-2:
Jestem dowolnym dev, potrzebuję w bardziej zaawansowany sposób dostosować apkę.
> git clone <repo>

and go from there