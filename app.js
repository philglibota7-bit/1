/* =========================================================
   Hygge & Co. — Editorial Cozy · Interaktion
   Alles Platzhalter-Daten: einfach anpassen.
   ========================================================= */

/* ---------- Produkt-Daten (Platzhalter) ---------- */
const PRODUCTS = [
  { id: 1, name: "Duftkerze „Waldruhe“", cat: "kerzen", price: 24.90, emoji: "🕯️", tag: "Bestseller", c1: "#d9a05b", c2: "#c95d3f", desc: "Zedernholz & Vanille für lange Abende." },
  { id: 2, name: "Kuscheldecke „Wolke“", cat: "textil", price: 49.00, emoji: "🧶", tag: "Neu", c1: "#a8c8a0", c2: "#7fa874", desc: "Extra weiche Bio-Baumwolle." },
  { id: 3, name: "Keramik-Tasse „Morgen“", cat: "kueche", price: 16.50, emoji: "☕", tag: "", c1: "#e9c46a", c2: "#d9a05b", desc: "Handgetöpfert, 350 ml." },
  { id: 4, name: "Makramee-Wandbehang", cat: "deko", price: 34.00, emoji: "🪢", tag: "", c1: "#d9b48f", c2: "#a8825d", desc: "Handgeknüpft, 60 cm." },
  { id: 5, name: "Trockenblumen-Strauß", cat: "deko", price: 28.00, emoji: "💐", tag: "Beliebt", c1: "#e7a4a4", c2: "#c97e7e", desc: "Hält jahrelang, ohne Gießen." },
  { id: 6, name: "Teekanne „Ritual“", cat: "kueche", price: 42.00, emoji: "🫖", tag: "", c1: "#8ebfd8", c2: "#5f93ad", desc: "Gusseisen mit Sieb, 0,8 l." },
  { id: 7, name: "Duftkerzen-Set (3er)", cat: "kerzen", price: 59.00, emoji: "🎁", tag: "Set", c1: "#d9a05b", c2: "#a34528", desc: "Drei Jahreszeiten-Düfte." },
  { id: 8, name: "Leinen-Kissenbezug", cat: "textil", price: 22.00, emoji: "🛋️", tag: "", c1: "#cbb7a3", c2: "#96826d", desc: "Gewaschenes Leinen, 45 × 45 cm." },
];

const CAT_NAMES = { kerzen: "Kerzen", textil: "Textil", deko: "Deko", kueche: "Küche" };

const TESTIMONIALS = [
  { text: "Die Kerzen riechen himmlisch und die Verpackung war so liebevoll. Fühlt sich an wie ein Geschenk an mich selbst.", name: "Lena M.", role: "Hamburg", avatar: "🌸", stars: 5, c1: "#e7a4a4", c2: "#c97e7e" },
  { text: "Endlich ein Shop, der Nachhaltigkeit ernst nimmt und dabei so gut aussieht. Meine Decke ist der Wahnsinn.", name: "Jonas K.", role: "Wien", avatar: "🌿", stars: 5, c1: "#a8c8a0", c2: "#7fa874" },
  { text: "Schneller Versand, top Qualität. Die Tasse ist jetzt mein täglicher Begleiter. Klare Empfehlung.", name: "Aylin R.", role: "Zürich", avatar: "☕", stars: 5, c1: "#e9c46a", c2: "#d9a05b" },
];

const fmt = (n) => n.toFixed(2).replace(".", ",") + " €";

/* ---------- State ---------- */
const cart = new Map(); // id -> qty
const favs = new Set();

