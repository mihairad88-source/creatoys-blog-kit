# Creatoys Blog Kit v1.0.0

Biblioteca de design și module pentru articolele de pe creatoys.ro/blog.
Articolele se trimit prin REST API ca bloc HTML și încarcă aceste două fișiere.

```
dist/creatoys-blog.css   sistemul de design, totul sub .ct-article
dist/creatoys-blog.js    module, fără dependențe, ~10 KB
articles/*.py            generatoarele articolelor (ies în articles/out/)
demo/index.html          articolul într-o pagină care imită tema XStore
```

## Cum arată un articol

```html
<!-- wp:html -->
<link rel="stylesheet" href="https://CDN/creatoys-blog.css">
<div class="ct-article"> ... </div>
<script src="https://CDN/creatoys-blog.js" defer></script>
<!-- /wp:html -->
```

Blocul `wp:html` e obligatoriu: fără el, WordPress trece conținutul prin `wpautop` și rupe layoutul.
Contul care urcă trebuie să aibă `unfiltered_html` (rol Editor), altfel `<link>` și `<script>` sunt șterse.

## Principiul

Articolul e complet și fără JavaScript. Scriptul doar adaugă: prețuri și stoc live, bara de progres,
instrumentele interactive, măsurarea. Dacă nu se încarcă, cititorul vede tot textul și cardurile statice.

## Componente (doar CSS)

| Clasă | Ce e |
|---|---|
| `.ct-compare` | infograficul comparativ cu pătrățele (16 vs 4), animat discret când JS e activ |
| `.ct-meta` | rândul cu autorul, sursele, timpul de citire |
| `.ct-answer` | răspunsul direct, primul bloc citat de AI |
| `.ct-takeaways` | „Ce reții în 20 de secunde” |
| `.ct-acc`, `.ct-toc` | acordeoane: cuprins, vârste, FAQ |
| `.ct-stats` / `.ct-stat--warm` | cardurile cu cifre |
| `.ct-callout`, `--limit`, `--plain` | casete; `--limit` e „Ce nu spune studiul” |
| `.ct-steps` | pași numerotați automat |
| `.ct-myths` / `.ct-myth` | cartonașele „Mit sau adevăr”, merg fără JS |
| `.ct-slots` | cele patru locuri dintr-o cutie |
| `.ct-table` | tabel; sub 520 px devine carduri (fiecare `td` are `data-label`) |
| `.ct-products` / `.ct-product` | carduri de produs cu „Limita” |
| `.ct-cta` | banda verde de final |
| `.ct-sources` | lista de surse |

## Module (JS)

| Atribut | Ce face |
|---|---|
| `data-ct="produse"` + `.ct-product[data-id]` | aduce preț, preț tăiat la reducere și stoc din Store API; ascunde produsele epuizate |
| `data-ct="cutii"` `data-age="2-3"` | generatorul de cutii; conținutul static din interior e varianta fără JS |
| automat | bara de progres și evenimentele de scroll 25/50/75/100 |
| automat | evenimente la deschiderea mitului, a întrebării frecvente, a secțiunii |

## Evenimente GA4

`ct_scroll`, `ct_open`, `ct_product_click`, `ct_tool_start`, `ct_tool_age`, `ct_tool_copy`,
`ct_tool_print`, `ct_tool_gap_click`. Merg prin `gtag` dacă există, altfel în `dataLayer`.

## Testare locală

`window.CT_STORE_API = "mock"` înainte de script face ca produsele să fie citite din `demo/mock/products`
(răspuns real, salvat), pentru că Store API nu permite cereri de pe alt domeniu.
