# Generator wersji testowej sklepu SMK (strony statyczne o strukturze jak w WooCommerce).
# python -X utf8 _build/build.py
import os, json, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROK = 2026

FIRMA = {
    'nazwa': 'SMK sp. z o.o.',
    'ulica': 'ul. Przyczółkowa 400',
    'kod': '02-962',
    'miasto': 'Warszawa',
    'email': 'smkbiuro@op.pl',
    'tel': '+48 509 922 772',
    'tel_href': '+48509922772',
    'krs': '0001253174',
    'nip': '951-265-21-76',
    'regon': '545247365',
}

KATEGORIE = [
    ('opakowania', 'Opakowania z tworzyw'),
    ('plyty-rury', 'Płyty, rury i kształtowniki'),
    ('budownictwo', 'Wyroby dla budownictwa'),
    ('wyroby', 'Pozostałe wyroby z tworzyw'),
    ('surowce', 'Hurt surowców i chemii'),
]
KAT = dict(KATEGORIE)

# Oferty na start - do podmiany na oferty przekazane przez SMK (nazwy, opisy, zdjęcia, ceny).
PRODUKTY = [
    dict(slug='pojemniki-z-pokrywka', kat='opakowania', nazwa='Pojemniki z tworzywa z pokrywką',
         krotko='Pojemniki z tworzywa sztucznego z pokrywą do przechowywania, transportu i sprzedaży produktów.',
         opis=['Pojemniki zamykane pokrywą, do pakowania produktów spożywczych, chemii, części i drobnych wyrobów.',
               'Pojemność, kolor pojemnika i pokrywy oraz ilość podają Państwo w uwagach do pozycji albo w zapytaniu. Przy większych i powtarzalnych zamówieniach przygotujemy wycenę serii.'],
         zdj=[('opakowania-1.webp', 'Pojemniki z tworzywa z czerwonymi pokrywkami', 1100, 1100)]),
    dict(slug='beczki-z-tworzywa', kat='opakowania', nazwa='Beczki z tworzywa sztucznego',
         krotko='Beczki z pokrywą do przechowywania i transportu płynów, sypkich surowców i odpadów.',
         opis=['Beczki z tworzywa sztucznego z pokrywą, do magazynowania i przewozu płynów oraz materiałów sypkich.',
               'Pojemność, rodzaj zamknięcia i ilość prosimy wpisać w uwagach do pozycji. Beczki można zamówić razem z dowozem na wskazany adres.'],
         zdj=[('opakowania-2.webp', 'Beczki z tworzywa sztucznego z pokrywami', 1100, 734),
              ('hurt-1.webp', 'Niebieskie beczki na paletach przed magazynem', 800, 929)]),
    dict(slug='rury-z-tworzyw', kat='plyty-rury', nazwa='Rury i kształtowniki z tworzyw',
         krotko='Rury, profile i arkusze z tworzyw sztucznych do instalacji, zabudowy i dalszej obróbki.',
         opis=['Rury z tworzyw sztucznych do instalacji, osłon i zastosowań technicznych oraz kształtowniki (profile), płyty i arkusze do dalszej obróbki i montażu.',
               'Średnicę lub przekrój, grubość ścianki, długość odcinków i ilość podają Państwo w uwagach albo w zapytaniu z rysunkiem.'],
         zdj=[('rury.webp', 'Szare rury z tworzywa ułożone w stos', 1100, 734)]),
    dict(slug='elementy-dla-budownictwa', kat='budownictwo', nazwa='Elementy z tworzyw dla budownictwa',
         krotko='Elementy z tworzyw sztucznych do instalacji i prac budowlanych.',
         opis=['Wyroby z tworzyw sztucznych stosowane w budownictwie: elementy instalacji, osłony, łączniki i akcesoria montażowe.',
               'Rodzaj elementu, wymiary i ilość prosimy opisać w uwagach do pozycji. Do zapytania ofertowego można dołączyć rysunek.'],
         zdj=[('budownictwo.webp', 'Montaż elementu z tworzywa na budowie', 800, 1422)]),
    dict(slug='palety-z-tworzywa', kat='wyroby', nazwa='Palety z tworzywa sztucznego',
         krotko='Palety z tworzywa do magazynu i transportu, odporne na wilgoć i łatwe w myciu.',
         opis=['Palety z tworzywa sztucznego do składowania i przewozu towarów, także tam, gdzie liczy się czystość i odporność na wilgoć.',
               'Wymiar palety, nośność i ilość prosimy podać w uwagach do pozycji.'],
         zdj=[('palety.webp', 'Stosy niebieskich palet z tworzywa przed magazynem', 800, 1200)]),
    dict(slug='skrzynki-z-tworzywa', kat='wyroby', nazwa='Skrzynki z tworzywa sztucznego',
         krotko='Ażurowe i pełne skrzynki z tworzywa do magazynu, transportu i ekspozycji.',
         opis=['Skrzynki z tworzywa sztucznego, ustawiane w stosy, do przechowywania i przewozu towarów.',
               'Wymiary, kolor, rodzaj ścianek (ażurowe lub pełne) i ilość prosimy wpisać w uwagach do pozycji.'],
         zdj=[('skrzynki.webp', 'Niebieskie skrzynki z tworzywa ustawione w stosy', 1100, 1004)]),
    dict(slug='granulat-tworzyw', kat='surowce', nazwa='Granulat tworzyw sztucznych',
         krotko='Surowce do przetwórstwa tworzyw w sprzedaży hurtowej, z dowozem.',
         opis=['Granulat tworzyw sztucznych i inne półprodukty do przetwórstwa, w sprzedaży hurtowej.',
               'Rodzaj tworzywa, ilość i termin dostawy prosimy podać w uwagach. Sprzedajemy także wyroby chemiczne w opakowaniach zbiorczych.'],
         zdj=[('hurt-2.webp', 'Granulat tworzywa sztucznego w dłoni', 800, 1425)]),
]

