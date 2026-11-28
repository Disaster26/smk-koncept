(function () {
  'use strict';
  var d = document, pre = d.body.getAttribute('data-pre') || '';
  var KLUCZ = 'smk-koszyk';

  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }

  /* menu mobilne */
  var burger = d.getElementById('burger'), menu = d.getElementById('menu');
  function zamknij() { menu.classList.remove('otwarte'); burger.setAttribute('aria-expanded', 'false'); burger.setAttribute('aria-label', 'Otwórz menu'); }
  burger.addEventListener('click', function () {
    var o = menu.classList.toggle('otwarte');
    burger.setAttribute('aria-expanded', o ? 'true' : 'false');
    burger.setAttribute('aria-label', o ? 'Zamknij menu' : 'Otwórz menu');
  });
  d.addEventListener('keydown', function (e) { if (e.key === 'Escape') zamknij(); });
  d.addEventListener('click', function (e) { if (menu.classList.contains('otwarte') && !e.target.closest('#menu,#burger')) zamknij(); });

  /* koszyk w pamięci przeglądarki */
  function wczytaj() { try { return JSON.parse(localStorage.getItem(KLUCZ)) || []; } catch (e) { return []; } }
  function zapisz(k) { try { localStorage.setItem(KLUCZ, JSON.stringify(k)); } catch (e) {} licznik(); }
  function licznik() {
    var n = wczytaj().reduce(function (s, p) { return s + p.ilosc; }, 0);
    d.querySelectorAll('[data-licznik]').forEach(function (b) { b.textContent = n; b.hidden = n === 0; });
  }
  function dodaj(p, ilosc, uwagi) {
    var k = wczytaj(), klucz = p.id + '|' + (uwagi || ''), jest = null;
    k.forEach(function (x) { if (x.klucz === klucz) jest = x; });
    if (jest) jest.ilosc += ilosc;
    else k.push({ klucz: klucz, id: p.id, nazwa: p.nazwa, img: p.img, url: p.url, ilosc: ilosc, uwagi: uwagi || '', cena: p.cena || 0, jedn: p.jedn || '' });
    zapisz(k);
    toast(p.nazwa);
  }
  var tid;
  function toast(nazwa) {
    var t = d.getElementById('toast');
    t.innerHTML = '<span>Dodano do koszyka: <b>' + esc(nazwa) + '</b></span><a href="' + pre + 'koszyk/">Zobacz koszyk</a>';
    t.hidden = false;
    clearTimeout(tid); tid = setTimeout(function () { t.hidden = true; }, 4500);
  }
  licznik();

  d.addEventListener('click', function (e) {
    var b = e.target.closest('[data-dodaj]');
    if (!b) return;
    dodaj(JSON.parse(b.getAttribute('data-dodaj')), 1, '');
  });

  /* karta produktu: ilość i dodanie */
  var kup = d.querySelector('[data-kup]');
  if (kup) {
    var pole = kup.querySelector('[name=ilosc]');
    kup.addEventListener('click', function (e) {
      var b = e.target.closest('[data-ile]'); if (!b) return;
      pole.value = Math.max(1, (parseInt(pole.value, 10) || 1) + parseInt(b.getAttribute('data-ile'), 10));
    });
    kup.addEventListener('submit', function (e) {
      e.preventDefault();
      var n = Math.max(1, parseInt(pole.value, 10) || 1);
      dodaj(JSON.parse(kup.getAttribute('data-kup')), n, kup.querySelector('[name=uwagi]').value.trim());
    });
  }

  /* galeria: przesuwanie palcem i myszą, miniatury */
  d.querySelectorAll('[data-galeria]').forEach(function (g) {
    var tor = g.querySelector('.kp-tor'), min = [].slice.call(g.querySelectorAll('.miniatury button'));
    function aktywna() {
      var i = Math.round(tor.scrollLeft / tor.clientWidth);
      min.forEach(function (b, j) { if (i === j) b.setAttribute('aria-current', 'true'); else b.removeAttribute('aria-current'); });
    }
    min.forEach(function (b) {
      b.addEventListener('click', function () { tor.scrollTo({ left: tor.clientWidth * parseInt(b.getAttribute('data-do'), 10), behavior: 'smooth' }); });
    });
    tor.addEventListener('scroll', aktywna, { passive: true });
    aktywna();
    var x0 = 0, s0 = 0, ruch = false, wc = false;
    tor.addEventListener('pointerdown', function (e) { if (e.pointerType !== 'mouse' || e.button !== 0) return; wc = true; ruch = false; x0 = e.clientX; s0 = tor.scrollLeft; });
    window.addEventListener('pointermove', function (e) {
      if (!wc) return; var dx = e.clientX - x0;
      if (!ruch && Math.abs(dx) > 4) { ruch = true; tor.classList.add('ciagnie'); }
      if (ruch) { tor.scrollLeft = s0 - dx; e.preventDefault(); }
    });
    window.addEventListener('pointerup', function () {
      if (!wc) return; wc = false;
      if (ruch) { tor.classList.remove('ciagnie'); tor.scrollTo({ left: Math.round(tor.scrollLeft / tor.clientWidth) * tor.clientWidth, behavior: 'smooth' }); }
    });
  });

  var q = new URLSearchParams(location.search);

  /* sklep: filtr kategorii */
  var lista = d.getElementById('produkty');
  if (lista) {
    var kat = q.get('kategoria') || '', n = 0;
    lista.querySelectorAll('.produkt').forEach(function (p) {
      var w = !kat || p.getAttribute('data-kat') === kat; p.hidden = !w; if (w) n++;
    });
    d.querySelectorAll('[data-filtr]').forEach(function (a) {
      if (a.getAttribute('data-filtr') === kat) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current');
    });
    var akt = d.querySelector('.filtr[aria-current]');
    if (akt && akt.scrollIntoView && kat) akt.scrollIntoView({ block: 'nearest', inline: 'center' });
    d.getElementById('wynik').textContent = n + (n === 1 ? ' oferta' : (n > 1 && n < 5 ? ' oferty' : ' ofert'));
  }

  function zl(x) { return x.toFixed(2).replace('.', ',').replace(/\B(?=(\d{3})+(?!\d))/g, ' ') + ' zł'; }
  function wartosc(k) { return k.reduce(function (s, p) { return s + (p.cena ? p.cena * p.ilosc : 0); }, 0); }
  /* wysyłka DPD: 20 zł brutto za każdy karton */
  var DPD = 20;
  function kartony(k) { return k.reduce(function (s, p) { return s + p.ilosc; }, 0); }
  /* strona koszyka */
  var kl = d.getElementById('koszykLista');
  function rysujKoszyk() {
    var k = wczytaj();
    d.getElementById('pusty').hidden = k.length > 0;
    d.getElementById('podsum').hidden = k.length === 0;
    kl.hidden = k.length === 0;
    kl.innerHTML = k.map(function (p, i) {
      return '<div class="pozycja"><a href="' + pre + esc(p.url) + '"><img src="' + pre + esc(p.img) + '" alt="" width="96" height="96"></a>' +
        '<div><h2><a href="' + pre + esc(p.url) + '">' + esc(p.nazwa) + '</a></h2>' +
        (p.uwagi ? '<p class="poz-uwagi">Uwagi: ' + esc(p.uwagi) + '</p>' : '') + '<p class="poz-uwagi">' + (p.cena ? zl(p.cena) + ' brutto / ' + esc(p.jedn || 'szt.') + ', razem <b>' + zl(p.cena * p.ilosc) + '</b>' : 'Cena na zapytanie') + '</p></div>' +
        '<div class="poz-akcje"><div class="ilosc" role="group" aria-label="Ilość"><button type="button" data-zm="-1" data-i="' + i + '" aria-label="Mniej">&minus;</button>' +
        '<input type="number" min="1" value="' + p.ilosc + '" data-i="' + i + '" aria-label="Ilość" inputmode="numeric"><button type="button" data-zm="1" data-i="' + i + '" aria-label="Więcej">+</button></div>' +
        '<button type="button" class="usun" data-usun="' + i + '">Usuń</button></div></div>';
    }).join('');
    d.getElementById('sumPoz').textContent = k.length;
    d.getElementById('sumSzt').textContent = k.reduce(function (s, p) { return s + p.ilosc; }, 0);
    var sw = d.getElementById('sumWart'); if (sw) sw.textContent = zl(wartosc(k));
    var sy = d.getElementById('sumWys'); if (sy) sy.textContent = zl(DPD * kartony(k));
    var sr = d.getElementById('sumRazem'); if (sr) sr.textContent = zl(wartosc(k) + DPD * kartony(k));
    var sz = d.getElementById('sumZap'); if (sz) sz.hidden = !k.some(function (p) { return !p.cena; });
  }
  if (kl) {
    rysujKoszyk();
    kl.addEventListener('click', function (e) {
      var k = wczytaj(), b = e.target.closest('[data-zm],[data-usun]'); if (!b) return;
      if (b.hasAttribute('data-usun')) k.splice(+b.getAttribute('data-usun'), 1);
      else { var p = k[+b.getAttribute('data-i')]; p.ilosc = Math.max(1, p.ilosc + parseInt(b.getAttribute('data-zm'), 10)); }
      zapisz(k); rysujKoszyk();
    });
    kl.addEventListener('change', function (e) {
      var k = wczytaj(), i = e.target.getAttribute('data-i'); if (i === null) return;
      k[+i].ilosc = Math.max(1, parseInt(e.target.value, 10) || 1); zapisz(k); rysujKoszyk();
    });
  }

  /* zamówienie */
  var zam = d.getElementById('zamowienie');
  if (zam) {
    var k = wczytaj(), zlista = d.getElementById('zamLista');
    zlista.innerHTML = k.length ? k.map(function (p) {
      return '<li><span>' + esc(p.nazwa) + (p.uwagi ? '<small>' + esc(p.uwagi) + '</small>' : '') + (p.cena ? '<small>' + zl(p.cena) + ' brutto / ' + esc(p.jedn || 'szt.') + '</small>' : '<small>cena na zapytanie</small>') + '</span><b>' + p.ilosc + ' ' + (p.jedn === 'karton' ? 'kart.' : 'szt.') + '</b></li>';
    }).join('') : '<li><span>Koszyk jest pusty. <a href="' + pre + 'sklep/">Przejdź do sklepu</a></span></li>';
    var doWyc = k.some(function (p) { return !p.cena; }) ? ' + pozycje do wyceny' : '';
    var zw = d.getElementById('zamWart'); if (zw) zw.textContent = zl(wartosc(k)) + doWyc;
    function przelicz() {
      var dost = (zam.querySelector('[name=dostawa]:checked') || {}).value, wys = 0, opis = 'Wysyłka kurierem DPD', txt;
      if (dost === 'dpd') { wys = DPD * kartony(k); txt = zl(wys); opis += ' (' + kartony(k) + ' x 20 zł)'; }
      else if (dost === 'transport') { opis = 'Transport SMK'; txt = 'do potwierdzenia'; }
      else { opis = 'Odbiór osobisty'; txt = '0,00 zł'; }
      d.getElementById('zamWysOpis').textContent = opis;
      d.getElementById('zamWys').textContent = txt;
      d.getElementById('zamRazem').textContent = zl(wartosc(k) + wys) + (dost === 'transport' ? ' + transport' : '') + doWyc;
    }
    if (d.getElementById('zamWys')) { przelicz(); zam.addEventListener('change', function (e) { if (e.target.name === 'dostawa') przelicz(); }); }
    zam.addEventListener('submit', function (e) {
      e.preventDefault();
      var info = d.getElementById('zamInfo'), brak = null;
      zam.querySelectorAll('[required]').forEach(function (p) { if (!brak && (p.type === 'checkbox' ? !p.checked : !p.value.trim())) brak = p; });
      if (!wczytaj().length) { info.textContent = 'Koszyk jest pusty.'; return; }
      if (brak) { info.textContent = brak.type === 'checkbox' ? 'Proszę zaakceptować regulamin.' : 'Proszę uzupełnić zaznaczone pola.'; brak.focus(); return; }
      info.textContent = 'Wersja testowa sklepu: zamówienie nie zostało wysłane. W gotowym sklepie trafi do SMK, a na podany e-mail przyjdzie potwierdzenie.';
    });
  }

  /* formularz zapytania */
  var form = d.getElementById('zapytanie');
  if (form && form.tagName === 'FORM') {
    var sel = form.querySelector('[name=temat]'), t = q.get('temat');
    if (t && sel.querySelector('option[value="' + t.replace(/[^a-z0-9-]/g, '') + '"]')) sel.value = t;
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var info = d.getElementById('formInfo'), kon = form.querySelector('[name=kontakt]'), zg = form.querySelector('[name=zgoda]');
      if (!kon.value.trim()) { info.textContent = 'Proszę podać telefon lub e-mail do odpowiedzi.'; kon.focus(); return; }
      if (!zg.checked) { info.textContent = 'Proszę zaznaczyć zgodę na kontakt.'; zg.focus(); return; }
      info.textContent = 'Wersja testowa sklepu: formularz nie wysyła danych. W gotowym sklepie zapytanie trafi od razu na smkbiuro@op.pl.';
    });
  }
})();
