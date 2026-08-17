const PRODUCTS = [
    { id: 1, name: 'Kopfhörer Pro', price: 199.99, category: 'electronics', icon: '🎧', rating: '★★★★★' },
    { id: 2, name: 'Smartwatch X', price: 249.00, category: 'electronics', icon: '⌚', rating: '★★★★☆' },
    { id: 3, name: 'Laptop Ultra', price: 1299.00, category: 'electronics', icon: '💻', rating: '★★★★★' },
    { id: 4, name: 'Smartphone S', price: 899.00, category: 'electronics', icon: '📱', rating: '★★★★☆' },
    { id: 5, name: 'Sneaker Classic', price: 89.99, category: 'fashion', icon: '👟', rating: '★★★★☆' },
    { id: 6, name: 'Lederjacke', price: 249.99, category: 'fashion', icon: '🧥', rating: '★★★★★' },
    { id: 7, name: 'Sonnenbrille', price: 129.00, category: 'fashion', icon: '🕶️', rating: '★★★★☆' },
    { id: 8, name: 'Kaffeemaschine', price: 349.00, category: 'home', icon: '☕', rating: '★★★★★' },
    { id: 9, name: 'Schreibtischlampe', price: 59.99, category: 'home', icon: '💡', rating: '★★★★☆' },
    { id: 10, name: 'Zimmerpflanze', price: 24.99, category: 'home', icon: '🪴', rating: '★★★★★' },
    { id: 11, name: 'Rucksack', price: 79.99, category: 'fashion', icon: '🎒', rating: '★★★★☆' },
    { id: 12, name: 'Bluetooth Speaker', price: 149.00, category: 'electronics', icon: '🔊', rating: '★★★★★' }
];

const SHIPPING = 5.00;

function getCart() {
    try {
        return JSON.parse(localStorage.getItem('shophub_cart')) || [];
    } catch (e) {
        return [];
    }
}

function saveCart(cart) {
    localStorage.setItem('shophub_cart', JSON.stringify(cart));
    updateCartCount();
}

function updateCartCount() {
    const count = getCart().reduce((sum, item) => sum + item.qty, 0);
    document.querySelectorAll('.cart-count').forEach(el => el.textContent = count);
}

function addToCart(id) {
    const cart = getCart();
    const existing = cart.find(item => item.id === id);
    if (existing) {
        existing.qty++;
    } else {
        cart.push({ id: id, qty: 1 });
    }
    saveCart(cart);
    alert('Zum Warenkorb hinzugefügt!');
}

function removeFromCart(id) {
    saveCart(getCart().filter(item => item.id !== id));
    renderCart();
}

function changeQty(id, delta) {
    const cart = getCart();
    const item = cart.find(i => i.id === id);
    if (!item) return;
    item.qty += delta;
    if (item.qty < 1) {
        removeFromCart(id);
        return;
    }
    saveCart(cart);
    renderCart();
}

function productCard(p) {
    return `
        <div class="product-card">
            <div class="product-image">${p.icon}</div>
            <div class="product-info">
                <div class="product-name">${p.name}</div>
                <div class="product-rating">${p.rating}</div>
                <div class="product-price">€${p.price.toFixed(2)}</div>
                <button class="btn btn-add-cart" data-id="${p.id}">In den Warenkorb</button>
            </div>
        </div>`;
}

function renderProducts() {
    const grid = document.getElementById('products');
    if (!grid) return;
    const term = (document.getElementById('search')?.value || '').toLowerCase();
    const cat = document.getElementById('category')?.value || '';
    const list = PRODUCTS.filter(p =>
        p.name.toLowerCase().includes(term) && (!cat || p.category === cat)
    );
    grid.innerHTML = list.length
        ? list.map(productCard).join('')
        : '<p>Keine Produkte gefunden.</p>';
}

function renderFeatured() {
    const grid = document.getElementById('featured');
    if (!grid) return;
    grid.innerHTML = PRODUCTS.slice(0, 4).map(productCard).join('');
}

function cartDetails() {
    return getCart()
        .map(item => {
            const p = PRODUCTS.find(x => x.id === item.id);
            return p ? { ...p, qty: item.qty, sum: p.price * item.qty } : null;
        })
        .filter(Boolean);
}

function renderCart() {
    const body = document.getElementById('cart-body');
    if (!body) return;
    const items = cartDetails();
    const empty = document.getElementById('cart-empty');
    const wrap = document.getElementById('cart-items');

    if (!items.length) {
        empty.style.display = 'block';
        wrap.style.display = 'none';
        return;
    }
    empty.style.display = 'none';
    wrap.style.display = 'block';

    body.innerHTML = items.map(i => `
        <tr>
            <td>${i.icon} ${i.name}</td>
            <td>€${i.price.toFixed(2)}</td>
            <td>
                <div class="quantity-control">
                    <button data-qty="-1" data-id="${i.id}">−</button>
                    <input type="text" value="${i.qty}" readonly>
                    <button data-qty="1" data-id="${i.id}">+</button>
                </div>
            </td>
            <td>€${i.sum.toFixed(2)}</td>
            <td><button class="btn-remove" data-remove="${i.id}">Entfernen</button></td>
        </tr>`).join('');

    const subtotal = items.reduce((s, i) => s + i.sum, 0);
    document.getElementById('subtotal').textContent = '€' + subtotal.toFixed(2);
    document.getElementById('shipping').textContent = '€' + SHIPPING.toFixed(2);
    document.getElementById('total').textContent = '€' + (subtotal + SHIPPING).toFixed(2);
}

function renderCheckout() {
    const box = document.getElementById('order-items');
    if (!box) return;
    const items = cartDetails();
    box.innerHTML = items.length
        ? items.map(i => `
            <div class="order-item">
                <span>${i.icon} ${i.name} × ${i.qty}</span>
                <span>€${i.sum.toFixed(2)}</span>
            </div>`).join('') + `
            <div class="order-item"><span>Versand</span><span>€${SHIPPING.toFixed(2)}</span></div>`
        : '<p>Warenkorb ist leer.</p>';

    const subtotal = items.reduce((s, i) => s + i.sum, 0);
    const total = items.length ? subtotal + SHIPPING : 0;
    document.getElementById('order-total').textContent = '€' + total.toFixed(2);
}

document.addEventListener('click', e => {
    const add = e.target.closest('[data-id]:not([data-qty])');
    if (add && add.classList.contains('btn-add-cart')) {
        addToCart(Number(add.dataset.id));
        return;
    }
    const qty = e.target.closest('[data-qty]');
    if (qty) {
        changeQty(Number(qty.dataset.id), Number(qty.dataset.qty));
        return;
    }
    const rm = e.target.closest('[data-remove]');
    if (rm) removeFromCart(Number(rm.dataset.remove));
});

document.addEventListener('DOMContentLoaded', () => {
    updateCartCount();
    renderFeatured();
    renderProducts();
    renderCart();
    renderCheckout();

    document.getElementById('search')?.addEventListener('input', renderProducts);
    document.getElementById('category')?.addEventListener('change', renderProducts);

    document.getElementById('checkout-form')?.addEventListener('submit', e => {
        e.preventDefault();
        if (!getCart().length) {
            alert('Dein Warenkorb ist leer.');
            return;
        }
        saveCart([]);
        alert('Danke für deine Bestellung!');
        window.location.href = 'index.html';
    });
});