ZNAK = '<svg class="logo-znak" viewBox="0 0 40 40" aria-hidden="true"><rect width="40" height="40" rx="5"/><path d="M11 30V12h18v18"/></svg>'
KOSZ = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 4h3l2.2 10.5h10.3L21 7H7.1" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><rect x="8" y="17.5" width="3.5" height="3.5"/><rect x="15" y="17.5" width="3.5" height="3.5"/></svg>'
TEL_IKONA = '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M6.2 2.5 8.3 6.6 6.6 8.1c.9 2.2 2.9 4.2 5.3 5.3l1.5-1.7 4.1 2.1-.9 3.4C9.7 17.4 2.6 10.3 2.8 3.4z"/></svg>'

with open(os.path.join(ROOT, '_build', 'badge.part'), encoding='utf-8') as f:
    BADGE = f.read()

e = html.escape


def head(pre, tytul, opis, sciezka, extra='', preload=''):
    url = 'https://wylinka-podglad.pl/smk-koncept/' + sciezka
    return f'''<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="robots" content="noindex, nofollow" data-podglad>
<title>{e(tytul)}</title>
<meta name="description" content="{e(opis)}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#0B57D0">
<meta property="og:type" content="website">
<meta property="og:locale" content="pl_PL">
<meta property="og:title" content="{e(tytul)}">
<meta property="og:description" content="{e(opis)}">
<meta property="og:image" content="https://wylinka-podglad.pl/smk-koncept/img/hero-1600.webp">
<link rel="icon" href="{pre}favicon.svg" type="image/svg+xml">
<link rel="icon" href="{pre}img/logo-96.png" sizes="96x96" type="image/png">
<link rel="apple-touch-icon" href="{pre}img/apple-touch-icon.png">
<link rel="preload" href="{pre}fonts/archivo-latin.woff2" as="font" type="font/woff2" crossorigin>
{preload}<link rel="stylesheet" href="{pre}style.css">
{extra}</head>
'''


MENU = [('sklep/', 'Sklep'), ('o-firmie/', 'O firmie'), ('kontakt/', 'Kontakt')]


def naglowek(pre, aktywny):
    linki = ''.join(
        f'<a href="{pre}{h}"{" aria-current=\"page\"" if h == aktywny else ""}>{t}</a>' for h, t in MENU)
    kosz_akt = ' aria-current="page"' if aktywny == 'koszyk/' else ''
    return f'''<body data-pre="{pre}">
<a class="pomin" href="#tresc">Przejdź do treści</a>
<header class="naglowek">
  <div class="wrap nag-in">
    <a href="{pre}" class="logo" aria-label="{FIRMA['nazwa']} - strona główna">{ZNAK}<span class="logo-txt"><b>SMK</b><small>tworzywa sztuczne</small></span></a>
    <nav class="menu" id="menu" aria-label="Menu główne">
      {linki}
      <a href="{pre}kontakt/#zapytanie" class="menu-cta">Zapytaj o wycenę</a>
    </nav>
    <a href="tel:{FIRMA['tel_href']}" class="nag-tel">{TEL_IKONA}<span>{FIRMA['tel']}</span></a>
    <a href="{pre}koszyk/" class="nag-kosz"{kosz_akt} aria-label="Koszyk">{KOSZ}<span class="kosz-txt">Koszyk</span><b class="kosz-licz" data-licznik hidden>0</b></a>
    <button class="burger" id="burger" type="button" aria-expanded="false" aria-controls="menu" aria-label="Otwórz menu"><span></span><span></span></button>
  </div>
</header>
<main id="tresc">
'''


def stopka(pre):
    kat = ''.join(f'<li><a href="{pre}sklep/?kategoria={k}">{t}</a></li>' for k, t in KATEGORIE)
    return f'''</main>
{BADGE.split('</style>')[0]}</style>
<footer class="stopka">
  <div class="wrap stopka-in">
    <div class="st-kol st-firma">
      <a href="{pre}" class="logo logo-st" aria-label="{FIRMA['nazwa']}">{ZNAK}<span class="logo-txt"><b>SMK</b><small>tworzywa sztuczne</small></span></a>
      <p>{FIRMA['nazwa']}<br>{FIRMA['ulica']}<br>{FIRMA['kod']} {FIRMA['miasto']}</p>
      <p>KRS {FIRMA['krs']}<br>NIP {FIRMA['nip']}</p>
    </div>
    <div class="st-kol">
      <h2 class="st-h">Sklep</h2>
      <ul>{kat}</ul>
    </div>
    <div class="st-kol">
      <h2 class="st-h">Informacje</h2>
      <ul>
        <li><a href="{pre}o-firmie/">O firmie</a></li>
        <li><a href="{pre}dostawa-i-platnosci/">Dostawa i płatności</a></li>
        <li><a href="{pre}regulamin/">Regulamin sklepu</a></li>
        <li><a href="{pre}polityka-prywatnosci/">Polityka prywatności</a></li>
      </ul>
    </div>
    <div class="st-kol">
      <h2 class="st-h">Kontakt</h2>
      <p><a href="tel:{FIRMA['tel_href']}">{FIRMA['tel']}</a><br><a href="mailto:{FIRMA['email']}">{FIRMA['email']}</a></p>
      <p><a href="{pre}kontakt/#zapytanie">Zapytanie ofertowe</a></p>
    </div>
  </div>
  <div class="wrap stopka-dol">
    <span>&copy; {ROK} {FIRMA['nazwa']}</span>
    <span class="st-foto">Zdjęcia poglądowe: Pexels</span>
    {BADGE.split('</style>')[1].strip()}
  </div>
</footer>
<div class="toast" id="toast" role="status" aria-live="polite" hidden></div>
<script src="{pre}app.js" defer></script>
</body>
</html>
'''


def wytlok(jasny=False):
    return f'<span class="wytlok{" jasny" if jasny else ""}" aria-hidden="true"></span>'


