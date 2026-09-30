# Articolul „Rotația jucăriilor", scris pe Creatoys Blog Kit (clase .ct-*).
# Rulare: python3 rotatia-jucariilor.py <baza-url-assets>  -> out/rotatia-jucariilor.html (fragmentul pentru WordPress)
import sys, pathlib

ASSETS = sys.argv[1] if len(sys.argv) > 1 else "../dist"
SHOP = "https://www.creatoys.ro"

def ext(href, text):
    return f'<a href="{href}" target="_blank" rel="noopener">{text}</a>'

DAUCH = "https://doi.org/10.1016/j.infbeh.2017.11.005"
KOSK = "https://doi.org/10.1016/j.infbeh.2021.101589"
YOGMAN = "https://doi.org/10.1542/peds.2018-2058"
BARKER = "https://doi.org/10.3389/fpsyg.2014.00593"

P = {
 "turn": (885034, "/produs/turn-de-stivuire-cu-inele-din-lemn/", "Turnul de stivuire cu inele din lemn", "https://www.creatoys.ro/wp-content/uploads/2026/03/BS-Toys-GA544-Stacking-Rings-4.webp", "1-4 ani · 10 piese",
          "Primul exercițiu de ordine. După ce îl stăpânește, inelele devin roți, farfurii, monede.", "Singur nu ține mult. Merge bine în cutie cu altele."),
 "spiral": (781571, "/produs/spiral-tower-traseu-cu-bile-pentru-bebelusi-quercetti/", "Spiral Tower de la Quercetti", "https://www.creatoys.ro/wp-content/uploads/2022/05/Quercetti-Spiral-tower-1.jpg", "1-4 ani · 3 bile mari",
          "Trei bile mari coboară pe șapte etaje, iar el vrea să vadă asta de douăzeci de ori.", "Pe la 4 ani devine prea simplu."),
 "cubes": (899003, "/produs/magna-tiles-cubes-primul-meu-set-magnetic/", "MAGNA-TILES Cubes", "https://www.creatoys.ro/wp-content/uploads/2026/07/Magna-Tiles-264013CU-Cubes-9-piese-1.webp", "2-5 ani · 9 cuburi",
          "Magneții prind ușor, deci turnul stă în picioare și la mâini de doi ani.", "Cu 9 piese iese un turn sau un tren. Un castel, nu."),
 "clear": (714835, "/produs/magna-tiles-clear-colors-set-magnetic-32-piese/", "MAGNA-TILES Clear Colors, 32 de piese", "https://www.creatoys.ro/wp-content/uploads/2022/07/Magna-Tiles-02132-Clear-Colors-32-1.jpg", "de la 3 ani · 32 de piese",
          "Destule plăci pentru o construcție care devine garaj, acvariu sau casă pentru figurine.", "Cine prinde gustul o să ceară repede piese în plus."),
 "bile": (743159, "/produs/bile-din-lemn-set-36-piese-grapat/", "Bilele din lemn Grapat, 36 de piese", "https://www.creatoys.ro/wp-content/uploads/2026/04/Grapat-Bile-din-lemn-set-36-piese-01.webp", "de la 3 ani · 36 de bile",
          "Se sortează pe culori, fac trasee, ajung cereale pentru păpuși. Revin din dulap de fiecare dată altfel.", "Recomandate de la 3 ani. Respectă vârsta."),
 "migoga": (16196, "/produs/quercetti-migoga-marble-run-basic/", "Traseul Quercetti Migoga Basic", "https://www.creatoys.ro/wp-content/uploads/2017/03/quercetti-migoga-marble-run-basic-educativ-01.jpg", "5-7 ani · 45 de piese",
          "Montează, vede unde se oprește bila, reface. Exact proiectul care se dărâmă și se reface.", "Traseele ies scurte, iar bilele de sticlă sunt mici. Ține-l departe de frații sub 3 ani."),
}
link = lambda k, t=None: f'<a href="{SHOP}{P[k][1]}">{t or P[k][2]}</a>'

def card(k):
    pid, path, name, img, meta, why, lim = P[k]
    url = SHOP + path
    return (f'<article class="ct-product" data-id="{pid}">'
            f'<a class="ct-product__img" href="{url}" tabindex="-1" aria-hidden="true"><img src="{img}" alt="" loading="lazy" decoding="async" width="600" height="600"></a>'
            f'<div class="ct-product__body"><p class="ct-product__meta">{meta}</p>'
            f'<h3 class="ct-product__name"><a href="{url}" style="color:inherit;text-decoration:none">{name}</a></h3>'
            f'<p class="ct-product__why">{why}</p><p class="ct-product__limit"><strong>Limita:</strong> {lim}</p>'
            f'<div class="ct-product__foot"><span class="ct-price"></span><a class="ct-btn" href="{url}">Vezi jucăria</a></div></div></article>')

