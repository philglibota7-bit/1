/* =========================================================
   Hygge & Co. — Interaktion
   Alles Platzhalter-Daten: einfach anpassen.
   ========================================================= */

/* ---------- Produkt-Daten (Platzhalter) ---------- */
const PRODUCTS = [
  { id: 1, name: "Duftkerze „Waldruhe“", cat: "kerzen", price: 24.90, emoji: "🕯️", tag: "Bestseller", rating: 5, c1: "#f4a261", c2: "#e76f51", desc: "Warmes Zedernholz & Vanille für gemütliche Abende." },
  { id: 2, name: "Kuscheldecke „Wolke“", cat: "textil", price: 49.00, emoji: "🧶", tag: "Neu", rating: 5, c1: "#a8c8a0", c2: "#8ab17d", desc: "Extra weiche Bio-Baumwolle, waschmaschinenfest." },
  { id: 3, name: "Keramik-Tasse „Morgen“", cat: "kueche", price: 16.50, emoji: "☕", tag: "", rating: 4, c1: "#e9c46a", c2: "#f4a261", desc: "Handgetöpfert, spülmaschinenfest, 350 ml." },
  { id: 4, name: "Makramee-Wandbehang", cat: "deko", price: 34.00, emoji: "🪢", tag: "", rating: 5, c1: "#d9b48f", c2: "#b08968", desc: "Handgeknüpft aus Naturbaumwolle, 60 cm." },
  { id: 5, name: "Trockenblumen-Strauß", cat: "deko", price: 28.00, emoji: "💐", tag: "Beliebt", rating: 5, c1: "#e7a4a4", c2: "#d98c8c", desc: "Hält jahrelang, ganz ohne Gießen." },
  { id: 6, name: "Teekanne „Ritual“", cat: "kueche", price: 42.00, emoji: "🫖", tag: "", rating: 4, c1: "#8ecae6", c2: "#5fa8c9", desc: "Gusseisen mit Sieb, für 0,8 Liter Tee." },
  { id: 7, name: "Duftkerzen-Set (3er)", cat: "kerzen", price: 59.00, emoji: "🎁", tag: "Set", rating: 5, c1: "#f4a261", c2: "#e76f51", desc: "Drei Jahreszeiten-Düfte in einer Box." },
  { id: 8, name: "Leinen-Kissenbezug", cat: "textil", price: 22.00, emoji: "🛋️", tag: "", rating: 4, c1: "#cbb7a3", c2: "#a89685", desc: "Gewaschenes Leinen, 45 × 45 cm, mit Reißverschluss." },
];

const TESTIMONIALS = [
  { text: "Die Kerzen riechen himmlisch und die Verpackung war so liebevoll! Fühlt sich an wie ein Geschenk an mich selbst.", name: "Lena M.", role: "aus Hamburg", avatar: "🌸", stars: 5 },
  { text: "Endlich ein Shop, der Nachhaltigkeit ernst nimmt UND schön aussieht. Meine Decke ist der Wahnsinn.", name: "Jonas K.", role: "aus Wien", avatar: "🌿", stars: 5 },
  { text: "Schneller Versand, top Qualität. Die Tasse ist jetzt mein täglicher Begleiter. Klare Empfehlung!", name: "Aylin R.", role: "aus Zürich", avatar: "☕", stars: 5 },
];

const fmt = (n) => n.toFixed(2).replace(".", ",") + " €";

/* ---------- State ---------- */
const cart = new Map(); // id -> qty
const favs = new Set();

/* ---------- Produkte rendern ---------- */
const grid = document.getElementById("productGrid");
function renderProducts() {
  grid.innerHTML = PRODUCTS.map(p => `
    <article class="card reveal" data-cat="${p.cat}" style="--c1:${p.c1};--c2:${p.c2}">
      <div class="card__media">
        ${p.tag ? `<span class="card__tag">${p.tag}</span>` : ""}
        <button class="card__fav" data-fav="${p.id}" aria-label="Merken">🤍</button>
        <span class="emoji">${p.emoji}</span>
      </div>
      <div class="card__body">
        <div class="card__rating" aria-label="${p.rating} von 5 Sternen">${"★".repeat(p.rating)}${"☆".repeat(5 - p.rating)}</div>
        <h3 class="card__title">${p.name}</h3>
        <p class="card__desc">${p.desc}</p>
        <div class="card__foot">
          <span class="card__price">${fmt(p.price)}</span>
          <button class="card__add" data-add="${p.id}" aria-label="In den Warenkorb">+</button>
        </div>
      </div>
    </article>
  `).join("");
  observeReveals();
}

