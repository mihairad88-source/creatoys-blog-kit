/*!
 * Creatoys Blog Kit v1.0.0
 * Module pentru articolele de pe creatoys.ro/blog. Fără dependențe.
 * Principiu: articolul e complet și fără acest fișier; scriptul adaugă date live și interactivitate.
 */
(function () {
  "use strict";

  var STORE_API = window.CT_STORE_API || (function () {
    var host = location.hostname.replace(/^www\./, "");
    return host === "creatoys.ro" ? "/wp-json/wc/store/v1" : "https://www.creatoys.ro/wp-json/wc/store/v1";
  })();

  /* ---------- Măsurare: GA4 dacă există, altfel dataLayer ---------- */
  function track(name, params) {
    params = params || {};
    params.ct_article = document.title;
    try {
      if (typeof window.gtag === "function") window.gtag("event", name, params);
      else (window.dataLayer = window.dataLayer || []).push(Object.assign({ event: name }, params));
    } catch (e) {}
  }

  function store(key, val) {
    try {
      if (val === undefined) return JSON.parse(localStorage.getItem("ct:" + key) || "null");
      localStorage.setItem("ct:" + key, JSON.stringify(val));
    } catch (e) { return null; }
  }

  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  /* ---------- 1. Bara de progres ---------- */
  function initProgress(article) {
    if (document.querySelector(".ct-progress")) return;
    var bar = document.createElement("div");
    bar.className = "ct-progress";
    bar.setAttribute("aria-hidden", "true");
    bar.innerHTML = "<span></span>";
    document.body.appendChild(bar);
    var fill = bar.firstChild, marks = { 25: 0, 50: 0, 75: 0, 100: 0 }, ticking = false;
    function update() {
      ticking = false;
      var r = article.getBoundingClientRect();
      var total = r.height - window.innerHeight * 0.6;
      var done = Math.min(1, Math.max(0, -r.top / (total > 0 ? total : 1)));
      fill.style.transform = "scaleX(" + done.toFixed(3) + ")";
      [25, 50, 75, 100].forEach(function (m) {
        if (!marks[m] && done * 100 >= m - 0.5) { marks[m] = 1; track("ct_scroll", { percent: m }); }
      });
    }
    window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
    window.addEventListener("resize", update);
    update();
  }

  /* ---------- 2. Carduri de produs live ---------- */
  function money(prices, key) {
    var v = parseInt(prices[key], 10) / Math.pow(10, prices.currency_minor_unit || 0);
    return v.toLocaleString("ro-RO", { minimumFractionDigits: v % 1 ? 2 : 0, maximumFractionDigits: 2 }) + " lei";
  }

  function initProducts(root) {
    var cards = root.querySelectorAll(".ct-product[data-id]");
    if (!cards.length) return;
    var ids = Array.prototype.map.call(cards, function (c) { return c.getAttribute("data-id"); });
    fetch(STORE_API + "/products?per_page=" + ids.length + "&include=" + ids.join(","), { credentials: "omit" })
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function (list) {
        var byId = {};
        list.forEach(function (p) { byId[String(p.id)] = p; });
        Array.prototype.forEach.call(cards, function (card) {
          var p = byId[card.getAttribute("data-id")];
          if (!p || !p.is_in_stock || !p.is_purchasable) { card.hidden = true; return; }
          var price = card.querySelector(".ct-price");
          if (price && p.prices) {
            price.innerHTML = p.on_sale
              ? "<del>" + esc(money(p.prices, "regular_price")) + "</del>" + esc(money(p.prices, "sale_price"))
              : esc(money(p.prices, "price"));
          }
          var img = card.querySelector(".ct-product__img img");
          if (img && p.images && p.images[0] && !img.getAttribute("src")) img.src = p.images[0].src;
        });
        if (!root.querySelector(".ct-product:not([hidden])")) root.hidden = true;
      })
      .catch(function () { /* rămân cardurile statice */ });

    root.addEventListener("click", function (e) {
      var a = e.target.closest("a");
      var card = a && a.closest(".ct-product");
      if (card) track("ct_product_click", { product_id: card.getAttribute("data-id"), product_name: (card.querySelector(".ct-product__name") || {}).textContent });
    });
  }

  /* ---------- 3. Generatorul de cutii ---------- */
  var SHOP = "https://www.creatoys.ro";
  var AGES = {
    "1-2": { label: "1-2 ani", slots: [
      { k: "c", label: "De construit", items: ["cuburi mari sau moi", "cutii de carton goale", "pahare de stivuit"], idea: "cutii de carton de mărimi diferite", shop: ["Turnul de stivuire cu inele", SHOP + "/produs/turn-de-stivuire-cu-inele-din-lemn/"] },
      { k: "b", label: "De băgat și scos", items: ["cratiță cu capac și linguri de lemn", "cutie cu fantă pentru capace mari", "coș cu mingi"], idea: "o cutie de pantofi cu o fantă în capac", shop: ["Jocurile de sortare", SHOP + "/categorie-produs/educative/jocuri-de-sortare/"] },
      { k: "r", label: "De rol", items: ["păpușă sau animal de pluș", "mașinuță mare", "telefon de jucărie"], idea: "o eșarfă și o pălărie din dulap", shop: ["Jucăriile de rol", SHOP + "/categorie-produs/de-rol/"] },
      { k: "l", label: "De răsfoit", items: ["cărți cartonate"], idea: "un album cu poze de familie", shop: null }
    ]},
    "2-3": { label: "2-3 ani", slots: [
      { k: "c", label: "De construit", items: ["cuburi de lemn", "piese mari de construcție", "cutii de mărimi diferite"], idea: "cutii de cereale goale, lipite cu bandă", shop: ["MAGNA-TILES Cubes", SHOP + "/produs/magna-tiles-cubes-primul-meu-set-magnetic/"] },
      { k: "b", label: "De băgat și scos", items: ["cutie de pantofi cu fantă", "borcane de plastic cu capac", "sortator de forme"], idea: "un bol cu capace mari de borcan", shop: ["Spiral Tower de la Quercetti", SHOP + "/produs/spiral-tower-traseu-cu-bile-pentru-bebelusi-quercetti/"] },
      { k: "r", label: "De rol", items: ["vase de bucătărie de jucărie", "figurine de animale", "păpușă cu hăinuțe", "telefon vechi, fără baterie"], idea: "o cratiță mică și o lingură adevărată", shop: ["Jucăriile de rol", SHOP + "/categorie-produs/de-rol/"] },
      { k: "l", label: "De răsfoit", items: ["cărți cu povești scurte"], idea: "o carte de la bibliotecă", shop: null }
    ]},
    "3-5": { label: "3-5 ani", slots: [
      { k: "c", label: "De construit", items: ["plăci magnetice", "set de construcție", "piese de lemn"], idea: "role de hârtie și cutii de ouă", shop: ["MAGNA-TILES Clear Colors, 32 de piese", SHOP + "/produs/magna-tiles-clear-colors-set-magnetic-32-piese/"] },
      { k: "b", label: "De sortat", items: ["bile sau pietre mari", "capace colorate", "puzzle"], idea: "capace colorate de sticlă, pe culori", shop: ["Bilele din lemn Grapat", SHOP + "/produs/bile-din-lemn-set-36-piese-grapat/"] },
      { k: "r", label: "De rol", items: ["figurine", "costume sau pălării", "trusă de doctor sau de bucătărie"], idea: "o cutie mare care devine casă sau magazin", shop: ["Jucăriile de rol", SHOP + "/categorie-produs/de-rol/"] },
      { k: "l", label: "De citit", items: ["cărți cu personaje"], idea: "o carte de la bibliotecă", shop: null }
    ]},
    "5-7": { label: "5-7 ani", slots: [
      { k: "c", label: "Proiectul", items: ["traseu cu bile", "set mare de construcție", "piese mici de construcție"], idea: "un traseu din role de hârtie lipite pe perete", shop: ["Traseul Quercetti Migoga Basic", SHOP + "/produs/quercetti-migoga-marble-run-basic/"] },
      { k: "b", label: "De logică", items: ["joc de societate simplu", "puzzle de peste 100 de piese", "joc de memorie"], idea: "un pachet de cărți de joc", shop: ["Jocurile de logică", SHOP + "/categorie-produs/de-logica/"] },
      { k: "r", label: "De făcut", items: ["carton, bandă adezivă, foarfecă", "plastilină", "creioane și hârtie mare"], idea: "cutii de carton și bandă adezivă", shop: ["Kiturile creative", SHOP + "/categorie-produs/creative/kituri-creative-diy/"] },
      { k: "l", label: "De citit", items: ["cărți pe capitole"], idea: "o carte pe care o citiți împreună", shop: null }
    ]}
  };

  function initBoxes(root) {
    var saved = store("cutii") || {};
    var state = {
      age: AGES[saved.age] ? saved.age : (root.getAttribute("data-age") || "2-3"),
      boxes: saved.boxes >= 3 && saved.boxes <= 6 ? saved.boxes : 4,
      have: saved.have || null
    };
    var started = false;
    var uid = "ct" + Math.random().toString(36).slice(2, 7);

    root.innerHTML =
      '<div class="ct-tool__head">' +
      '<p class="ct-tool__lead">Alege vârsta, bifează ce ai deja în casă și primești cutiile gata împărțite.</p></div>' +
      '<fieldset><legend>Câți ani are copilul?</legend><div class="ct-choices" data-r="ages"></div></fieldset>' +
      '<fieldset><legend>Ce ai deja în casă?</legend><div class="ct-have" data-r="have"></div></fieldset>' +
      '<fieldset><legend id="' + uid + 'n">În câte cutii împarți?</legend><div class="ct-stepper" role="group" aria-labelledby="' + uid + 'n">' +
      '<button type="button" data-r="minus" aria-label="O cutie mai puțin">−</button><output data-r="count" aria-live="polite"></output>' +
      '<button type="button" data-r="plus" aria-label="O cutie în plus">+</button></div></fieldset>' +
      '<div class="ct-result" data-r="result" aria-live="polite"></div>' +
      '<div class="ct-tool__actions"><button type="button" class="ct-btn" data-r="copy">Copiază planul</button>' +
      '<button type="button" class="ct-btn ct-btn--outline" data-r="print">Printează</button></div>';

    var $ = function (r) { return root.querySelector('[data-r="' + r + '"]'); };

    function defaults(age) {
      var h = {};
      AGES[age].slots.forEach(function (s) { s.items.forEach(function (it) { h[s.k + ":" + it] = 1; }); });
      return h;
    }
    function counts() {
      return AGES[state.age].slots.filter(function (s) { return s.k !== "l"; }).map(function (s) {
        return s.items.filter(function (it) { return state.have[s.k + ":" + it]; }).length;
      });
    }
    function recommended() { return Math.min(6, Math.max(3, Math.min.apply(null, counts()))); }
    if (!state.have || saved.age !== state.age) { state.have = defaults(state.age); state.boxes = recommended(); }

    function renderAges() {
      $("ages").innerHTML = Object.keys(AGES).map(function (a) {
        return '<button type="button" class="ct-choice" data-age="' + a + '" aria-pressed="' + (a === state.age) + '">' + AGES[a].label + "</button>";
      }).join("");
    }
    function renderHave() {
      $("have").innerHTML = AGES[state.age].slots.map(function (s) {
        return '<div class="ct-have__group"><b>' + esc(s.label) + "</b>" + s.items.map(function (it) {
          var key = s.k + ":" + it;
          return '<label class="ct-check"><input type="checkbox" data-key="' + esc(key) + '"' + (state.have[key] ? " checked" : "") + "><span>" + esc(it) + "</span></label>";
        }).join("") + "</div>";
      }).join("");
    }

    function plan() {
      var n = state.boxes, boxes = [], gaps = [];
      for (var i = 0; i < n; i++) boxes.push([]);
      AGES[state.age].slots.forEach(function (s) {
        var mine = s.items.filter(function (it) { return state.have[s.k + ":" + it]; });
        if (s.k === "l" && mine.length) { boxes.forEach(function (b) { b.push({ slot: s.label, item: "1-2 " + mine[0] }); }); return; }
        mine.forEach(function (it, j) { boxes[j % n].push({ slot: s.label, item: it }); });
        var missing = Math.max(0, n - mine.length);
        if (missing) {
          for (var m = mine.length; m < n; m++) boxes[m].push({ slot: s.label, gap: true });
          gaps.push({ s: s, missing: missing });
        }
      });
      return { boxes: boxes, gaps: gaps };
    }

    function render() {
      $("count").textContent = state.boxes;
      $("minus").disabled = state.boxes <= 3;
      $("plus").disabled = state.boxes >= 6;
      var p = plan();
      var complete = Math.min.apply(null, counts());
      var html = '<p class="ct-result__sum">' + state.boxes + " cutii. Dacă schimbi o dată pe săptămână, prima cutie revine pe raft după " + state.boxes + " săptămâni, când pare din nou nouă." +
        (complete < state.boxes ? " Cu ce ai bifat, " + (complete === 1 ? "iese completă o cutie" : "ies complete " + complete + " cutii") + "." : "") + "</p>";
      html += '<div class="ct-boxes">' + p.boxes.map(function (b, i) {
        return '<div class="ct-boxcard"><h4>Cutia ' + (i + 1) + "</h4><small>" + (i === 0 ? "pe raft săptămâna asta" : "în dulap, iese în săptămâna " + (i + 1)) + "</small><ul>" +
          b.map(function (x) {
            return x.gap ? '<li class="ct-gap">' + esc(x.slot) + ": lipsește</li>" : "<li>" + esc(x.item) + "</li>";
          }).join("") + "</ul></div>";
      }).join("") + "</div>";
      if (p.gaps.length) {
        html += '<div class="ct-gaps"><p><strong>Ce lipsește ca fiecare cutie să fie completă:</strong></p>' + p.gaps.map(function (g) {
          var shop = g.s.shop ? ' Din magazin: <a href="' + g.s.shop[1] + '" data-ct-gap="' + esc(g.s.label) + '">' + esc(g.s.shop[0]) + "</a>." : "";
          return "<p><strong>" + esc(g.s.label) + "</strong>, " + g.missing + (g.missing === 1 ? " cutie" : " cutii") + ". Idee din casă: " + esc(g.s.idea) + "." + shop + "</p>";
        }).join("") + "</div>";
      } else {
        html += '<div class="ct-gaps"><p><strong>Toate cutiile sunt complete cu ce ai deja.</strong> Nu trebuie să cumperi nimic ca să începi.</p></div>';
      }
      $("result").innerHTML = html;
      store("cutii", state);
    }

    function first() { if (!started) { started = true; track("ct_tool_start", { tool: "cutii" }); } }

    root.addEventListener("click", function (e) {
      var t = e.target.closest("button, a");
      if (!t) return;
      if (t.hasAttribute("data-age")) {
        first(); state.age = t.getAttribute("data-age"); state.have = defaults(state.age); state.boxes = recommended();
        renderAges(); renderHave(); render(); track("ct_tool_age", { tool: "cutii", age: state.age });
      } else if (t === $("minus") && state.boxes > 3) { first(); state.boxes--; render(); }
      else if (t === $("plus") && state.boxes < 6) { first(); state.boxes++; render(); }
      else if (t === $("copy")) { copyPlan(t); }
      else if (t === $("print")) { track("ct_tool_print", { tool: "cutii" }); window.print(); }
      else if (t.hasAttribute("data-ct-gap")) { track("ct_tool_gap_click", { tool: "cutii", slot: t.getAttribute("data-ct-gap") }); }
    });
    root.addEventListener("change", function (e) {
      var k = e.target.getAttribute("data-key");
      if (!k) return;
      first(); if (e.target.checked) state.have[k] = 1; else delete state.have[k];
      render();
    });

    function copyPlan(btn) {
      var p = plan();
      var txt = "Planul de rotație, " + AGES[state.age].label + "\n\n" + p.boxes.map(function (b, i) {
        return "Cutia " + (i + 1) + ":\n" + b.map(function (x) { return " - " + (x.gap ? x.slot + ": lipsește" : x.item); }).join("\n");
      }).join("\n\n") + "\n\nDin ghidul Creatoys: " + location.href.split("#")[0];
      var done = function () { btn.textContent = "Copiat"; setTimeout(function () { btn.textContent = "Copiază planul"; }, 1800); };
      track("ct_tool_copy", { tool: "cutii" });
      if (navigator.clipboard) navigator.clipboard.writeText(txt).then(done, function () {});
    }

    renderAges(); renderHave(); render();
  }

  /* ---------- 4. Acordeoane: măsurăm ce se deschide ---------- */
  function initDetails(article) {
    article.addEventListener("toggle", function (e) {
      var d = e.target;
      if (!d.open || d.tagName !== "DETAILS") return;
      var kind = d.classList.contains("ct-myth") ? "myth" : d.closest(".ct-faq") ? "faq" : "section";
      var s = d.querySelector("summary");
      track("ct_open", { kind: kind, label: s ? s.textContent.trim().slice(0, 90) : "" });
    }, true);
  }

  /* ---------- Pornire ---------- */
  function boot() {
    var article = document.querySelector(".ct-article");
    if (!article || article.getAttribute("data-ct-ready")) return;
    article.setAttribute("data-ct-ready", "1");
    article.classList.add("ct-js");
    initProgress(article);
    initDetails(article);
    article.querySelectorAll("[data-ct='produse']").forEach(initProducts);
    article.querySelectorAll("[data-ct='cutii']").forEach(initBoxes);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