def okruszki(pre, pozycje):
    li = []
    for i, (h, t) in enumerate(pozycje):
        if h is None:
            li.append(f'<li aria-current="page">{e(t)}</li>')
        else:
            li.append(f'<li><a href="{pre}{h}">{e(t)}</a></li>')
    items = []
    for i, (h, t) in enumerate(pozycje):
        it = {'@type': 'ListItem', 'position': i + 1, 'name': t}
        if h is not None:
            it['item'] = 'https://wylinka-podglad.pl/smk-koncept/' + h
        items.append(it)
    ld = json.dumps({'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': items}, ensure_ascii=False)
    return f'<nav class="okruszki" aria-label="Ścieżka"><ol>{"".join(li)}</ol></nav>\n<script type="application/ld+json">{ld}</script>\n'


def karta_produktu(pre, p, h='h3'):
    z = p['zdj'][0]
    return f'''<article class="produkt" data-kat="{p['kat']}">
  <a href="{pre}produkt/{p['slug']}/" class="produkt-foto"><img src="{pre}img/{z[0]}" alt="{e(z[1])}" width="{z[2]}" height="{z[3]}" loading="lazy"></a>
  <div class="produkt-tresc">
    <span class="produkt-kat">{KAT[p['kat']]}</span>
    <{h}><a href="{pre}produkt/{p['slug']}/">{e(p['nazwa'])}</a></{h}>
    <p>{e(p['krotko'])}</p>
    <div class="produkt-dol">
      <span class="cena">Cena na zapytanie</span>
      <button type="button" class="btn btn-gl btn-mały" data-dodaj='{dane_js(pre, p)}'>Do koszyka</button>
    </div>
  </div>
</article>'''


def dane_js(pre, p):
    return e(json.dumps({'id': p['slug'], 'nazwa': p['nazwa'], 'img': 'img/' + p['zdj'][0][0], 'url': 'produkt/' + p['slug'] + '/'}, ensure_ascii=False), quote=True)


def zapisz(sciezka, tresc):
    pelna = os.path.join(ROOT, sciezka)
    os.makedirs(os.path.dirname(pelna), exist_ok=True)
    with open(pelna, 'w', encoding='utf-8', newline='\n') as f:
        f.write(tresc)


ORG_LD = json.dumps({
    '@context': 'https://schema.org', '@type': 'Organization', 'name': FIRMA['nazwa'],
    'url': 'https://wylinka-podglad.pl/smk-koncept/', 'logo': 'https://wylinka-podglad.pl/smk-koncept/img/logo-192.png',
    'email': FIRMA['email'], 'telephone': FIRMA['tel'], 'taxID': '9512652176',
    'address': {'@type': 'PostalAddress', 'streetAddress': 'Przyczółkowa 400', 'postalCode': FIRMA['kod'],
                'addressLocality': FIRMA['miasto'], 'addressCountry': 'PL'},
}, ensure_ascii=False)