/* ---------- Testimonials rendern ---------- */
document.getElementById("testiGrid").innerHTML = TESTIMONIALS.map(t => `
  <div class="testi reveal">
    <div class="testi__stars">${"★".repeat(t.stars)}</div>
    <p class="testi__text">„${t.text}“</p>
    <div class="testi__who">
      <span class="testi__avatar">${t.avatar}</span>
      <span><span class="testi__name">${t.name}</span><br><span class="testi__role">${t.role}</span></span>
    </div>
  </div>
`).join("");

/* ---------- Warenkorb-Logik ---------- */
const cartCount = document.getElementById("cartCount");
const cartBody = document.getElementById("cartBody");
const cartTotal = document.getElementById("cartTotal");

function addToCart(id) {
  cart.set(id, (cart.get(id) || 0) + 1);
  const p = PRODUCTS.find(x => x.id === id);
  updateCart();
  bumpCart();
  showToast(`${p.emoji} „${p.name}“ hinzugefügt`);
}

function setQty(id, delta) {
  const q = (cart.get(id) || 0) + delta;
  if (q <= 0) cart.delete(id); else cart.set(id, q);
  updateCart();
}

function updateCart() {
  let count = 0, total = 0;
  cart.forEach((q, id) => { count += q; total += q * PRODUCTS.find(p => p.id === id).price; });

  cartCount.textContent = count;
  cartCount.hidden = count === 0;
  cartTotal.textContent = fmt(total);

  if (cart.size === 0) {
    cartBody.innerHTML = `<div class="drawer__empty"><span>🛒</span>Dein Warenkorb ist noch leer.<br>Stöber dich durch die Kollektion!</div>`;
    return;
  }

  cartBody.innerHTML = [...cart.entries()].map(([id, q]) => {
    const p = PRODUCTS.find(x => x.id === id);
    return `
      <div class="line-item" style="--c1:${p.c1};--c2:${p.c2}">
        <div class="line-item__media">${p.emoji}</div>
        <div class="line-item__info">
          <div class="line-item__title">${p.name}</div>
          <div class="line-item__price">${fmt(p.price)}</div>
          <div class="qty">
            <button data-qty="${id}" data-delta="-1" aria-label="Weniger">−</button>
            <span>${q}</span>
            <button data-qty="${id}" data-delta="1" aria-label="Mehr">+</button>
          </div>
        </div>
        <button class="line-item__remove" data-remove="${id}" aria-label="Entfernen">🗑️</button>
      </div>`;
  }).join("");
}

function bumpCart() {
  cartCount.style.animation = "none";
  void cartCount.offsetWidth;
  cartCount.style.animation = "pop .3s cubic-bezier(.22,1,.36,1)";
}

/* ---------- Drawer öffnen/schließen ---------- */
const drawer = document.getElementById("cartDrawer");
const overlay = document.getElementById("drawerOverlay");
function openCart() { drawer.classList.add("is-open"); overlay.hidden = false; drawer.setAttribute("aria-hidden", "false"); }
function closeCart() { drawer.classList.remove("is-open"); overlay.hidden = true; drawer.setAttribute("aria-hidden", "true"); }

/* ---------- Zentrale Klick-Delegation ---------- */
document.addEventListener("click", (e) => {
  const add = e.target.closest("[data-add]");
  const qty = e.target.closest("[data-qty]");
  const rem = e.target.closest("[data-remove]");
  const fav = e.target.closest("[data-fav]");
  if (add) addToCart(+add.dataset.add);
  if (qty) setQty(+qty.dataset.qty, +qty.dataset.delta);
  if (rem) { cart.delete(+rem.dataset.remove); updateCart(); }
  if (fav) {
    const id = +fav.dataset.fav;
    if (favs.has(id)) { favs.delete(id); fav.textContent = "🤍"; fav.classList.remove("is-fav"); }
    else { favs.add(id); fav.textContent = "❤️"; fav.classList.add("is-fav"); }
  }
});

document.getElementById("cartToggle").addEventListener("click", openCart);
document.getElementById("cartClose").addEventListener("click", closeCart);
overlay.addEventListener("click", closeCart);
document.addEventListener("keydown", (e) => { if (e.key === "Escape") closeCart(); });
document.getElementById("checkoutBtn").addEventListener("click", () => {
  if (cart.size === 0) { showToast("🛒 Dein Warenkorb ist leer"); return; }
  showToast("🎉 Danke! (Demo — kein echter Checkout)");
  cart.clear(); updateCart(); setTimeout(closeCart, 900);
});

