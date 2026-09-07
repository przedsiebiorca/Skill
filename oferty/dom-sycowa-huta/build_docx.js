// Generuje wersję DOCX prezentacji: node build_docx.js
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, AlignmentType,
  BorderStyle, ShadingType, HeadingLevel, PageBreak, Header, Footer, TabStopType, PageNumber,
  LevelFormat, VerticalAlign, LineRuleType,
} = require("docx");

const GREEN = "22402E", INK = "1C1A17", MUTED = "5D5850", LINE = "D9D3C7", PHOTO = "DFE3D8", PAPER = "F7F4EE";
const SERIF = "Georgia", SANS = "Calibri";
const PAGE_W = 11906, MARGIN = 900, CONTENT = PAGE_W - 2 * MARGIN; // 10106 DXA
const GAP = 400, WC = Math.floor((CONTENT - GAP) / 2);

const none = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const noBorders = { top: none, bottom: none, left: none, right: none, insideHorizontal: none, insideVertical: none };
const line = (color = LINE, size = 6) => ({ style: BorderStyle.SINGLE, size, color });

const t = (text, o = {}) => new TextRun({ text, font: o.serif ? SERIF : SANS, size: o.size || 22, bold: o.bold, italics: o.italics, color: o.color || INK, characterSpacing: o.spacing, allCaps: o.caps });
const p = (children, o = {}) => new Paragraph({ children: Array.isArray(children) ? children : [children], alignment: o.align, spacing: { before: o.before || 0, after: o.after == null ? 0 : o.after, line: o.line || 276, lineRule: LineRuleType.AUTO }, border: o.border, keepNext: o.keepNext, keepLines: true });

const eyebrow = (s, o = {}) => p(t(s, { size: 17, bold: true, color: o.color || GREEN, spacing: 40, caps: true }), { before: o.before || 0, after: o.after || 100 });
const h1 = (s) => p(t(s, { serif: true, size: 60 }), { line: 240, after: 160 });
const h2 = (s, o = {}) => p(t(s, { serif: true, size: 44 }), { line: 240, before: o.before || 0, after: o.after || 140 });
const h3 = (s, o = {}) => p(t(s, { serif: true, size: 28, bold: true }), { before: o.before || 160, after: 80, keepNext: true });
const lead = (s, o = {}) => p(t(s, { serif: true, size: 26, italics: true, color: "3A3631" }), { line: 300, after: o.after || 200 });
const body = (s, o = {}) => p(t(s, { size: o.size || 20 }), { line: 270, after: o.after == null ? 120 : o.after });
const small = (s, o = {}) => p(t(s, { size: o.size || 16, color: MUTED }), { line: 260, after: o.after || 0 });
const bullet = (s) => new Paragraph({ children: [t(s, { size: 20 })], numbering: { reference: "bullets", level: 0 }, spacing: { after: 60, line: 270, lineRule: LineRuleType.AUTO } });

const cell = (children, width, o = {}) => new TableCell({
  children, width: { size: width, type: WidthType.DXA }, verticalAlign: o.valign || VerticalAlign.TOP,
  shading: o.fill ? { type: ShadingType.CLEAR, fill: o.fill, color: "auto" } : undefined,
  borders: o.borders || noBorders,
  margins: { top: o.pad == null ? 0 : o.pad, bottom: o.pad == null ? 0 : o.pad, left: o.padX == null ? 0 : o.padX, right: o.padX == null ? 0 : o.padX },
});
const table = (rows, widths) => new Table({ rows, columnWidths: widths, width: { size: widths.reduce((a, b) => a + b, 0), type: WidthType.DXA }, borders: noBorders });
const spacer = (h = 120) => new Paragraph({ spacing: { before: 0, after: 0, line: h, lineRule: "exact" }, children: [t("", { size: 2 })] });

const photoBox = (label, width, height) => table([new TableRow({ height: { value: height, rule: "exact" }, children: [cell([
  p(t("▢", { size: 32, color: "55634F" }), { align: AlignmentType.CENTER, after: 40 }),
  p(t(label, { size: 16, color: "55634F", spacing: 20, caps: true }), { align: AlignmentType.CENTER }),
], width, { fill: PHOTO, valign: VerticalAlign.CENTER, borders: { top: line("C9D0C1", 4), bottom: line("C9D0C1", 4), left: line("C9D0C1", 4), right: line("C9D0C1", 4) } })] })], [width]);