# ---------- strona główna ----------
def strona_glowna():
    pre = ''
    kat_karty = []
    zdj_kat = {'opakowania': ('opakowania-1.webp', 'Pojemniki z tworzywa z pokrywkami', 1100, 1100),
               'plyty-rury': ('rury.webp', 'Rury z tworzywa ułożone w stos', 1100, 734),
               'budownictwo': ('budownictwo.webp', 'Montaż rury z tworzywa na budowie', 800, 1422),
               'wyroby': ('palety.webp', 'Palety z tworzywa przed magazynem', 800, 1200),
               'surowce': ('hurt-2.webp', 'Granulat tworzywa sztucznego w dłoni', 800, 1425)}
    for k, t in KATEGORIE:
        z = zdj_kat[k]
        n = sum(1 for p in PRODUKTY if p['kat'] == k)
        kat_karty.append(f'''<a class="kat" href="sklep/?kategoria={k}">
  <img src="img/{z[0]}" alt="{e(z[1])}" width="{z[2]}" height="{z[3]}" loading="lazy">
  <span class="kat-txt"><b>{t}</b><small>{n} {"oferta" if n == 1 else "oferty"}</small></span>
</a>''')
    kat_karty.append('''<a class="kat" href="o-firmie/#transport">
  <img src="img/transport-2.webp" alt="Samochód ciężarowy z naczepą przed magazynem" width="1100" height="825" loading="lazy">
  <span class="kat-txt"><b>Transport towarów</b><small>dowóz zamówień</small></span>
</a>''')
    polecane = ''.join(karta_produktu(pre, p) for p in PRODUKTY[:4])
    preload = '<link rel="preload" as="image" href="img/hero-tel.webp" media="(max-width: 760px)">\n<link rel="preload" as="image" imagesrcset="img/hero-1024.webp 1024w, img/hero-1600.webp 1600w, img/hero-2520.webp 2520w" imagesizes="100vw" media="(min-width: 761px)">\n'
    t = head(pre, 'Opakowania i wyroby z tworzyw sztucznych, Warszawa | SMK sp. z o.o.',
             'Sklep SMK z Warszawy: opakowania, płyty, rury i kształtowniki z tworzyw sztucznych, wyroby dla budownictwa, hurt surowców i transport. Zamówienia online.',
             '', f'<script type="application/ld+json">{ORG_LD}</script>\n', preload)
    t += naglowek(pre, '')
    t += f'''<section class="hero" aria-labelledby="h1">
  <picture class="hero-foto">
    <source media="(max-width: 760px)" srcset="img/hero-tel.webp" width="900" height="1429">
    <img src="img/hero-1600.webp" srcset="img/hero-1024.webp 1024w, img/hero-1600.webp 1600w, img/hero-2520.webp 2520w" sizes="100vw" alt="Niebieskie skrzynki z tworzywa sztucznego ustawione w stosy" width="2520" height="2200" fetchpriority="high">
  </picture>
  <div class="wrap hero-in">
    <h1 id="h1">Opakowania i wyroby z&nbsp;tworzyw sztucznych z&nbsp;Warszawy</h1>
    <p class="hero-lead">Opakowania, płyty, rury i kształtowniki, wyroby dla budownictwa i surowce w hurcie. Zamówienie składa się online, a towar dowozimy własnym transportem. Od produkcji po dowóz.</p>
    <div class="hero-akcje">
      <a href="sklep/" class="btn btn-gl hero-cta">Przejdź do sklepu</a>
      <a href="kontakt/#zapytanie" class="btn btn-jasny">Zapytaj o wycenę</a>
    </div>
  </div>
</section>

<section class="sekcja" aria-labelledby="h-kat">
  <div class="wrap">
    <div class="sek-glowa">
      <h2 id="h-kat">Czego Państwo szukają?</h2>
      {wytlok()}
      <p>Oferta SMK w sześciu grupach. Każdą pozycję można zamówić od razu albo zapytać o wycenę z wymiarami, ilością lub rysunkiem.</p>
    </div>
    <div class="kategorie">
      {''.join(kat_karty)}
    </div>
  </div>
</section>

<section class="sekcja szara" aria-labelledby="h-pol">
  <div class="wrap">
    <div class="sek-glowa sek-glowa-rzad">
      <div>
        <h2 id="h-pol">Oferty w sklepie</h2>
        {wytlok()}
      </div>
      <a href="sklep/" class="btn btn-obrys">Wszystkie oferty</a>
    </div>
    <div class="produkty">
      {polecane}
    </div>
  </div>
</section>

<section class="sekcja ciemna" aria-labelledby="h-jak">
  <div class="wrap jak-in">
    <div class="jak-tekst">
      <h2 id="h-jak">Jak zamówić</h2>
      {wytlok(True)}
      <ol class="kroki">
        <li><b>Wybór oferty.</b> Dodają Państwo produkty do koszyka i w uwagach wpisują wymiary, kolor albo ilość.</li>
        <li><b>Zamówienie z danymi do faktury.</b> Płatność online albo tradycyjnym przelewem, faktura z NIP firmy.</li>
        <li><b>Dostawa.</b> Dowozimy własnym transportem albo kurierem, można też odebrać towar osobiście.</li>
      </ol>
      <p class="jak-dop">Nietypowe wymiary i większe serie najlepiej opisać w zapytaniu ofertowym. Można dołączyć rysunek lub zdjęcie.</p>
      <a href="kontakt/#zapytanie" class="btn btn-gl">Wyślij zapytanie</a>
    </div>
    <figure class="jak-foto">
      <img src="img/transport-1.webp" alt="Wózek widłowy załadowuje palety do samochodu ciężarowego" width="800" height="1156" loading="lazy">
    </figure>
  </div>
</section>

<section class="sekcja" aria-labelledby="h-firma">
  <div class="wrap firma-in">
    <figure class="firma-foto">
      <img src="img/firma.webp" alt="Linia produkcyjna z butelkami z tworzywa w zakładzie" width="1600" height="1068" loading="lazy">
    </figure>
    <div class="firma-tekst">
      <h2 id="h-firma">SMK sp. z o.o.</h2>
      {wytlok()}
      <p>Warszawska spółka zajmująca się wyrobami z tworzyw sztucznych: od opakowań, przez płyty, rury i kształtowniki, po elementy dla budownictwa. Do produkcji dochodzi hurtowa sprzedaż surowców i wyrobów chemicznych oraz transport drogowy towarów.</p>
      <a href="o-firmie/" class="btn btn-obrys">Więcej o firmie</a>
    </div>
  </div>
</section>
'''
    t += stopka(pre)
    zapisz('index.html', t)


# ---------- sklep ----------
def sklep():
    pre = '../'
    filtry = '<a href="./" class="filtr" data-filtr="">Wszystkie</a>' + ''.join(
        f'<a href="?kategoria={k}" class="filtr" data-filtr="{k}">{t}</a>' for k, t in KATEGORIE)
    karty = ''.join(karta_produktu(pre, p, 'h2') for p in PRODUKTY)
    t = head(pre, 'Sklep: wyroby z tworzyw sztucznych | SMK sp. z o.o.',
             'Sklep SMK: pojemniki, beczki, rury, płyty, palety i skrzynki z tworzyw sztucznych oraz granulat w hurcie. Zamówienia z fakturą, dostawa własnym transportem.',
             'sklep/')
    t += naglowek(pre, 'sklep/')
    t += f'''<section class="pod-glowa">
  <div class="wrap">
    {okruszki(pre, [('', 'Strona główna'), (None, 'Sklep')])}
    <h1>Sklep</h1>
    {wytlok()}
    <p class="pod-lead">Wybierz ofertę, dodaj do koszyka i w uwagach wpisz wymiary albo ilość. Ceny nietypowych zamówień potwierdzamy przed realizacją.</p>
  </div>
</section>
<section class="sekcja sklep" aria-label="Oferty">
  <div class="wrap">
    <div class="filtry" role="navigation" aria-label="Kategorie">{filtry}</div>
    <p class="wynik" id="wynik" aria-live="polite">{len(PRODUKTY)} ofert</p>
    <div class="produkty produkty-sklep" id="produkty">
      {karty}
    </div>
  </div>
</section>
'''
    t += stopka(pre)
    zapisz('sklep/index.html', t)