def slots(rows):
    return '<div class="ct-slots">' + "".join(f'<div class="ct-slot"><b>{a}</b><span>{b}</span></div>' for a, b in rows) + "</div>"

static_boxes = "".join(
    f'<details class="ct-acc ct-acc--pale"><summary>Cutia pentru {age}</summary><div class="ct-acc__body">{slots(rows)}<p>{extra}</p></div></details>'
    for age, rows, extra in [
        ("1-2 ani", [("De construit", "3-4 cutii de carton goale sau cuburi mari, moi"), ("De băgat și scos", "o cratiță cu capac și câteva linguri de lemn"), ("De rol", "o păpușă sau un animal de pluș"), ("De răsfoit", "o carte cartonată, cu poze mari")], f"Dacă vrei să adaugi ceva: {link('turn')} (1-4 ani)."),
        ("2-3 ani", [("De construit", "cuburi de lemn sau de plastic, câte ai"), ("De băgat și scos", "o cutie de pantofi cu o fantă tăiată în capac"), ("De rol", "vase de bucătărie de jucărie sau un telefon vechi, fără baterie"), ("De răsfoit", "o carte cu o poveste scurtă, pe care o știe")], f"Dacă vrei să adaugi ceva: {link('cubes')} (2-5 ani) sau {link('spiral')} (1-4 ani)."),
        ("3-5 ani", [("De construit", "un set de construcție care stă în picioare"), ("De sortat", "bile, capace sau pietre mari, pe culori"), ("De rol", "figurine care pot locui în ce construiește"), ("De răsfoit", "o carte cu personaje pe care le poate juca")], f"Dacă vrei să adaugi ceva: {link('clear')} sau {link('bile')} (ambele de la 3 ani)."),
        ("5-7 ani", [("Proiectul", "ceva care se construiește, se dărâmă și se reface"), ("De logică", "un joc de societate simplu, pentru doi"), ("De făcut", "carton, bandă adezivă, foarfecă pentru copii"), ("De citit", "o carte pe care o citiți împreună, pe capitole")], f"Dacă vrei să adaugi ceva: {link('migoga')}."),
    ])

faq = [
 ("Câte jucării las la vedere?", f"Nu există un număr verificat pentru acasă. Studiile au comparat 4 cu 16 jucării ({ext(DAUCH, 'Dauch, 2018')}) și 5 cu 12 ({ext(KOSK, 'Koşkulu, 2021')}), nu au căutat numărul ideal. Un punct de plecare practic: cât încape pe un raft fără ca jucăriile să stea una peste alta. Dacă le ia pe toate jos în primele cinci minute, scoate câteva."),
 ("Cât de des schimb jucăriile în rotație?", "Depinde de copil. Semnul e că jucăriile de pe raft nu mai sunt atinse câteva zile la rând. La mulți copii asta înseamnă o dată pe săptămână sau la două săptămâni. Dacă o cutie ține o lună, n-ai de ce să o schimbi."),
 ("De la ce vârstă are sens rotația jucăriilor?", "Cele două studii care o susțin cel mai direct au fost făcute pe copii de 12 luni și de 18-30 de luni. De pe la un an, de când copilul ajunge singur la raft și alege, ai ce roti. Peste 7 ani, rotația contează mai puțin decât spațiul pentru proiecte."),
 ("Ce fac cu jucăriile primite cadou?", "Intră în rotație ca oricare altele. Una rămâne la vedere, restul intră în cutii și apar peste câteva săptămâni. Multe cadouri de sărbători ajung așa să fie folosite abia în februarie, când chiar e nevoie de ceva nou."),
 ("Nu o să se supere copilul că îi iau jucăriile?", "Poate, în primele zile. De aceea ajută să nu arunci nimic, doar să muți, și să lași favoriții pe loc. Copiii mai mari pot alege ei ce cutie iese săptămâna asta. Dacă cere insistent o anumită jucărie, i-o dai. Nu e un test."),
 ("Rotația jucăriilor e o metodă Montessori?", "E asociată des cu Montessori, pentru că pedagogia aceasta pune accent pe un spațiu ordonat, cu puține materiale la vedere, alese pentru vârsta copilului. Nu trebuie însă să urmezi metoda ca să faci rotația. Un raft jos și câteva cutii în dulap sunt de ajuns."),
 ("Ce jucării nu merită păstrate?", "Cele stricate sau incomplete și cele pe care nu le-a mai atins după două-trei ture de rotație. Dacă o jucărie a trecut de trei ori prin raft și a stat neatinsă de fiecare dată, probabil nu mai e pentru el. Poate ajunge la un copil mai mic."),
]