// wiersz "nazwa ........ wartość" z dolną linią
const kv = (name, value, o = {}) => new Paragraph({
  children: [t(name, { size: o.size || 20 }), new TextRun({ text: "\t", font: SANS, size: 20 }), t(value, { size: o.size || 20, bold: true })],
  tabStops: [{ type: TabStopType.RIGHT, position: WC - 10 }],
  spacing: { before: 70, after: 70, line: 260, lineRule: LineRuleType.AUTO }, border: { bottom: line("E4DFD4", 4) },
});

const stat = (v, l, w) => cell([p(t(v, { serif: true, size: 40, bold: true }), { after: 40 }), p(t(l, { size: 15, color: MUTED, spacing: 20, caps: true }))], w, { pad: 200, padX: 40 });

// ------------------------------------------------------------ strona 1
const W2 = Math.floor(CONTENT / 2), W5 = Math.floor(CONTENT / 5);
const page1 = [
  photoBox("Zdjęcie główne (zdjęcie 1 z oferty)", CONTENT, 5400),
  spacer(360),
  eyebrow("Sycowa Huta · Kaszuby · woj. pomorskie"),
  h1("Las z dwóch stron. Pięć jezior. Gotowy dom na Kaszubach."),
  lead("Dom premium wykończony pod klucz, ok. 7 minut od centrum Kościerzyny i około godziny od Gdańska."),
  new Table({ rows: [new TableRow({ children: [stat("120,05 m²", "powierzchnia", 2700), stat("580 m²", "działka", 2100), stat("4", "pokoje", 1600), stat("2", "łazienki", 1600), stat("2026", "rok budowy", CONTENT - 8000)] })],
    columnWidths: [2700, 2100, 1600, 1600, CONTENT - 8000], width: { size: CONTENT, type: WidthType.DXA }, borders: { ...noBorders, top: line(GREEN, 8), bottom: line(LINE, 6) } }),
  spacer(240),
  table([new TableRow({ children: [
    cell([eyebrow("Cena", { after: 40 }), p([t("1 400 000 zł ", { serif: true, size: 56, bold: true }), t("brutto", { serif: true, size: 26, italics: true, color: MUTED })])], W2, { valign: VerticalAlign.BOTTOM }),
    cell([p(t("Kupujący nie płaci prowizji.", { size: 20, color: "3A3631" }), { align: AlignmentType.RIGHT, after: 40 }), p(t("Możliwość zakupu w systemie płatności ratalnej.", { size: 20, color: "3A3631" }), { align: AlignmentType.RIGHT })], W2, { valign: VerticalAlign.BOTTOM }),
  ] })], [W2, W2]),
  new Paragraph({ children: [new PageBreak()] }),
];