# ---------- karta produktu ----------
def produkt(p):
    pre = '../../'
    zdj = ''.join(
        f'<img src="{pre}img/{z[0]}" alt="{e(z[1])}" width="{z[2]}" height="{z[3]}"{" fetchpriority=\"high\"" if i == 0 else " loading=\"lazy\""}>'
        for i, z in enumerate(p['zdj']))
    miniatury = ''
    if len(p['zdj']) > 1:
        miniatury = '<div class="miniatury">' + ''.join(
            f'<button type="button" data-do="{i}" aria-label="Zdjęcie {i + 1}"><img src="{pre}img/{z[0]}" alt="" width="{z[2]}" height="{z[3]}" loading="lazy"></button>'
            for i, z in enumerate(p['zdj'])) + '</div>'
    opis = ''.join(f'<p>{e(x)}</p>' for x in p['opis'])
    inne = [q for q in PRODUKTY if q['slug'] != p['slug']]
    inne = sorted(inne, key=lambda q: q['kat'] != p['kat'])[:3]
    ld = json.dumps({'@context': 'https://schema.org', '@type': 'Product', 'name': p['nazwa'],
                     'description': p['krotko'], 'category': KAT[p['kat']],
                     'image': ['https://wylinka-podglad.pl/smk-koncept/img/' + z[0] for z in p['zdj']],
                     'brand': {'@type': 'Brand', 'name': 'SMK'}}, ensure_ascii=False)
    t = head(pre, f"{p['nazwa']} | Sklep SMK sp. z o.o.", p['krotko'] + ' Zamówienie online z fakturą, dostawa.',
             f"produkt/{p['slug']}/")
    t += naglowek(pre, 'sklep/')
    t += f'''<section class="karta-prod">
  <div class="wrap">
    {okruszki(pre, [('', 'Strona główna'), ('sklep/', 'Sklep'), ('sklep/?kategoria=' + p['kat'], KAT[p['kat']]), (None, p['nazwa'])])}
    <div class="kp-in">
      <div class="kp-galeria" data-galeria>
        <div class="kp-tor">{zdj}</div>
        {miniatury}
      </div>
      <div class="kp-info">
        <span class="produkt-kat">{KAT[p['kat']]}</span>
        <h1>{e(p['nazwa'])}</h1>
        {wytlok()}
        <p class="kp-krotko">{e(p['krotko'])}</p>
        <p class="kp-cena"><span class="cena">Cena na zapytanie</span><small>Cenę potwierdzamy po złożeniu zamówienia, przed płatnością.</small></p>
        <form class="kp-kup" data-kup='{dane_js(pre, p)}'>
          <label class="kp-uwagi">Uwagi do pozycji (wymiary, kolor, pojemność)<input name="uwagi" maxlength="200" placeholder="np. 5 l, pokrywa czerwona"></label>
          <div class="kp-rzad">
            <div class="ilosc" role="group" aria-label="Ilość">
              <button type="button" data-ile="-1" aria-label="Mniej">&minus;</button>
              <input name="ilosc" type="number" min="1" value="1" inputmode="numeric" aria-label="Ilość">
              <button type="button" data-ile="1" aria-label="Więcej">+</button>
            </div>
            <button type="submit" class="btn btn-gl kp-dodaj">Dodaj do koszyka</button>
          </div>
        </form>
        <ul class="kp-fakty">
          <li><b>Płatność</b>online albo przelewem, faktura z NIP</li>
          <li><b>Dostawa</b>transport własny, kurier albo odbiór osobisty</li>
          <li><b>Seria lub nietypowy wymiar</b><a href="{pre}kontakt/?temat={p['slug']}#zapytanie">zapytanie z rysunkiem</a></li>
        </ul>
      </div>
    </div>
  </div>
</section>
<section class="sekcja szara kp-opis" aria-labelledby="h-opis">
  <div class="wrap kp-opis-in">
    <div>
      <h2 id="h-opis">Opis</h2>
      {wytlok()}
      {opis}
    </div>
  </div>
</section>
<section class="sekcja" aria-labelledby="h-inne">
  <div class="wrap">
    <div class="sek-glowa"><h2 id="h-inne">Zobacz też</h2>{wytlok()}</div>
    <div class="produkty produkty-3">{''.join(karta_produktu(pre, q) for q in inne)}</div>
  </div>
</section>
<script type="application/ld+json">{ld}</script>
'''
    t += stopka(pre)
    zapisz(f"produkt/{p['slug']}/index.html", t)


