# Dom Sycowa Huta – oferta D/0001 (prezentacja do druku)

Czterostronicowa prezentacja A4 nieruchomości z https://www.lidzbarska.pl/nieruchomosci/dom-sycowahuta-1

- `Dom-Sycowa-Huta-oferta-D0001.pdf` – gotowy PDF do druku (A4, 4 strony, fonty osadzone).
- `Dom-Sycowa-Huta-oferta-D0001.docx` – ta sama prezentacja w formacie Word (do edycji, wstawienia zdjęć w oznaczone pola).
- `build_docx.js` – generator wersji DOCX (`node build_docx.js`, wymaga pakietu `docx`).
- `build.py` – generator: z jednego źródła treści tworzy artboardy `*.dc.html` (kanwa projektowa) oraz `dom-sycowa-huta-druk.html` (wersja do druku).
- `canvas.json` – układ artboardów na kanwie.

Zdjęcia: strona lidzbarska.pl nie była osiągalna z sesji, więc w projekcie są oznaczone miejsca na zdjęcia nr 1–4 z oferty.

Odświeżenie PDF (Chromium/Playwright): `python3 build.py`, a następnie wydruk `dom-sycowa-huta-druk.html` do PDF w formacie A4 bez marginesów.