// ------------------------------------------------------------ strona 2
const FEATURES = ["powierzchnia całkowita 120,05 m²", "technologia prefabrykowanych elementów betonowych", "wykończony pod klucz, gotowy do zamieszkania", "4 pokoje", "garaż jednostanowiskowy z pomieszczeniem technicznym i przejściem do części mieszkalnej", "miejsce postojowe przed garażem", "strych z wejściem na rzeczy sezonowe", "prywatny ogród z tarasem", "ogrzewanie podłogowe", "pompa ciepła VAILLANT", "rekuperacja AWENTA PRO", "klimatyzacja BOSCH w salonie i w każdej sypialni", "dach z blachy na rąbek stojący", "ogrodzona posesja: brama na pilota, furtka, domofon", "system monitoringu", "wyrównana działka z założonym trawnikiem"];
const page2 = [
  table([new TableRow({ children: [cell([photoBox("Zdjęcie 2 z oferty", WC, 1700)], WC), cell([p(t(""))], GAP), cell([photoBox("Zdjęcie 3 z oferty", WC, 1700)], WC)] })], [WC, GAP, WC]),
  spacer(240),
  h2("Są lokalizacje, których nie da się odtworzyć."),
  table([new TableRow({ children: [
    cell([
      body("Nie dlatego, że są daleko od cywilizacji. Wręcz przeciwnie – pozwalają każdego dnia korzystać z bliskości natury, nie rezygnując z wygody miasta."),
      body("Ten wyjątkowy dom położony jest w Sycowej Hucie, zaledwie ok. 7 minut od centrum Kościerzyny i ok. godziny od Gdańska. Od frontu oraz od strony prywatnego ogrodu i tarasu posesja graniczy z lasem, zapewniając mieszkańcom poczucie prywatności i zielony widok przez cały rok."),
      body("Sycowa Huta leży w sercu Pojezierza Kaszubskiego. W najbliższym otoczeniu znajduje się pięć jezior – Sudomie, Mielnica, Żołnowo, Sominko i Osuszno – połączonych rzeką Trzebiochą, tworzących system wodny ceniony przez miłośników kajakarstwa, żeglarstwa i aktywnego wypoczynku."),
      body("Dom został wykończony pod klucz i jest gotowy do zamieszkania. Nie wymaga dodatkowych nakładów ani czasu na wykończenie – od pierwszego dnia można cieszyć się jego komfortem."),
      h3("Solidna technologia wykonania", { before: 60 }),
      body("Prefabrykacja betonowa daje wysoką trwałość, precyzję wykonania i bardzo dobrą izolacyjność akustyczną. Z pompą ciepła, rekuperacją i klimatyzacją tworzy energooszczędny dom na lata.", { after: 0 }),
    ], WC),
    cell([p(t(""))], GAP),
    cell([eyebrow("Najważniejsze informacje", { after: 120 }), ...FEATURES.map(bullet)], WC),
  ] })], [WC, GAP, WC]),
  new Paragraph({ children: [new PageBreak()] }),
];

// ------------------------------------------------------------ strona 3
const floorHead = (name, area) => new Paragraph({
  children: [t(name, { serif: true, size: 28, bold: true }), new TextRun({ text: "\t", font: SERIF, size: 26 }), t(area, { serif: true, size: 26, bold: true })],
  tabStops: [{ type: TabStopType.RIGHT, position: WC - 10 }],
  spacing: { before: 0, after: 60, line: 260, lineRule: LineRuleType.AUTO }, border: { bottom: line(GREEN, 12) }, keepNext: true,
});
const feature = (title, desc, w) => cell([p(t(title, { serif: true, size: 26, bold: true }), { after: 40, border: { top: line(GREEN, 6) }, before: 120 }), small(desc, { size: 17 })], w, { padX: 0 });
const info = (label, value, w) => cell([p(t(label, { size: 15, color: MUTED, spacing: 30, caps: true }), { after: 20 }), p(t(value, { size: 20 }))], w, { pad: 80 });
const W4 = Math.floor((CONTENT - 3 * 240) / 4), G4 = 240, W3 = Math.floor(CONTENT / 3);
const page3 = [
  h2("Przemyślany układ pomieszczeń"),
  lead("Wyraźny podział na strefę dzienną i prywatną – wygodny zarówno dla rodziny z dziećmi, jak i osób pracujących zdalnie."),
  table([new TableRow({ children: [
    cell([floorHead("Parter", "60,41 m²"), kv("Salon z wyjściem na taras i ogród", "18,78 m²"), kv("Kuchnia otwarta na salon", "7,89 m²"), kv("Garaż w bryle budynku", "19,66 m²"), kv("Pomieszczenie techniczne", "4,32 m²"), kv("Wiatrołap", "5,54 m²"), kv("Łazienka", "2,91 m²"), kv("Komunikacja", "1,32 m²"),
      spacer(160), body("Przestronna strefa dzienna z dużymi przeszkleniami. Widok na las sprawia, że natura staje się naturalnym tłem codzienności. Garaż ma bezpośrednie przejście do części mieszkalnej.", { size: 19, after: 0 })], WC),
    cell([p(t(""))], GAP),
    cell([floorHead("Piętro", "59,64 m²"), kv("Sypialnia główna", "12,59 m²"), kv("Pokój (gabinet lub gościnny)", "10,60 m²"), kv("Pokój (dziecięcy lub biuro)", "8,12 m²"), kv("Łazienka z pralnią (wanna, 2 umywalki)", "9,17 m²"), kv("Garderoba", "3,68 m²"), kv("Komunikacja", "7,34 m²"),
      spacer(160), body("Prywatna część domu zaprojektowana z myślą o komforcie wszystkich domowników. Wydzielona strefa pralni z miejscem na pralkę i suszarkę. Dodatkowo strych z wejściem na rzeczy sezonowe.", { size: 19, after: 0 })], WC),
  ] })], [WC, GAP, WC]),
  spacer(360),
  eyebrow("Komfort i energooszczędność", { after: 0 }),
  table([new TableRow({ children: [
    feature("Pompa ciepła", "VAILLANT, z ogrzewaniem podłogowym w całym domu", W4), cell([p(t(""))], G4),
    feature("Rekuperacja", "AWENTA PRO – zdrowy mikroklimat i niskie koszty", W4), cell([p(t(""))], G4),
    feature("Klimatyzacja", "BOSCH w salonie i w każdej z trzech sypialni", W4), cell([p(t(""))], G4),
    feature("Bezpieczeństwo", "brama na pilota, furtka, domofon, monitoring", W4),
  ] })], [W4, G4, W4, G4, W4, G4, W4]),
  spacer(360),
  table([
    new TableRow({ children: [info("Rynek", "pierwotny", W3), info("Rodzaj zabudowy", "wolnostojąca, 2 kondygnacje", W3), info("Stan", "do zamieszkania", W3)] }),
    new TableRow({ children: [info("Dach", "blacha na rąbek stojący", W3), info("Dojazd", "bezpośrednio z drogi publicznej, droga gruntowa", W3), info("Parkowanie", "garaż + miejsce postojowe przed garażem", W3)] }),
  ], [W3, W3, W3]),
  new Paragraph({ children: [new PageBreak()] }),
];