# ---------- o firmie ----------
def o_firmie():
    pre = '../'
    obszary = [
        ('Opakowania z tworzyw', 'Pojemniki, beczki i inne opakowania do przechowywania, transportu i sprzedaży.'),
        ('Płyty, rury i kształtowniki', 'Półprodukty z tworzyw do dalszej obróbki, zabudowy i montażu.'),
        ('Wyroby dla budownictwa', 'Elementy z tworzyw stosowane w instalacjach i pracach budowlanych.'),
        ('Pozostałe wyroby', 'Skrzynki, palety i wyroby z tworzyw na zamówienie.'),
        ('Hurt surowców i chemii', 'Granulat, półprodukty i wyroby chemiczne w sprzedaży hurtowej.'),
        ('Transport drogowy', 'Dowóz zamówionych wyrobów i surowców na wskazany adres.'),
    ]
    ob = ''.join(f'<li><span class="nr">{i + 1:02d}</span><div><h3>{a}</h3><p>{b}</p></div></li>' for i, (a, b) in enumerate(obszary))
    t = head(pre, 'O firmie | SMK sp. z o.o., tworzywa sztuczne Warszawa',
             'SMK sp. z o.o. z Warszawy: produkcja opakowań i wyrobów z tworzyw sztucznych, hurt surowców i transport towarów. Dane rejestrowe firmy.',
             'o-firmie/', f'<script type="application/ld+json">{ORG_LD}</script>\n')
    t += naglowek(pre, 'o-firmie/')
    t += f'''<section class="pod-glowa">
  <div class="wrap">
    {okruszki(pre, [('', 'Strona główna'), (None, 'O firmie')])}
    <h1>O firmie</h1>
    {wytlok()}
    <p class="pod-lead">SMK sp. z o.o. to warszawska spółka zajmująca się wyrobami z tworzyw sztucznych, od produkcji po dowóz towaru do klienta.</p>
  </div>
</section>
<figure class="pas-foto">
  <img src="{pre}img/firma-2400.webp" srcset="{pre}img/firma.webp 1600w, {pre}img/firma-2400.webp 2400w" sizes="100vw" alt="Linia produkcyjna z butelkami z tworzywa w zakładzie" width="2400" height="1602" fetchpriority="high">
</figure>
<section class="sekcja" aria-labelledby="h-zakres">
  <div class="wrap">
    <div class="sek-glowa">
      <h2 id="h-zakres">Zakres działalności</h2>
      {wytlok()}
      <p>Produkcja, sprzedaż hurtowa i transport w jednej firmie. Zamówienie, faktura i dostawa załatwiane w jednym miejscu.</p>
    </div>
    <ol class="obszary">{ob}</ol>
  </div>
</section>
<section class="sekcja ciemna" id="transport" aria-labelledby="h-trans">
  <div class="wrap jak-in">
    <div class="jak-tekst">
      <h2 id="h-trans">Transport towarów</h2>
      {wytlok(True)}
      <p class="jak-dop">Zamówione wyroby i surowce dowozimy na wskazany adres, bez szukania osobnego przewoźnika. Termin i koszt dostawy potwierdzamy przy zamówieniu.</p>
      <a href="{pre}kontakt/?temat=transport#zapytanie" class="btn btn-gl">Zapytaj o transport</a>
    </div>
    <figure class="jak-foto"><img src="{pre}img/transport-2.webp" alt="Samochód ciężarowy z naczepą przed magazynem" width="1100" height="825" loading="lazy"></figure>
  </div>
</section>
<section class="sekcja szara" aria-labelledby="h-dane">
  <div class="wrap">
    <div class="sek-glowa"><h2 id="h-dane">Dane firmy</h2>{wytlok()}</div>
    <dl class="dane">
      <div><dt>Nazwa</dt><dd>SMK spółka z ograniczoną odpowiedzialnością</dd></div>
      <div><dt>Siedziba</dt><dd>{FIRMA['ulica']}, {FIRMA['kod']} {FIRMA['miasto']}</dd></div>
      <div><dt>KRS</dt><dd>{FIRMA['krs']}</dd></div>
      <div><dt>NIP</dt><dd>{FIRMA['nip']}</dd></div>
      <div><dt>REGON</dt><dd>{FIRMA['regon']}</dd></div>
      <div><dt>E-mail</dt><dd><a href="mailto:{FIRMA['email']}">{FIRMA['email']}</a></dd></div>
    </dl>
  </div>
</section>
'''
    t += stopka(pre)
    zapisz('o-firmie/index.html', t)


# ---------- kontakt ----------
def kontakt():
    pre = '../'
    opcje = ''.join(f'<option value="{p["slug"]}">{e(p["nazwa"])}</option>' for p in PRODUKTY)
    t = head(pre, 'Kontakt i zapytanie ofertowe | SMK sp. z o.o., Warszawa',
             'Kontakt z SMK sp. z o.o.: telefon, e-mail, adres ul. Przyczółkowa 400 w Warszawie z mapą dojazdu. Zapytanie ofertowe z rysunkiem.',
             'kontakt/')
    t += naglowek(pre, 'kontakt/')
    t += f'''<section class="pod-glowa">
  <div class="wrap">
    {okruszki(pre, [('', 'Strona główna'), (None, 'Kontakt')])}
    <h1>Kontakt</h1>
    {wytlok()}
    <p class="pod-lead">Zapytanie ofertowe można wysłać formularzem, e-mailem albo zadzwonić.</p>
  </div>
</section>
<section class="sekcja kontakt">
  <div class="wrap kontakt-in">
    <div class="kontakt-dane">
      <ul class="kanaly">
        <li><span>Telefon</span><a href="tel:{FIRMA['tel_href']}">{FIRMA['tel']}</a></li>
        <li><span>E-mail</span><a href="mailto:{FIRMA['email']}">{FIRMA['email']}</a></li>
        <li><span>Adres</span><span class="adr">{FIRMA['nazwa']}<br>{FIRMA['ulica']}, {FIRMA['kod']} {FIRMA['miasto']}</span></li>
      </ul>
      <div class="mapa">
        <iframe title="Mapa dojazdu: ul. Przyczółkowa 400, Warszawa" src="https://maps.google.com/maps?q=Przycz%C3%B3%C5%82kowa%20400%2C%2002-962%20Warszawa&amp;z=14&amp;output=embed" referrerpolicy="no-referrer-when-downgrade"></iframe>
      </div>
      <p class="mapa-link"><a href="https://www.google.com/maps/dir/?api=1&amp;destination=Przycz%C3%B3%C5%82kowa+400%2C+02-962+Warszawa" rel="noopener" target="_blank">Wyznacz trasę w Mapach Google</a></p>
    </div>
    <form class="formularz" id="zapytanie" novalidate>
      <h2>Zapytanie ofertowe</h2>
      <label>Czego dotyczy zapytanie
        <select name="temat">
          <option value="">Wybierz albo opisz poniżej</option>
          {opcje}
          <option value="transport">Transport towarów</option>
          <option value="inne">Inny wyrób z tworzyw</option>
        </select>
      </label>
      <div class="pola2">
        <label>Imię i firma<input name="kto" autocomplete="organization" placeholder="np. Jan Nowak, Firma XYZ"></label>
        <label>Telefon lub e-mail<input name="kontakt" autocomplete="email" placeholder="do odpowiedzi" required></label>
      </div>
      <label>Opis: wyrób, wymiary, ilość, termin<textarea name="opis" rows="5" placeholder="np. pojemnik 5 l z pokrywką, 2 000 szt., dostawa w grudniu"></textarea></label>
      <label class="plik">Rysunek lub zdjęcie (opcjonalnie, do 10 MB)<input type="file" name="plik" accept=".pdf,.jpg,.jpeg,.png,.dwg,.dxf"></label>
      <label class="zgoda"><input type="checkbox" name="zgoda" required> <span>Zgadzam się na kontakt w sprawie zapytania. Szczegóły w <a href="{pre}polityka-prywatnosci/">polityce prywatności</a>.</span></label>
      <button type="submit" class="btn btn-gl">Wyślij zapytanie</button>
      <p class="form-info" id="formInfo" role="status" aria-live="polite"></p>
    </form>
  </div>
</section>
'''
    t += stopka(pre)
    zapisz('kontakt/index.html', t)