/* ---------- Produkte rendern ---------- */
const grid = document.getElementById("productGrid");
function renderProducts() {
  grid.innerHTML = PRODUCTS.map((p) => `
    <article class="card reveal" data-cat="${p.cat}" style="--c1:${p.c1};--c2:${p.c2}">
      <div class="card__media">
        ${p.tag ? `<span class="card__badge">${p.tag}</span>` : ""}
        <button class="fav-btn" data-fav="${p.id}" aria-label="Merken">🤍</button>
        <span class="card__emoji">${p.emoji}</span>
      </div>
      <div class="card__body">
        <span class="card__cat">${CAT_NAMES[p.cat]}</span>
        <h3 class="card__name">${p.name}</h3>
        <p class="card__desc">${p.desc}</p>
        <div class="card__foot">
          <span class="card__price">${fmt(p.price)}</span>
          <button class="add-btn" data-add="${p.id}">In den Korb</button>
        </div>
      </div>
    </article>
  `).join("");
  observeReveals();
}

/* ---------- Testimonials rendern ---------- */
document.getElementById("testiGrid").innerHTML = TESTIMONIALS.map((t) => `
  <div class="testi reveal">
    <div class="testi__stars">${"★".repeat(t.stars)}</div>
    <p class="testi__quote">„${t.text}“</p>
    <div class="testi__who">
      <span class="testi__avatar" style="--c1:${t.c1};--c2:${t.c2}">${t.avatar}</span>
      <span>
        <span class="testi__name">${t.name}</span><br />
        <span class="testi__meta">${t.role}</span>
      </span>
    </div>
  </div>
`).join("");

/* ---------- Warenkorb ---------- */
const cartCount = document.getElementById("cartCount");
const cartBody = document.getElementById("cartBody");
const cartTotal = document.getElementById("cartTotal");

function addToCart(id) {
  cart.set(id, (cart.get(id) || 0) + 1);
  const p = PRODUCTS.find((x) => x.id === id);
  updateCart();
  bumpCart();
  showToast(`${p.emoji} ${p.name} hinzugefügt`);
}

function setQty(id, delta) {
  const q = (cart.get(id) || 0) + delta;
  if (q <= 0) cart.delete(id);
  else cart.set(id, q);
  updateCart();
}

function updateCart() {
  let count = 0, total = 0;
  cart.forEach((q, id) => {
    count += q;
    total += q * PRODUCTS.find((p) => p.id === id).price;
  });

  cartCount.textContent = count;
  cartCount.hidden = count === 0;
  cartTotal.textContent = fmt(total);

  if (cart.size === 0) {
    cartBody.innerHTML = `<div class="drawer__empty">Noch ist es still hier.<br />Stöber dich durch die Kollektion.</div>`;
    return;
  }

  cartBody.innerHTML = [...cart.entries()].map(([id, q]) => {
    const p = PRODUCTS.find((x) => x.id === id);
    return `
      <div class="cart-item" style="--c1:${p.c1};--c2:${p.c2}">
        <div class="cart-item__thumb">${p.emoji}</div>
        <div>
          <div class="cart-item__name">${p.name}</div>
          <div class="cart-item__price">${fmt(p.price)}</div>
        </div>
        <div class="cart-item__qty">
          <button class="qty-btn" data-qty="${id}" data-delta="-1" aria-label="Weniger">−</button>
          <span>${q}</span>
          <button class="qty-btn" data-qty="${id}" data-delta="1" aria-label="Mehr">+</button>
        </div>
      </div>`;
  }).join("");
}

function bumpCart() {
  cartCount.style.animation = "none";
  void cartCount.offsetWidth;
  cartCount.style.animation = "pop .3s cubic-bezier(.22,1,.36,1)";
}

/* ---------- Drawer ---------- */
const drawer = document.getElementById("cartDrawer");
const overlay = document.getElementById("drawerOverlay");
function openCart() {
  drawer.classList.add("is-open");
  overlay.hidden = false;
  drawer.setAttribute("aria-hidden", "false");
}
function closeCart() {
  drawer.classList.remove("is-open");
  overlay.hidden = true;
  drawer.setAttribute("aria-hidden", "true");
}

document.getElementById("cartToggle").addEventListener("click", openCart);
document.getElementById("cartClose").addEventListener("click", closeCart);
overlay.addEventListener("click", closeCart);
document.addEventListener("keydown", (e) => { if (e.key === "Escape") closeCart(); });