// ------------------------------------------------------------ strona 4
const dist = (n, d, tm) => new Paragraph({
  children: [t(n, { size: 20 }), new TextRun({ text: "\t", font: SANS, size: 20 }), t(d, { size: 20, bold: true }), new TextRun({ text: "\t", font: SANS, size: 20 }), t(tm, { size: 16, color: MUTED })],
  tabStops: [{ type: TabStopType.LEFT, position: 2200 }, { type: TabStopType.RIGHT, position: WC - 60 }],
  spacing: { before: 70, after: 70, line: 260, lineRule: LineRuleType.AUTO }, border: { bottom: line("E4DFD4", 4) },
});
const WB = Math.floor((CONTENT - 300) / 2);
const page4 = [
  h2("Między jeziorami Sudomie i Mielnica"),
  lead("Las od frontu i za ogrodem. Codzienny spacer nad wodę, rower czy spływ kajakowy mogą stać się naturalną częścią życia."),
  table([new TableRow({ children: [
    cell([eyebrow("Odległości od domu", { after: 60 }), dist("Jezioro Sudomie", "ok. 350 m", "4–5 min pieszo"), dist("Jezioro Mielnica", "ok. 600 m", "7–8 min pieszo"), dist("Jezioro Żołnowo", "ok. 1 km", "12 min pieszo"), dist("Rzeka Trzebiocha", "ok. 1 km", "12–14 min pieszo"), dist("Jezioro Sominko", "ok. 1,5 km", "6 min rowerem"), dist("Jezioro Osuszno", "ok. 1,8 km", "7 min rowerem"), dist("Centrum Kościerzyny", "ok. 7 min", "autem"), dist("Gdańsk", "ok. 60 min", "autem")], WC),
    cell([p(t(""))], GAP),
    cell([photoBox("Zdjęcie 4 z oferty (ogród / las)", WC, 2400), spacer(200), h3("Dom do życia. Miejsce na odpoczynek.", { before: 0 }), body("Dla osób, które chcą mieszkać w otoczeniu natury, nie rezygnując z wygody i bliskości miasta. Sprawdzi się też jako second home na Kaszubach.", { size: 20, after: 0 })], WC),
  ] })], [WC, GAP, WC]),
  spacer(360),
  table([new TableRow({ children: [
    cell([eyebrow("Cena", { color: "B9C9B4", after: 80 }), p([t("1 400 000 zł ", { serif: true, size: 50, bold: true, color: PAPER }), t("brutto", { serif: true, size: 24, italics: true, color: PAPER })], { after: 120 }), p(t("Zakup bez prowizji po stronie Kupującego. Możliwość zakupu w systemie płatności ratalnej, bez konieczności kredytu bankowego – szczegóły podczas indywidualnego kontaktu.", { size: 19, color: "DFE6DA" }), { line: 270 })], WB, { fill: GREEN, pad: 320, padX: 360 }),
    cell([p(t(""))], 300),
    cell([eyebrow("Opiekun oferty", { after: 60 }), p(t("Adrianna Lidzbarska", { serif: true, size: 34, bold: true }), { after: 40 }), small("Lidzbarska Nieruchomości", { size: 18, after: 160 }), p(t("+48 727 926 639", { size: 24, bold: true }), { after: 60 }), p(t("adrianna@lidzbarska.pl", { size: 21 }), { after: 40 }), p(t("lidzbarska.pl", { size: 21 }))], WB, { pad: 320, padX: 360, borders: { top: line(GREEN, 6), bottom: line(GREEN, 6), left: line(GREEN, 6), right: line(GREEN, 6) } }),
  ] })], [WB, 300, WB]),
  h3("Indywidualna prezentacja", { before: 300 }),
  body("Zakup domu to jedna z najważniejszych decyzji, dlatego warto zobaczyć tę nieruchomość osobiście. Z przyjemnością oprowadzę Państwa po domu, przedstawię jego układ i zastosowane rozwiązania techniczne oraz odpowiem na wszystkie pytania. Zapraszam do kontaktu i umówienia terminu spotkania.", { after: 200 }),
  small("Przedstawiona oferta ma charakter poglądowy i może zawierać uproszczenia lub błędy. Niniejsze ogłoszenie nie stanowi oferty w rozumieniu art. 66 § 1 Kodeksu cywilnego. Współpracujemy z innymi biurami nieruchomości.", { size: 15 }),
];