myths = [
 ("mit", "Mit", "„Mai multe jucării înseamnă mai multe opțiuni, deci mai multă joacă.”",
  f"În studiul de la Toledo, cu 16 jucării copiii au sărit de la una la alta. Cu 4, au stat mai mult la fiecare și au folosit-o în mai multe feluri ({ext(DAUCH, 'Dauch, 2018')})."),
 ("mit", "Mit", "„Pentru rotație îți trebuie jucării Montessori.”",
  "Se face cu ce ai deja: cutii de carton, o cratiță, cuburile vechi. Contează câte sunt la vedere, nu de unde sunt."),
 ("adevar", "Adevărat", "„Cu mai puține jucării, părintele se joacă altfel cu copilul.”",
  f"La copiii de 12 luni, cu 5 jucării în loc de 12, mamele au urmat mai des ce făcea copilul, în loc să-i îndrepte atenția spre altceva ({ext(KOSK, 'Koşkulu, 2021')})."),
 ("mit", "Nu chiar", "„Dacă îi ascund jucăriile, o să sufere.”",
  "Poate protesta în primele zile. Nu arunci nimic și favoriții rămân pe loc, iar o jucărie uitată de o lună revine de obicei ca nouă."),
]

def td(label, v): return f'<td data-label="{label}">{v}</td>'
rows = [
 ("Nu mai atinge nimic de pe raft de 3-4 zile", "E rândul cutiei următoare."),
 ("Ia tot jos în primele cinci minute", "Sunt prea multe pe raft. Scoate două."),
 ("Cere o anumită jucărie din dulap", "I-o dai. În schimb, pui în dulap alta de pe raft."),
 ("Se întoarce mereu la aceeași jucărie", "Rămâne permanent. A ieșit din rotație."),
 ("A primit cadouri", "Unul stă la vedere. Restul intră în cutii și apar peste câteva săptămâni."),
]

toc = [("camera-plina", "De ce se plictisește într-o cameră plină"), ("studiile", "Ce au arătat cele două studii"),
       ("mituri", "Mit sau adevăr"), ("de-ce-conteaza", "De ce contează câteva minute în plus"), ("pasi", "Rotația în cinci pași"),
       ("generator", "Generatorul de cutii"), ("semne", "Când schimbi cutia"), ("jucarii", "Jucăriile care rezistă în rotație"),
       ("limite", "Ce nu rezolvă rotația"), ("intrebari", "Întrebări frecvente")]