/* ---------- Filter ---------- */
document.getElementById("filters").addEventListener("click", (e) => {
  const chip = e.target.closest(".chip");
  if (!chip) return;
  document.querySelectorAll(".chip").forEach(c => c.classList.remove("is-active"));
  chip.classList.add("is-active");
  const f = chip.dataset.filter;
  document.querySelectorAll(".card").forEach(card => {
    card.classList.toggle("is-hidden", f !== "all" && card.dataset.cat !== f);
  });
});

/* ---------- Toast ---------- */
const toast = document.getElementById("toast");
let toastTimer;
function showToast(msg) {
  toast.textContent = msg;
  toast.classList.add("is-show");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove("is-show"), 2400);
}

/* ---------- Theme Toggle ---------- */
const themeBtn = document.getElementById("themeToggle");
const themeIcon = themeBtn.querySelector(".theme-icon");
function applyTheme(t) {
  document.body.dataset.theme = t;
  themeIcon.textContent = t === "dark" ? "☀️" : "🌙";
  try { localStorage.setItem("hc-theme", t); } catch (_) {}
}
themeBtn.addEventListener("click", () => {
  applyTheme(document.body.dataset.theme === "dark" ? "light" : "dark");
});
try {
  const saved = localStorage.getItem("hc-theme");
  if (saved) applyTheme(saved);
  else if (window.matchMedia("(prefers-color-scheme: dark)").matches) applyTheme("dark");
} catch (_) {}

/* ---------- Nav: Schatten bei Scroll ---------- */
const nav = document.getElementById("nav");
window.addEventListener("scroll", () => {
  nav.classList.toggle("is-scrolled", window.scrollY > 20);
}, { passive: true });

/* ---------- Scroll-Reveal ---------- */
let revealObserver;
function observeReveals() {
  if (!revealObserver) {
    revealObserver = new IntersectionObserver((entries) => {
      entries.forEach(en => { if (en.isIntersecting) { en.target.classList.add("is-in"); revealObserver.unobserve(en.target); } });
    }, { threshold: 0.12 });
  }
  document.querySelectorAll(".reveal:not(.is-in)").forEach(el => revealObserver.observe(el));
}

/* ---------- Animierte Zähler ---------- */
function animateCounters() {
  document.querySelectorAll(".stat__num").forEach(el => {
    const target = +el.dataset.count;
    const dur = 1600; const start = performance.now();
    function step(now) {
      const p = Math.min((now - start) / dur, 1);
      const eased = 1 - Math.pow(1 - p, 3);
      const val = Math.floor(eased * target);
      el.textContent = target >= 1000 ? val.toLocaleString("de-DE") : val;
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  });
}
new IntersectionObserver((entries, obs) => {
  if (entries[0].isIntersecting) { animateCounters(); obs.disconnect(); }
}, { threshold: 0.4 }).observe(document.querySelector(".hero__stats"));

/* ---------- 3D-Tilt (Hero-Karte, nur mit Zeiger) ---------- */
const tilt = document.querySelector("[data-tilt]");
if (tilt && window.matchMedia("(pointer: fine)").matches) {
  const card = document.getElementById("heroCard");
  card.addEventListener("mousemove", (e) => {
    const r = tilt.getBoundingClientRect();
    const x = (e.clientX - r.left) / r.width - 0.5;
    const y = (e.clientY - r.top) / r.height - 0.5;
    tilt.style.transform = `perspective(800px) rotateY(${x * 14}deg) rotateX(${-y * 14}deg)`;
  });
  card.addEventListener("mouseleave", () => { tilt.style.transform = ""; });
}

/* ---------- Reaktiver Cursor-Glow ---------- */
const glow = document.querySelector(".cursor-glow");
if (window.matchMedia("(pointer: fine)").matches) {
  window.addEventListener("mousemove", (e) => {
    glow.style.opacity = "1";
    glow.style.transform = `translate(${e.clientX}px, ${e.clientY}px) translate(-50%,-50%)`;
  }, { passive: true });
}

/* ---------- Newsletter ---------- */
document.getElementById("newsletterForm").addEventListener("submit", (e) => {
  e.preventDefault();
  const email = document.getElementById("email");
  if (!email.value || !email.value.includes("@")) { showToast("📧 Bitte gültige E-Mail eingeben"); return; }
  document.getElementById("nlNote").hidden = false;
  email.value = "";
  showToast("💌 Willkommen im Club!");
});

/* ---------- Init ---------- */
document.getElementById("year").textContent = new Date().getFullYear();
renderProducts();
updateCart();
observeReveals();