const header = new Header({ children: [new Paragraph({
  children: [t("Lidzbarska ", { serif: true, size: 26, bold: true, color: GREEN }), t("Nieruchomości", { serif: true, size: 26, italics: true, color: GREEN }),
    new TextRun({ text: "\t", font: SANS, size: 16 }), t("Oferta nr D/0001 · Sprzedaż · Dom", { size: 15, color: MUTED, spacing: 20, caps: true })],
  tabStops: [{ type: TabStopType.RIGHT, position: CONTENT }], spacing: { after: 160 }, border: { bottom: line(GREEN, 6, ) },
})] });
const footer = new Footer({ children: [new Paragraph({
  children: [t("Adrianna Lidzbarska  ·  +48 727 926 639  ·  adrianna@lidzbarska.pl  ·  lidzbarska.pl", { size: 16, color: MUTED }),
    new TextRun({ text: "\t", font: SANS, size: 16 }),
    new TextRun({ children: [PageNumber.CURRENT], font: SANS, size: 16, color: MUTED }), t(" / ", { size: 16, color: MUTED }), new TextRun({ children: [PageNumber.TOTAL_PAGES], font: SANS, size: 16, color: MUTED })],
  tabStops: [{ type: TabStopType.RIGHT, position: CONTENT }], spacing: { before: 160 }, border: { top: line(LINE, 6) },
})] });

const doc = new Document({
  creator: "Lidzbarska Nieruchomości", title: "Dom Sycowa Huta – oferta D/0001",
  styles: { default: { document: { run: { font: SANS, size: 22, color: INK } } } },
  numbering: { config: [{ reference: "bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "✓", alignment: AlignmentType.LEFT, style: { run: { font: "Segoe UI Symbol", color: GREEN, bold: true }, paragraph: { indent: { left: 360, hanging: 360 } } } }] }] },
  sections: [{
    properties: { page: { size: { width: PAGE_W, height: 16838 }, margin: { top: 1500, right: MARGIN, bottom: 1300, left: MARGIN, header: 700, footer: 600 } } },
    headers: { default: header }, footers: { default: footer },
    children: [...page1, ...page2, ...page3, ...page4],
  }],
});

Packer.toBuffer(doc).then((buf) => { const out = path.join(__dirname, "Dom-Sycowa-Huta-oferta-D0001.docx"); fs.writeFileSync(out, buf); console.log("wrote", out, buf.length, "bytes"); });