# ---------- koszyk ----------
def koszyk():
    pre = '../'
    t = head(pre, 'Koszyk | Sklep SMK sp. z o.o.', 'Koszyk sklepu SMK sp. z o.o.', 'koszyk/')
    t += naglowek(pre, 'koszyk/')
    t += f'''<section class="pod-glowa pod-glowa-mala">
  <div class="wrap">
    {okruszki(pre, [('', 'Strona główna'), ('sklep/', 'Sklep'), (None, 'Koszyk')])}
    <h1>Koszyk</h1>
    {wytlok()}
  </div>
</section>
<section class="sekcja koszyk-sek">
  <div class="wrap koszyk-in" id="koszyk">
    <div class="koszyk-lista" id="koszykLista"></div>
    <aside class="podsum" id="podsum" hidden>
      <h2>Podsumowanie</h2>
      <dl>
        <div><dt>Pozycje</dt><dd id="sumPoz">0</dd></div>
        <div><dt>Sztuki razem</dt><dd id="sumSzt">0</dd></div>
        <div><dt>Wartość</dt><dd>potwierdzimy przed płatnością</dd></div>
      </dl>
      <a href="{pre}zamowienie/" class="btn btn-gl">Przejdź do zamówienia</a>
      <a href="{pre}sklep/" class="btn btn-obrys">Kontynuuj zakupy</a>
    </aside>
    <div class="pusty" id="pusty" hidden>
      <p>Koszyk jest pusty.</p>
      <a href="{pre}sklep/" class="btn btn-gl">Przejdź do sklepu</a>
    </div>
  </div>
</section>
'''
    t += stopka(pre)
    zapisz('koszyk/index.html', t)


# ---------- zamówienie ----------
def zamowienie():
    pre = '../'
    t = head(pre, 'Zamówienie | Sklep SMK sp. z o.o.', 'Składanie zamówienia w sklepie SMK sp. z o.o.', 'zamowienie/')
    t += naglowek(pre, 'koszyk/')
    t += f'''<section class="pod-glowa pod-glowa-mala">
  <div class="wrap">
    {okruszki(pre, [('', 'Strona główna'), ('koszyk/', 'Koszyk'), (None, 'Zamówienie')])}
    <h1>Zamówienie</h1>
    {wytlok()}
  </div>
</section>
<section class="sekcja zam-sek">
  <form class="wrap zam-in" id="zamowienie" novalidate>
    <div class="zam-pola">
      <fieldset>
        <legend>Dane do faktury</legend>
        <div class="pola2">
          <label>Nazwa firmy<input name="firma" autocomplete="organization" required></label>
          <label>NIP<input name="nip" inputmode="numeric" placeholder="np. 123-456-78-90"></label>
        </div>
        <label>Ulica i numer<input name="ulica" autocomplete="street-address" required></label>
        <div class="pola2">
          <label>Kod pocztowy<input name="kod" autocomplete="postal-code" required></label>
          <label>Miejscowość<input name="miasto" autocomplete="address-level2" required></label>
        </div>
        <div class="pola2">
          <label>Imię i nazwisko<input name="osoba" autocomplete="name" required></label>
          <label>Telefon<input name="tel" type="tel" autocomplete="tel" required></label>
        </div>
        <label>E-mail (potwierdzenie zamówienia)<input name="email" type="email" autocomplete="email" required></label>
      </fieldset>
      <fieldset>
        <legend>Dostawa</legend>
        <label class="opcja"><input type="radio" name="dostawa" value="transport" checked><span><b>Transport SMK</b>dowóz na wskazany adres, koszt potwierdzamy przy zamówieniu</span></label>
        <label class="opcja"><input type="radio" name="dostawa" value="kurier"><span><b>Kurier</b>przesyłki paczkowe i paletowe</span></label>
        <label class="opcja"><input type="radio" name="dostawa" value="odbior"><span><b>Odbiór osobisty</b>{FIRMA['ulica']}, {FIRMA['miasto']}</span></label>
        <label>Adres dostawy, jeśli inny niż do faktury<textarea name="adres_dostawy" rows="2"></textarea></label>
      </fieldset>
      <fieldset>
        <legend>Płatność</legend>
        <label class="opcja"><input type="radio" name="platnosc" value="online" checked><span><b>Płatność online Przelewy24</b>BLIK, karta albo szybki przelew</span></label>
        <label class="opcja"><input type="radio" name="platnosc" value="przelew"><span><b>Przelew tradycyjny</b>dane do przelewu w potwierdzeniu zamówienia</span></label>
      </fieldset>
      <label>Uwagi do zamówienia<textarea name="uwagi" rows="3"></textarea></label>
    </div>
    <aside class="podsum zam-podsum">
      <h2>Twoje zamówienie</h2>
      <ul class="zam-lista" id="zamLista"></ul>
      <dl><div><dt>Wartość</dt><dd>potwierdzimy przed płatnością</dd></div></dl>
      <label class="zgoda"><input type="checkbox" name="regulamin" required> <span>Akceptuję <a href="{pre}regulamin/">regulamin sklepu</a> i <a href="{pre}polityka-prywatnosci/">politykę prywatności</a>.</span></label>
      <button type="submit" class="btn btn-gl">Zamawiam</button>
      <p class="form-info" id="zamInfo" role="status" aria-live="polite"></p>
    </aside>
  </form>
</section>
'''
    t += stopka(pre)
    zapisz('zamowienie/index.html', t)


