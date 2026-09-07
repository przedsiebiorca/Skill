#!/usr/bin/env python3
"""Generuje artboardy .dc.html (kanwa projektowa) oraz jeden plik HTML do druku
z tych samych fragmentów treści. Uruchom: python3 build.py"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 794, 1123  # A4 @ 96 dpi

FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&family=IBM+Plex+Sans:wght@400;500;600&display=swap">'

CSS = """
  body { margin: 0; background: #e8e4dc; font-family: 'IBM Plex Sans', 'Segoe UI', system-ui, Helvetica, Arial, sans-serif; color: #1c1a17; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  a { color: #22402e; text-decoration: none; } a:hover { color: #163020; }
  .page { font-size: 15.5px; font-variant-numeric: lining-nums; position: relative; width: 794px; height: 1123px; box-sizing: border-box; background: #f7f4ee; overflow: hidden; padding: 52px 56px 48px 56px; display: flex; flex-direction: column; }
  .serif { font-family: 'Cormorant Garamond', Georgia, 'Times New Roman', serif; }
  .eyebrow { font-size: 12px; letter-spacing: 0.18em; text-transform: uppercase; color: #22402e; font-weight: 600; }
  .topbar { display: flex; justify-content: space-between; align-items: center; padding-bottom: 14px; border-bottom: 1px solid #22402e; }
  .brand { font-family: 'Cormorant Garamond', Georgia, serif; font-size: 22px; font-weight: 600; letter-spacing: 0.04em; color: #22402e; }
  .brand span { font-weight: 500; font-style: italic; }
  .h1 { font-family: 'Cormorant Garamond', Georgia, serif; font-weight: 500; font-size: 50px; line-height: 1.06; margin: 0; letter-spacing: -0.01em; text-wrap: pretty; }
  .h2 { font-family: 'Cormorant Garamond', Georgia, serif; font-weight: 500; font-size: 34px; line-height: 1.1; margin: 0; letter-spacing: -0.005em; }
  .h3 { font-family: 'Cormorant Garamond', Georgia, serif; font-weight: 600; font-size: 22px; line-height: 1.2; margin: 0; }
  .lead { font-family: 'Cormorant Garamond', Georgia, serif; font-size: 21px; line-height: 1.4; font-style: italic; color: #3a3631; margin: 0; }
  .body { font-size: inherit; line-height: 1.55; margin: 0; text-wrap: pretty; }
  .small { font-size: 12px; line-height: 1.45; color: #5d5850; }
  .rule { height: 1px; background: #d9d3c7; }
  .photo { background: #dfe3d8; border: 1px solid #c9d0c1; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 8px; color: #55634f; box-sizing: border-box; }
  .photo .cap { font-size: 12px; letter-spacing: 0.08em; text-transform: uppercase; font-weight: 500; }
  .stat { display: flex; flex-direction: column; gap: 2px; }
  .stat .v { font-family: 'Cormorant Garamond', Georgia, serif; font-size: 34px; font-weight: 600; line-height: 1; color: #1c1a17; }
  .stat .l { font-size: 12px; letter-spacing: 0.12em; text-transform: uppercase; color: #5d5850; }
  .row { display: flex; justify-content: space-between; gap: 16px; padding: 7px 0; border-bottom: 1px solid #e4dfd4; font-size: 15px; line-height: 1.35; }
  .row .n { flex: 1; } .row .a { font-weight: 500; white-space: nowrap; }
  .row.sum { border-bottom: 0; border-top: 1px solid #22402e; font-weight: 600; margin-top: 4px; }
  .check { display: flex; gap: 10px; align-items: flex-start; font-size: 14.5px; line-height: 1.4; }
  .check svg { flex: none; margin-top: 3px; }
  .box { background: #22402e; color: #f7f4ee; padding: 22px 26px; box-sizing: border-box; }
  .box .eyebrow { color: #b9c9b4; }
  .footer { margin-top: auto; padding-top: 12px; border-top: 1px solid #d9d3c7; display: flex; justify-content: space-between; align-items: center; font-size: 12px; color: #5d5850; letter-spacing: 0.04em; }
"""

ICON_PHOTO = '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#55634f" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="1.5"></rect><circle cx="9" cy="10" r="1.6"></circle><path d="M21 16l-5-5-8 8"></path></svg>'
CHECK = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#22402e" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12.5l5 5L20 7"></path></svg>'

def photo(h, cap, extra=""):
    return f'<div class="photo" style="height: {h}px; {extra}">{ICON_PHOTO}<div class="cap">{cap}</div></div>'

def topbar(right):
    return f'<div class="topbar"><div class="brand">Lidzbarska <span>Nieruchomości</span></div><div class="small" style="letter-spacing: 0.1em; text-transform: uppercase;">{right}</div></div>'

def footer(n):
    return f'<div class="footer"><div>Adrianna Lidzbarska &nbsp;·&nbsp; +48 727 926 639 &nbsp;·&nbsp; adrianna@lidzbarska.pl &nbsp;·&nbsp; lidzbarska.pl</div><div>{n} / 4</div></div>'

def check(t):
    return f'<div class="check">{CHECK}<div>{t}</div></div>'

def dist(n, d, t):
    return f'<div style="display: grid; grid-template-columns: 1.5fr 0.8fr 1fr; gap: 8px; padding: 7px 0; border-bottom: 1px solid #e4dfd4; font-size: 14px; line-height: 1.35; align-items: baseline;"><div>{n}</div><div style="font-weight: 500; white-space: nowrap;">{d}</div><div class="small" style="text-align: right; white-space: nowrap;">{t}</div></div>'

def row(n, a, cls=""):
    return f'<div class="row {cls}"><div class="n">{n}</div><div class="a">{a}</div></div>'

# ---------------------------------------------------------------- strona 1
P1 = f"""
<div class="page">
  {topbar("Oferta nr D/0001 · Sprzedaż · Dom")}
  <div style="margin-top: 28px;">{photo(400, "Zdjęcie główne (zdjęcie 1 z oferty)")}</div>
  <div style="margin-top: 34px; display: flex; flex-direction: column; gap: 14px;">
    <div class="eyebrow">Sycowa Huta · Kaszuby · woj. pomorskie</div>
    <h1 class="h1">Las z dwóch stron. Pięć jezior.<br>Gotowy dom na&nbsp;Kaszubach.</h1>
    <p class="lead">Dom premium wykończony pod klucz, ok. 7 minut od centrum Kościerzyny i&nbsp;około godziny od&nbsp;Gdańska.</p>
  </div>
  <div style="margin-top: 30px; display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 16px; padding: 22px 0; border-top: 1px solid #22402e; border-bottom: 1px solid #d9d3c7;">
    <div class="stat"><div class="v">120,05</div><div class="l">m² powierzchni</div></div>
    <div class="stat"><div class="v">580</div><div class="l">m² działki</div></div>
    <div class="stat"><div class="v">4</div><div class="l">pokoje</div></div>
    <div class="stat"><div class="v">2</div><div class="l">łazienki</div></div>
    <div class="stat"><div class="v">2026</div><div class="l">rok budowy</div></div>
  </div>
  <div style="margin-top: 22px; display: flex; justify-content: space-between; align-items: flex-end;">
    <div>
      <div class="eyebrow">Cena</div>
      <div class="serif" style="font-size: 44px; font-weight: 600; line-height: 1.05; margin-top: 4px;">1 400 000 zł <span style="font-size: 20px; font-weight: 500; font-style: italic; color: #5d5850;">brutto</span></div>
    </div>
    <div style="text-align: right; font-size: 14px; line-height: 1.45; color: #3a3631;">Kupujący nie płaci prowizji.<br>Możliwość zakupu w systemie płatności ratalnej.</div>
  </div>
  {footer(1)}
</div>
"""

# ---------------------------------------------------------------- strona 2
FEATURES = [
  "powierzchnia całkowita 120,05 m²",
  "technologia prefabrykowanych elementów betonowych",
  "wykończony pod klucz, gotowy do zamieszkania",
  "4 pokoje",
  "garaż jednostanowiskowy z pomieszczeniem technicznym i przejściem do części mieszkalnej",
  "miejsce postojowe przed garażem",
  "strych z wejściem na rzeczy sezonowe",
  "prywatny ogród z tarasem",
  "ogrzewanie podłogowe",
  "pompa ciepła VAILLANT",
  "rekuperacja AWENTA PRO",
  "klimatyzacja BOSCH w salonie i w każdej sypialni",
  "dach z blachy na rąbek stojący",
  "ogrodzona posesja: brama na pilota, furtka, domofon",
  "system monitoringu",
  "wyrównana działka z założonym trawnikiem",
]
P2 = f"""
<div class="page">
  {topbar("Opis nieruchomości")}
  <div style="margin-top: 26px; display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
    {photo(136, "Zdjęcie 2 z oferty")}
    {photo(136, "Zdjęcie 3 z oferty")}
  </div>
  <h2 class="h2" style="margin-top: 22px;">Są lokalizacje, których nie da się odtworzyć.</h2>
  <div style="margin-top: 16px; display: grid; grid-template-columns: 1fr 1fr; gap: 32px; font-size: 14.5px;">
    <div style="display: flex; flex-direction: column; gap: 10px;">
      <p class="body">Nie dlatego, że są daleko od cywilizacji. Wręcz przeciwnie – pozwalają każdego dnia korzystać z bliskości natury, nie rezygnując z wygody miasta.</p>
      <p class="body">Ten wyjątkowy dom położony jest w Sycowej Hucie, zaledwie ok. 7 minut od centrum Kościerzyny i ok. godziny od Gdańska. Od frontu oraz od strony prywatnego ogrodu i tarasu posesja graniczy z lasem, zapewniając mieszkańcom poczucie prywatności i zielony widok przez cały rok.</p>
      <p class="body">Sycowa Huta leży w sercu Pojezierza Kaszubskiego. W najbliższym otoczeniu znajduje się pięć jezior – Sudomie, Mielnica, Żołnowo, Sominko i Osuszno – połączonych rzeką Trzebiochą, tworzących system wodny ceniony przez miłośników kajakarstwa, żeglarstwa i aktywnego wypoczynku.</p>
      <p class="body">Dom został wykończony pod klucz i jest gotowy do zamieszkania. Nie wymaga dodatkowych nakładów ani czasu na wykończenie – od pierwszego dnia można cieszyć się jego komfortem.</p>
      <h3 class="h3" style="margin-top: 8px;">Solidna technologia wykonania</h3>
      <p class="body">Prefabrykacja betonowa daje wysoką trwałość, precyzję wykonania i bardzo dobrą izolacyjność akustyczną. Z pompą ciepła, rekuperacją i klimatyzacją tworzy energooszczędny dom na lata.</p>
    </div>
    <div>
      <div class="eyebrow" style="margin-bottom: 12px;">Najważniejsze informacje</div>
      <div style="display: flex; flex-direction: column; gap: 7px;">
        {"".join(check(f) for f in FEATURES)}
      </div>
    </div>
  </div>
  {footer(2)}
</div>
"""

# ---------------------------------------------------------------- strona 3
P3 = f"""
<div class="page">
  {topbar("Układ pomieszczeń")}
  <h2 class="h2" style="margin-top: 26px;">Przemyślany układ pomieszczeń</h2>
  <p class="lead" style="margin-top: 10px;">Wyraźny podział na strefę dzienną i prywatną – wygodny zarówno dla rodziny z dziećmi, jak i osób pracujących zdalnie.</p>
  <div style="margin-top: 26px; display: grid; grid-template-columns: 1fr 1fr; gap: 40px;">
    <div>
      <div style="display: flex; justify-content: space-between; align-items: baseline; border-bottom: 2px solid #22402e; padding-bottom: 8px;">
        <div class="h3">Parter</div><div class="serif" style="font-size: 20px; font-weight: 600;">60,41 m²</div>
      </div>
      {row("Salon z wyjściem na taras i ogród", "18,78 m²")}
      {row("Kuchnia otwarta na salon", "7,89 m²")}
      {row("Garaż w bryle budynku", "19,66 m²")}
      {row("Pomieszczenie techniczne", "4,32 m²")}
      {row("Wiatrołap z miejscem na zabudowę", "5,54 m²")}
      {row("Łazienka", "2,91 m²")}
      {row("Komunikacja", "1,32 m²")}
      <p class="body" style="margin-top: 14px; font-size: 14.5px; color: #3a3631;">Przestronna strefa dzienna z dużymi przeszkleniami. Widok na las sprawia, że natura staje się naturalnym tłem codzienności. Garaż ma bezpośrednie przejście do części mieszkalnej.</p>
    </div>
    <div>
      <div style="display: flex; justify-content: space-between; align-items: baseline; border-bottom: 2px solid #22402e; padding-bottom: 8px;">
        <div class="h3">Piętro</div><div class="serif" style="font-size: 20px; font-weight: 600;">59,64 m²</div>
      </div>
      {row("Sypialnia główna", "12,59 m²")}
      {row("Pokój (dziecięcy, gabinet lub gościnny)", "10,60 m²")}
      {row("Pokój (dziecięcy lub domowe biuro)", "8,12 m²")}
      {row("Łazienka z pralnią – wanna, podwójna umywalka", "9,17 m²")}
      {row("Garderoba", "3,68 m²")}
      {row("Komunikacja", "7,34 m²")}
      <p class="body" style="margin-top: 14px; font-size: 14.5px; color: #3a3631;">Prywatna część domu zaprojektowana z myślą o komforcie wszystkich domowników. Wydzielona strefa pralni z miejscem na pralkę i suszarkę. Dodatkowo strych z wejściem na rzeczy sezonowe.</p>
    </div>
  </div>
  <div style="margin-top: 30px;">
    <div class="eyebrow" style="margin-bottom: 12px;">Komfort i energooszczędność</div>
    <div style="display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px;">
      <div style="border-top: 1px solid #22402e; padding-top: 10px;"><div class="h3" style="font-size: 20px;">Pompa ciepła</div><div class="small" style="margin-top: 4px;">VAILLANT, z ogrzewaniem podłogowym w całym domu</div></div>
      <div style="border-top: 1px solid #22402e; padding-top: 10px;"><div class="h3" style="font-size: 20px;">Rekuperacja</div><div class="small" style="margin-top: 4px;">AWENTA PRO – zdrowy mikroklimat i niskie koszty</div></div>
      <div style="border-top: 1px solid #22402e; padding-top: 10px;"><div class="h3" style="font-size: 20px;">Klimatyzacja</div><div class="small" style="margin-top: 4px;">BOSCH w salonie i w każdej z trzech sypialni</div></div>
      <div style="border-top: 1px solid #22402e; padding-top: 10px;"><div class="h3" style="font-size: 20px;">Bezpieczeństwo</div><div class="small" style="margin-top: 4px;">brama na pilota, furtka, domofon, monitoring</div></div>
    </div>
  </div>
  <div style="margin-top: 30px; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px 24px; font-size: 14px; line-height: 1.4;">
    <div><div class="small" style="letter-spacing: 0.1em; text-transform: uppercase;">Rynek</div>pierwotny</div>
    <div><div class="small" style="letter-spacing: 0.1em; text-transform: uppercase;">Rodzaj zabudowy</div>wolnostojąca, 2 kondygnacje</div>
    <div><div class="small" style="letter-spacing: 0.1em; text-transform: uppercase;">Stan</div>do zamieszkania</div>
    <div><div class="small" style="letter-spacing: 0.1em; text-transform: uppercase;">Dach</div>blacha na rąbek stojący</div>
    <div><div class="small" style="letter-spacing: 0.1em; text-transform: uppercase;">Dojazd</div>bezpośrednio z drogi publicznej, droga gruntowa</div>
    <div><div class="small" style="letter-spacing: 0.1em; text-transform: uppercase;">Parkowanie</div>garaż + miejsce postojowe przed garażem</div>
  </div>
  {footer(3)}
</div>
"""

# ---------------------------------------------------------------- strona 4
P4 = f"""
<div class="page">
  {topbar("Położenie · Kontakt")}
  <h2 class="h2" style="margin-top: 26px;">Między jeziorami Sudomie i Mielnica</h2>
  <p class="lead" style="margin-top: 10px;">Las od frontu i za ogrodem. Codzienny spacer nad wodę, rower czy spływ kajakowy mogą stać się naturalną częścią życia.</p>
  <div style="margin-top: 24px; display: grid; grid-template-columns: 1fr 1fr; gap: 40px;">
    <div>
      <div class="eyebrow" style="margin-bottom: 8px;">Odległości od domu</div>
      {dist("Jezioro Sudomie", "ok. 350 m", "4–5 min pieszo")}
      {dist("Jezioro Mielnica", "ok. 600 m", "7–8 min pieszo")}
      {dist("Jezioro Żołnowo", "ok. 1 km", "ok. 12 min pieszo")}
      {dist("Rzeka Trzebiocha", "ok. 1 km", "12–14 min pieszo")}
      {dist("Jezioro Sominko", "ok. 1,5 km", "ok. 6 min rowerem")}
      {dist("Jezioro Osuszno", "ok. 1,8 km", "ok. 7 min rowerem")}
      {dist("Centrum Kościerzyny", "ok. 7 min", "autem")}
      {dist("Gdańsk", "ok. 60 min", "autem")}
    </div>
    <div style="display: flex; flex-direction: column; gap: 14px;">
      {photo(170, "Zdjęcie 4 z oferty (ogród / las)")}
      <h3 class="h3">Dom do życia. Miejsce na odpoczynek.</h3>
      <p class="body" style="font-size: 14.5px;">Dla osób, które chcą mieszkać w otoczeniu natury, nie rezygnując z wygody i bliskości miasta. Sprawdzi się też jako second home na Kaszubach.</p>
    </div>
  </div>
  <div style="margin-top: 24px; display: grid; grid-template-columns: 1.15fr 1fr; gap: 20px;">
    <div class="box" style="display: flex; flex-direction: column; gap: 10px;">
      <div class="eyebrow">Cena</div>
      <div class="serif" style="font-size: 40px; font-weight: 600; line-height: 1;">1 400 000 zł <span style="font-size: 18px; font-weight: 500; font-style: italic;">brutto</span></div>
      <div style="font-size: 14px; line-height: 1.5; color: #dfe6da;">Zakup bez prowizji po stronie Kupującego. Możliwość zakupu w systemie płatności ratalnej, bez konieczności kredytu bankowego – szczegóły podczas indywidualnego kontaktu.</div>
    </div>
    <div style="border: 1px solid #22402e; padding: 22px 24px; box-sizing: border-box; display: flex; flex-direction: column; gap: 6px;">
      <div class="eyebrow">Opiekun oferty</div>
      <div class="serif" style="font-size: 26px; font-weight: 600; line-height: 1.1; margin-top: 2px;">Adrianna Lidzbarska</div>
      <div class="small" style="font-size: 13px;">Lidzbarska Nieruchomości</div>
      <div style="font-size: 16px; font-weight: 500; margin-top: 8px;">+48 727 926 639</div>
      <div style="font-size: 15px;">adrianna@lidzbarska.pl</div>
      <div style="font-size: 15px;">lidzbarska.pl</div>
    </div>
  </div>
  <div style="margin-top: 18px;">
    <h3 class="h3">Indywidualna prezentacja</h3>
    <p class="body" style="margin-top: 6px; font-size: 14.5px;">Zakup domu to jedna z najważniejszych decyzji, dlatego warto zobaczyć tę nieruchomość osobiście. Z przyjemnością oprowadzę Państwa po domu, przedstawię jego układ i zastosowane rozwiązania techniczne oraz odpowiem na wszystkie pytania. Zapraszam do kontaktu i umówienia terminu spotkania.</p>
  </div>
  <p class="small" style="margin-top: 16px; font-size: 11.5px;">Przedstawiona oferta ma charakter poglądowy i może zawierać uproszczenia lub błędy. Niniejsze ogłoszenie nie stanowi oferty w rozumieniu art. 66 § 1 Kodeksu cywilnego. Współpracujemy z innymi biurami nieruchomości.</p>
  {footer(4)}
</div>
"""

PAGES = [("Main", P1), ("Opis", P2), ("Uklad", P3), ("Lokalizacja", P4)]

DC = """<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
  %s
  <style>%s</style>
</helmet>
%s
</x-dc>
</body>
</html>
"""

for name, html in PAGES:
    with open(os.path.join(HERE, f"{name}.dc.html"), "w", encoding="utf-8") as f:
        f.write(DC % (FONTS, CSS, html.strip()))

PRINT = """<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<title>Dom Sycowa Huta – oferta D/0001</title>
%s
<style>%s
  @page { size: 210mm 297mm; margin: 0; }
  html, body { background: #fff; }
  .page { page-break-after: always; break-after: page; }
  .page:last-child { page-break-after: auto; }
</style>
</head>
<body>
%s
</body>
</html>
"""
fonts_head = FONTS
if "--fonts" in sys.argv:
    fonts_head = "<style>" + open(sys.argv[sys.argv.index("--fonts") + 1], encoding="utf-8").read() + "</style>"
with open(os.path.join(HERE, "dom-sycowa-huta-druk.html"), "w", encoding="utf-8") as f:
    f.write(PRINT % (fonts_head, CSS, "\n".join(h.strip() for _, h in PAGES)))
print("ok")