document.getElementById("checkoutBtn").addEventListener("click", () => {
  if (cart.size === 0) { showToast("Dein Warenkorb ist leer"); return; }
  showToast("Danke! (Demo — kein echter Checkout) ✳");
  cart.clear();
  updateCart();
  setTimeout(closeCart, 900);
});

/* ---------- Zentrale Klick-Delegation ---------- */
document.addEventListener("click", (e) => {
  const add = e.target.closest("[data-add]");
  const qty = e.target.closest("[data-qty]");
  const fav = e.target.closest("[data-fav]");
  if (add) addToCart(+add.dataset.add);
  if (qty) setQty(+qty.dataset.qty, +qty.dataset.delta);
  if (fav) {
    const id = +fav.dataset.fav;
    if (favs.has(id)) { favs.delete(id); fav.textContent = "🤍"; fav.classList.remove("is-fav"); }
    else { favs.add(id); fav.textContent = "❤️"; fav.classList.add("is-fav"); }
  }
});

/* ---------- Filter ---------- */
function applyFilter(f) {
  document.querySelectorAll(".chip").forEach((c) => {
    c.classList.toggle("is-active", c.dataset.filter === f);
  });
  document.querySelectorAll(".card").forEach((card) => {
    card.classList.toggle("is-hidden", f !== "all" && card.dataset.cat !== f);
  });
}

document.getElementById("filters").addEventListener("click", (e) => {
  const chip = e.target.closest(".chip");
  if (chip) applyFilter(chip.dataset.filter);
});

/* XXL-Kategorien: klick filtert die Kollektion */
document.querySelectorAll("[data-cat-link]").forEach((link) => {
  link.addEventListener("click", () => applyFilter(link.dataset.catLink));
});

/* ---------- Toast ---------- */
const toast = document.getElementById("toast");
let toastTimer;
function showToast(msg) {
  toast.textContent = msg;
  toast.classList.add("is-shown");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove("is-shown"), 2400);
}

/* ---------- Theme Toggle ---------- */
const themeBtn = document.getElementById("themeToggle");
const themeIcon = themeBtn.querySelector(".theme-icon");
function applyTheme(t) {
  document.body.dataset.theme = t;
  themeIcon.textContent = t === "dark" ? "○" : "●";
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

/* ---------- Nav & Hero-Parallax bei Scroll ---------- */
const nav = document.getElementById("nav");
const heroBg = document.getElementById("heroBg");
window.addEventListener("scroll", () => {
  const y = window.scrollY;
  nav.classList.toggle("is-scrolled", y > 20);
  if (heroBg && y < window.innerHeight * 1.2) {
    heroBg.style.transform = `translateY(${y * 0.25}px)`;
  }
}, { passive: true });

/* ---------- Scroll-Reveal ---------- */
let revealObserver;
function observeReveals() {
  if (!revealObserver) {
    revealObserver = new IntersectionObserver((entries) => {
      entries.forEach((en) => {
        if (en.isIntersecting) {
          en.target.classList.add("is-visible");
          revealObserver.unobserve(en.target);
        }
      });
    }, { threshold: 0.12 });
  }
  document.querySelectorAll(".reveal:not(.is-visible)").forEach((el) => revealObserver.observe(el));
}

/* ---------- Animierte Zähler ---------- */
function animateCounters() {
  document.querySelectorAll(".stat__num").forEach((el) => {
    const target = +el.dataset.count;
    const dur = 1600;
    const start = performance.now();
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
}, { threshold: 0.4 }).observe(document.getElementById("statsBand"));

/* ---------- Newsletter ---------- */
document.getElementById("newsletterForm").addEventListener("submit", (e) => {
  e.preventDefault();
  const email = document.getElementById("email");
  if (!email.value || !email.value.includes("@")) { showToast("Bitte gültige E-Mail eingeben"); return; }
  document.getElementById("nlNote").hidden = false;
  email.value = "";
  showToast("Willkommen im Club ✳");
});

/* ---------- Init ---------- */
document.getElementById("year").textContent = new Date().getFullYear();
renderProducts();
updateCart();
observeReveals();