def tekstowa(slug, tytul, opis, tresc):
    pre = '../'
    t = head(pre, f'{tytul} | SMK sp. z o.o.', opis, slug + '/')
    t += naglowek(pre, '')
    t += f'''<section class="pod-glowa pod-glowa-mala">
  <div class="wrap">
    {okruszki(pre, [('', 'Strona główna'), (None, tytul)])}
    <h1>{tytul}</h1>
    {wytlok()}
  </div>
</section>
<section class="sekcja tekst-sek"><div class="wrap tekst">{tresc}</div></section>
'''
    t += stopka(pre)
    zapisz(slug + '/index.html', t)


def tekstowe():
    tekstowa('dostawa-i-platnosci', 'Dostawa i płatności',
             'Sposoby dostawy i płatności w sklepie SMK sp. z o.o.: transport własny, kurier, odbiór osobisty, płatność online lub przelewem.',
             f'''<h2>Dostawa</h2>
<p>Zamówione wyroby dowozimy własnym transportem na wskazany adres. Mniejsze zamówienia możemy wysłać kurierem, a towar można też odebrać osobiście w siedzibie firmy: {FIRMA['ulica']}, {FIRMA['kod']} {FIRMA['miasto']}.</p>
<p>Koszt i termin dostawy zależą od wielkości zamówienia i miejsca dostawy. Potwierdzamy je po złożeniu zamówienia, przed płatnością.</p>
<h2>Płatność</h2>
<p>Za zamówienie można zapłacić online przez Przelewy24 (BLIK, karta płatnicza, szybki przelew) albo tradycyjnym przelewem na rachunek podany w potwierdzeniu zamówienia.</p>
<h2>Faktura</h2>
<p>Do każdego zamówienia wystawiamy fakturę na dane podane w zamówieniu, w tym NIP firmy.</p>''')
    tekstowa('regulamin', 'Regulamin sklepu', 'Regulamin sklepu internetowego SMK sp. z o.o.',
             f'''<p>Regulamin określa zasady składania zamówień w sklepie internetowym prowadzonym przez {FIRMA['nazwa']}, {FIRMA['ulica']}, {FIRMA['kod']} {FIRMA['miasto']}, KRS {FIRMA['krs']}, NIP {FIRMA['nip']}, e-mail {FIRMA['email']}.</p>
<p>Pełna treść regulaminu zostanie opublikowana w tym miejscu przed uruchomieniem sklepu.</p>''')
    tekstowa('polityka-prywatnosci', 'Polityka prywatności', 'Polityka prywatności sklepu SMK sp. z o.o.',
             f'''<h2>Administrator danych</h2>
<p>{FIRMA['nazwa']}, {FIRMA['ulica']}, {FIRMA['kod']} {FIRMA['miasto']}, KRS {FIRMA['krs']}, NIP 9512652176, e-mail {FIRMA['email']}. Dane przetwarzamy zgodnie z RODO (rozporządzenie UE 2016/679).</p>
<h2>Zamówienia</h2>
<p>Dane podane w zamówieniu (firma, NIP, adres, osoba kontaktowa, telefon, e-mail) wykorzystujemy do realizacji zamówienia, dostawy i wystawienia faktury (art. 6 ust. 1 lit. b i c RODO). Dane rozliczeniowe przechowujemy przez okres wymagany przepisami podatkowymi.</p>
<h2>Płatności i dostawa</h2>
<p>Przy płatności online dane potrzebne do zapłaty przekazujemy operatorowi płatności PayPro S.A. z siedzibą w Poznaniu (serwis Przelewy24), a przy wysyłce kurierem dane adresowe firmie kurierskiej, wyłącznie w zakresie potrzebnym do realizacji zamówienia.</p>
<h2>Formularz zapytania</h2>
<p>Dane z formularza (imię, firma, telefon lub e-mail, opis i załączony plik) wykorzystujemy do przygotowania oferty i kontaktu w jej sprawie (art. 6 ust. 1 lit. b RODO).</p>
<h2>Prawa</h2>
<p>Przysługuje Państwu prawo dostępu do danych, ich sprostowania, usunięcia, ograniczenia przetwarzania, przenoszenia, sprzeciwu oraz skargi do Prezesa UODO.</p>
<h2>Pliki cookies</h2>
<p>Sklep używa plików cookies niezbędnych do działania koszyka. Osadzona mapa Google może zapisywać własne pliki cookies zgodnie z polityką Google. Zgodę na cookies inne niż niezbędne można wycofać w każdej chwili.</p>''')


def strona_404():
    pre = '/smk-koncept/'
    t = head(pre, 'Nie znaleziono strony | SMK sp. z o.o.', 'Nie znaleziono strony.', '404.html')
    t += naglowek(pre, '')
    t += f'''<section class="pod-glowa"><div class="wrap">
<h1>Nie znaleziono strony</h1>{wytlok()}
<p class="pod-lead">Adres mógł się zmienić. Zapraszamy do sklepu albo na stronę główną.</p>
<p><a href="{pre}sklep/" class="btn btn-gl">Przejdź do sklepu</a></p>
</div></section>
'''
    t += stopka(pre)
    zapisz('404.html', t)


strona_glowna()
sklep()
for p in PRODUKTY:
    produkt(p)
o_firmie()
kontakt()
koszyk()
zamowienie()
tekstowe()
strona_404()

# mapa strony
adresy = ['', 'sklep/', 'o-firmie/', 'kontakt/', 'dostawa-i-platnosci/', 'regulamin/', 'polityka-prywatnosci/'] + [f"produkt/{p['slug']}/" for p in PRODUKTY]
zapisz('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
       ''.join(f'  <url><loc>https://wylinka-podglad.pl/smk-koncept/{a}</loc></url>\n' for a in adresy) + '</urlset>\n')
print('OK', len(adresy) + 3, 'stron')