html = f'''<link rel="stylesheet" href="{ASSETS}/creatoys-blog.css">
<div class="ct-article">

<div class="ct-compare" role="img" aria-label="Comparație: cu 16 jucării la vedere copilul sare de la una la alta, cu 4 jucării stă mai mult la fiecare">
<p class="ct-compare__title">Același copil, aceeași cameră. Doar numărul de jucării diferă.</p>
<div class="ct-compare__panels">
<div class="ct-compare__panel ct-compare__panel--many"><p class="ct-compare__num">16</p><p class="ct-compare__unit">jucării la vedere</p><div class="ct-tiles ct-tiles--16">{"<i></i>"*16}</div><p>Apucă, se uită, lasă, trece la următoarea. Fiecare primește câteva secunde.</p></div>
<div class="ct-compare__panel ct-compare__panel--few"><p class="ct-compare__num">4</p><p class="ct-compare__unit">jucării la vedere</p><div class="ct-tiles ct-tiles--4">{"<i></i>"*4}</div><p>Stă mai mult la fiecare și o întoarce pe toate părțile: o răstoarnă, potrivește, bagă una în alta.</p></div>
</div>
<p class="ct-compare__source">Pe baza studiului {ext(DAUCH, "Dauch et al., 2018")}, 36 de copii de 18-30 de luni.</p>
</div>

<p class="ct-meta">Scris de <strong>echipa Creatoys</strong>, magazin de jucării educative din 2015 · 4 studii citate, cu link la sursă · 10 minute de citit · actualizat în septembrie 2026</p>

<div class="ct-answer"><p><strong>Rotația jucăriilor înseamnă să ții la vedere doar câteva jucării și să le schimbi din când în când cu altele, puse deoparte.</strong> Două echipe de cercetători independente, una din Statele Unite și una din Turcia, au ajuns la același rezultat: <strong>cu mai puține jucării în jur, copiii mici stau mai mult la fiecare, iar joaca cu părintele devine mai bună.</strong> Rotația se face cu ce ai deja în casă.</p></div>

<div class="ct-takeaways"><span class="ct-label">Ce reții în 20 de secunde</span><ul>
<li>La un copil mic, mai multe jucării la vedere nu aduc mai multă joacă. Aduc mai mult zapping.</li>
<li>Rotația cere 4-6 cutii și o oră o singură dată. Nu cere jucării noi.</li>
<li>Schimbi cutia când vezi un semn anume, nu când scrie în calendar.</li>
<li>Generatorul din articol îți împarte jucăriile pe cutii în două minute.</li>
</ul></div>

<details class="ct-acc ct-toc"><summary>Cuprins · {len(toc)} secțiuni</summary><div class="ct-acc__body"><ol>{"".join(f'<li><a href="#{i}">{t}</a></li>' for i, t in toc)}</ol></div></details>

<h2 id="camera-plina">De ce se plictisește un copil într-o cameră plină de jucării</h2>
<p>Seara ai strâns trei lăzi. A doua zi la cinci, totul e iar pe covor, iar copilul se plimbă printre piese și îți spune că n-are cu ce să se joace.</p>
<p>Pare o contradicție, dar explicația e destul de banală. Când are 40 de lucruri la vedere, un copil de doi ani le ia la rând: apucă, se uită, lasă, trece mai departe. Fiecare jucărie primește câteva secunde și nu apucă să fie folosită la ceva. Din afară arată a plictiseală. Seamănă mai mult cu un bufet prea mare.</p>
<p>Camera nu se umple din neglijență. Se umple din cadourile bunicilor, din zilele de naștere, din jucăria luată în drum spre casă după o zi grea. Și dintr-un raft de magazin care vinde după ce scrie pe cutie: 30 de funcții, sunete, lumini. Pe raft, cutia aia bate orice săculeț cu bile de lemn. Pe covorul din sufragerie, de cele mai multe ori pierde.</p>

<h2 id="studiile">Ce au arătat cele două studii despre numărul de jucării</h2>
<div class="ct-stats">
<div class="ct-stat"><b>117</b><span>copii observați, în total</span></div>
<div class="ct-stat"><b>12-30</b><span>luni, vârsta lor</span></div>
<div class="ct-stat ct-stat--warm"><b>2 din 2</b><span>studii, același rezultat</span></div>
</div>
<p>În 2018, o echipă de terapeuți ocupaționali de la Universitatea din Toledo, din Ohio, condusă de Carrie Dauch, a lăsat 36 de copii de 18-30 de luni să se joace liber, fiecare de două ori, sub supraveghere: o dată cu 4 jucării la dispoziție, o dată cu 16 ({ext(DAUCH, "Dauch et al., 2018")}). <strong>Cu 4 jucării, copiii au schimbat mai rar ce aveau în mână, au stat mai mult la fiecare și au găsit mai multe feluri de a se juca cu ea.</strong> Au răsturnat-o, au potrivit piese, au băgat una în alta, s-au prefăcut că e altceva. Cu 16, au sărit de la una la alta.</p>
<p>Trei ani mai târziu, o echipă de la Universitatea Koç din Istanbul a pus întrebarea din alt unghi: ce se întâmplă între părinte și copil? Au observat 81 de mame cu bebeluși de 12 luni, în cinci minute de joacă liberă, unele cu 5 jucării, altele cu 12 ({ext(KOSK, "Koşkulu et al., 2021")}). <strong>Cu 5 jucării, momentele în care mama și copilul se uitau la același lucru au durat mai mult, iar mamele au urmat mai des ce făcea copilul, în loc să-i mute atenția spre altceva.</strong> Momentele erau și mai des coordonate: copilul arăta că știe unde se uită mama, uitându-se la ea, vocalizând sau schimbând pe rând. Iar atenția comună a durat mai mult la jucăriile de organizat, cele cu piese care se așază, se stivuiesc sau se sortează, decât la cele de joc de-a ceva.</p>
<div class="ct-callout ct-callout--limit"><span class="ct-label">Ce nu spun studiile</span><p>Amândouă au eșantioane mici și sesiuni de joacă supravegheate, cu jucării alese de cercetători. Nu măsoară efecte pe termen lung și nu dau un număr ideal de jucării. Arată o direcție, și o arată de două ori, la două echipe diferite.</p></div>

<h2 id="mituri">Mit sau adevăr: ce auzi des despre jucării</h2>
<p>Apasă pe fiecare cartonaș ca să vezi răspunsul.</p>
<div class="ct-myths">
{"".join(f'<details class="ct-myth"><summary><span class="ct-myth__q">{q}</span><span class="ct-myth__hint">Vezi răspunsul</span></summary><div class="ct-myth__a"><span class="ct-verdict ct-verdict--{v}">{vl}</span><p style="margin:0">{a}</p></div></details>' for v, vl, q, a in myths)}
</div>

<h2 id="de-ce-conteaza">De ce contează câteva minute în plus cu aceeași jucărie</h2>
<p>Primele minute cu o jucărie sunt de inventar: ce e, cât cântărește, cum se prinde. Joaca începe după aceea, când cubul devine telefon, cupa devine pălărie și bila devine ou într-un cuib. Un copil care schimbă jucăria la fiecare două minute rămâne în faza de inventar.</p>
<p>Academia Americană de Pediatrie scrie, în raportul ei din 2018 despre joacă, că joaca ajută la dezvoltarea funcțiilor executive ({ext(YOGMAN, "Yogman et al., 2018")}). Sunt abilitățile cu care un copil își ține atenția pe un plan și îl schimbă când planul nu merge.</p>
<p>Un alt studiu, pe copii de 6-7 ani, a găsit că cei care aveau mai mult timp nestructurat în program, fără un adult care să le spună ce urmează, se descurcau mai bine când trebuiau să-și aleagă singuri pasul următor ({ext(BARKER, "Barker et al., 2014")}). E o corelație, nu o dovadă de cauză. Se potrivește însă cu ce s-a văzut la Toledo și la Istanbul.</p>

<h2 id="pasi">Cum faci rotația jucăriilor în cinci pași</h2>
<p class="ct-muted"><strong>Durată:</strong> o oră, o singură dată. După aceea, cinci minute când schimbi cutia.</p>
<ol class="ct-steps">
<li><div><b>Strânge tot într-un singur loc.</b>Tot, inclusiv ce e sub pat și în mașină. Ce e stricat sau i-au dispărut piesele iese acum din casă.</div></li>
<li><div><b>Împarte jucăriile în 4-6 cutii.</b>În fiecare pui câte ceva de construit, ceva ce se bagă în altceva sau se sortează, ceva pentru joc de rol și o carte sau două. Generatorul de mai jos face asta în locul tău.</div></li>
<li><div><b>Lasă la vedere o singură cutie.</b>Pe un raft jos și deschis, nu într-o ladă. Ce stă pe fundul lăzii nu se vede, deci pentru un copil de doi ani nu există. Celelalte cutii merg sus, în dulap.</div></li>
<li><div><b>Favoriții nu intră în rotație.</b>Ursul cu care doarme și mașinuța pe care o duce peste tot rămân unde sunt.</div></li>
<li><div><b>Schimbi cutia când vezi semnul.</b>Dacă nu mai atinge nimic de pe raft de câteva zile, e rândul următoarei. La mulți copii asta înseamnă o dată pe săptămână sau la două. Tabelul cu semne e mai jos.</div></li>
</ol>

<h2 id="generator">Generatorul de cutii: împarte-ți jucăriile în două minute</h2>
<div class="ct-tool" data-ct="cutii" data-age="2-3">
<p>Ce pui în fiecare cutie, în funcție de vârstă. Deschide vârsta copilului tău.</p>
{static_boxes}
</div>

<h2 id="semne">După ce semne știi că e timpul să schimbi cutia</h2>
<div class="ct-table"><table><thead><tr><th>Ce vezi</th><th>Ce faci</th></tr></thead><tbody>
{"".join(f"<tr>{td('Ce vezi', s)}{td('Ce faci', d)}</tr>" for s, d in rows)}
</tbody></table></div>

<h2 id="jucarii">Jucăriile care rezistă cel mai bine în rotație</h2>
<p>Rotația merge cu orice ai. Unele jucării o duc totuși mai bine: cele care nu fac nimic singure. O mașinuță cu sunete face același lucru și a zecea oară. Ce se întâmplă cu un set de bile de lemn depinde de copil, deci e altceva de fiecare dată când revine pe raft. Am ales șase, fiecare cu limita ei.</p>
<div class="ct-products" data-ct="produse">
{"".join(card(k) for k in ["turn", "spiral", "cubes", "clear", "bile", "migoga"])}
</div>

<h2 id="limite">Ce nu rezolvă rotația jucăriilor</h2>
<div class="ct-callout ct-callout--plain">
<p><strong>Nu îți ține locul.</strong> Un copil obosit la 18:30 vrea un om, nu o cutie nouă. Raportul Academiei Americane de Pediatrie despre alegerea jucăriilor spune același lucru: jucăria contează mai ales ca prilej de joacă împreună ({ext("https://doi.org/10.1542/peds.2018-3348", "Healey și Mendelsohn, 2019")}).</p>
<p><strong>Nu e un motiv să cumperi.</strong> Primele luni se fac numai cu ce ai. La strânsul de la început o să vezi probabil cât de multe sunt deja.</p>
<p><strong>Nici n-are nevoie să iasă perfect.</strong> Dacă scoate din dulap ceva din altă cutie, nu s-a stricat nimic. E un obicei, și obiceiurile se mai îndoaie.</p>
<p><strong>Nu știm cât de departe merge efectul.</strong> Studiile au măsurat copii mici, pe durata unor sesiuni de joacă, nu luni întregi. La 6 ani s-ar putea să conteze alte lucruri mai mult.</p>
</div>

<div class="ct-cta">
<p class="ct-cta__title">Pornești o cutie de la zero?</p>
<p>Am strâns într-un loc jucăriile care nu îți spun ce să faci cu ele. Pentru cei mici, separat, jocurile de sortare.</p>
<div class="ct-cta__actions"><a class="ct-btn ct-btn--light" href="{SHOP}/categorie-produs/creative/open-ended/">Vezi jucăriile open-ended</a><a class="ct-btn ct-btn--ghost" href="{SHOP}/categorie-produs/educative/jocuri-de-sortare/">Jocurile de sortare</a></div>
</div>

<h2 id="intrebari">Întrebări frecvente despre rotația jucăriilor</h2>
<div class="ct-faq">
{"".join(f'<details class="ct-acc"><summary>{q}</summary><div class="ct-acc__body"><p>{a}</p></div></details>' for q, a in faq)}
</div>

<h2 id="surse">Surse</h2>
<ol class="ct-sources">
<li>Dauch, C., Imwalle, M., Ocasio, B., &amp; Metz, A. E. (2018). The influence of the number of toys in the environment on toddlers’ play. <em>Infant Behavior and Development</em>, 50, 78-87. {ext(DAUCH, "doi.org/10.1016/j.infbeh.2017.11.005")}</li>
<li>Koşkulu, S., Küntay, A. C., Liszkowski, U., &amp; Uzundag, B. A. (2021). Number and type of toys affect joint attention of mothers and infants. <em>Infant Behavior and Development</em>, 64, 101589. {ext(KOSK, "doi.org/10.1016/j.infbeh.2021.101589")}</li>
<li>Yogman, M., Garner, A., Hutchinson, J., Hirsh-Pasek, K., &amp; Golinkoff, R. M. (2018). The Power of Play: A Pediatric Role in Enhancing Development in Young Children. <em>Pediatrics</em>, 142(3), e20182058. {ext(YOGMAN, "doi.org/10.1542/peds.2018-2058")}</li>
<li>Healey, A., &amp; Mendelsohn, A. (2019). Selecting Appropriate Toys for Young Children in the Digital Era. <em>Pediatrics</em>, 143(1), e20183348. {ext("https://doi.org/10.1542/peds.2018-3348", "doi.org/10.1542/peds.2018-3348")}</li>
<li>Barker, J. E., Semenov, A. D., Michaelson, L., Provan, L. S., Snyder, H. R., &amp; Munakata, Y. (2014). Less-structured time in children’s daily lives predicts self-directed executive functioning. <em>Frontiers in Psychology</em>, 5, 593. {ext(BARKER, "doi.org/10.3389/fpsyg.2014.00593")}</li>
</ol>

</div>
<script src="{ASSETS}/creatoys-blog.js" defer></script>
'''

out = pathlib.Path(__file__).parent / "out"
out.mkdir(exist_ok=True)
(out / "rotatia-jucariilor.html").write_text(html, encoding="utf-8")
print("ok", len(html))
