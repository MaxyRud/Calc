/* SOFTDRINK product-page kit — shared by all ten plush layouts.
   Product data, a cart that persists in localStorage (shared between layouts),
   a themeable cart drawer, fly-to-cart, toasts, an SVG sprite and small motion helpers.
   Each page themes the drawer through --kit-* CSS variables. */
(function () {
  "use strict";
  var script = document.currentScript;
  var ASSET = script && script.src ? new URL(".", script.src).href : "assets/";
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var finePointer = window.matchMedia("(pointer: fine)").matches;

  var PRODUCT = {
    name: "Zero Can Plush",
    short: "Zero Can",
    sku: "SD-ZC25",
    price: 12.99,
    compare: 19.99,
    rating: 4.9,
    colorways: [
      { id: "ar", name: "Arctic", a: "#eef0f3", b: "#b9bec6" },
      { id: "bl", name: "Blush", a: "#f6bfd2", b: "#e48aa9" },
      { id: "gl", name: "Glacier", a: "#bcdcf6", b: "#7fb4e3" },
      { id: "ma", name: "Matcha", a: "#c4e8c6", b: "#86c58b" }
    ],
    sizes: [
      { id: "25", name: "Classic 25 cm", add: 0 },
      { id: "40", name: "Big hug 40 cm", add: 10 }
    ],
    box: [
      { n: 1, label: "Zero Can plush" },
      { n: 2, label: "Embroidered eyes" },
      { n: 0, label: "Sugar (or caffeine)" }
    ],
    addons: [
      { id: "giftbox", name: "Gift box + message card", price: 3.5 },
      { id: "keychain", name: "Mini can keychain", price: 4.99 },
      { id: "stickers", name: "Sticker sheet · 12 cans", price: 1.99 }
    ],
    bundles: [
      { qty: 1, off: 0, label: "Just me" },
      { qty: 2, off: 0.1, label: "Bestie pack · save 10%" },
      { qty: 3, off: 0.15, label: "Squad · save 15%" }
    ],
    freeShip: 30
  };

  var LAYOUTS = [
    ["01-squish.html", "Squish Lab"],
    ["02-vending.html", "Vending Machine"],
    ["03-frost.html", "Cold Aisle"],
    ["04-rooms.html", "Room Service"],
    ["05-commerce.html", "Classic PDP"],
    ["06-scroll-story.html", "Unwind"],
    ["07-claw.html", "Claw Machine"],
    ["08-y2k.html", "Y2K Sticker Club"],
    ["09-gallery.html", "Exhibit"],
    ["10-gift-builder.html", "Gift Builder"]
  ];

  function img(id, small) { return ASSET + "plush-" + (id || "ar") + (small ? "-sm" : "") + ".webp"; }
  function way(id) { return PRODUCT.colorways.filter(function (c) { return c.id === id; })[0] || PRODUCT.colorways[0]; }
  function size(id) { return PRODUCT.sizes.filter(function (z) { return z.id === id; })[0] || PRODUCT.sizes[0]; }
  function addon(id) { return PRODUCT.addons.filter(function (a) { return a.id === id; })[0]; }
  function money(n) { return "$" + (Math.round(n * 100) / 100).toFixed(2); }
  function bundleOff(q) { return q >= 3 ? 0.15 : q === 2 ? 0.1 : 0; }

  /* ---------- storage (never trusted to exist) ---------- */
  var KEY = "softdrink-cart-v1";
  function load() {
    try { var v = JSON.parse(localStorage.getItem(KEY) || "[]"); return Array.isArray(v) ? v : []; } catch (e) { return []; }
  }
  function save(lines) { try { localStorage.setItem(KEY, JSON.stringify(lines)); } catch (e) { /* private mode */ } }

  /* ---------- cart ---------- */
  var lines = load();
  var listeners = [];
  function emit() { save(lines); render(); listeners.forEach(function (f) { f(totals()); }); }
  function totals() {
    var plushies = 0, plushSum = 0, other = 0, count = 0;
    lines.forEach(function (l) {
      count += l.qty;
      if (l.kind === "plush") { plushies += l.qty; plushSum += l.qty * l.price; } else other += l.qty * l.price;
    });
    var off = bundleOff(plushies);
    var saving = plushSum * off;
    var subtotal = plushSum + other;
    var total = subtotal - saving;
    return { count: count, plushies: plushies, subtotal: subtotal, saving: saving, off: off, total: total,
      toFree: Math.max(0, PRODUCT.freeShip - total) };
  }
  function upsert(line) {
    var hit = lines.filter(function (l) { return l.key === line.key; })[0];
    if (hit) hit.qty = Math.min(99, hit.qty + line.qty); else lines.push(line);
  }
  function addPlush(variant, sz, qty) {
    var w = way(variant), z = size(sz);
    upsert({ key: "p|" + w.id + "|" + z.id, kind: "plush", name: PRODUCT.name, variant: w.name + " · " + z.name, img: img(w.id, true), price: PRODUCT.price + z.add, qty: qty || 1 });
  }
  function addAddon(id, qty) {
    var a = addon(id); if (!a) return;
    upsert({ key: "a|" + a.id, kind: "addon", name: a.name, variant: "Add-on", img: "", price: a.price, qty: qty || 1 });
  }

  /* opts: { variant, size, qty, addons: [ids], from: element, silent } */
  function add(opts) {
    opts = opts || {};
    if (opts.qty !== 0) addPlush(opts.variant || "ar", opts.size || "25", opts.qty || 1);
    (opts.addons || []).forEach(function (id) { addAddon(id, 1); });
    emit();
    if (opts.from) fly(opts.from, img(opts.variant || "ar", true));
    if (!opts.silent) {
      var t = totals();
      toast(opts.message || ("Added to cart · " + t.count + " item" + (t.count === 1 ? "" : "s") + (t.off ? " · bundle −" + Math.round(t.off * 100) + "%" : "")));
    }
    bump();
  }

  /* ---------- sprite ---------- */
  var SPRITE =
    '<svg xmlns="http://www.w3.org/2000/svg" aria-hidden="true" style="position:absolute;width:0;height:0;overflow:hidden">' +
    "<defs>" +
    '<linearGradient id="kit-can" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#c9ced6"/><stop offset=".35" stop-color="#f7f8fa"/><stop offset=".7" stop-color="#eceef1"/><stop offset="1" stop-color="#b8bec7"/></linearGradient>' +
    "</defs>" +
    '<symbol id="i-can" viewBox="0 0 40 64"><rect x="5" y="6" width="30" height="54" rx="9" fill="url(#kit-can)"/><rect x="7" y="3" width="26" height="7" rx="3.5" fill="#d9dde3"/><circle cx="15" cy="34" r="2.6" fill="#16171b"/><circle cx="25" cy="34" r="2.6" fill="#16171b"/><path d="M17 39q3 3 6 0" fill="none" stroke="#16171b" stroke-width="1.6" stroke-linecap="round"/><rect x="9" y="12" width="4" height="40" rx="2" fill="#fff" opacity=".55"/></symbol>' +
    '<symbol id="i-heart" viewBox="0 0 24 24"><path d="M12 20.5s-7.5-4.6-7.5-10.3A4.3 4.3 0 0 1 12 7.6a4.3 4.3 0 0 1 7.5 2.6c0 5.7-7.5 10.3-7.5 10.3z" fill="currentColor"/></symbol>' +
    '<symbol id="i-spark" viewBox="0 0 24 24"><path d="M12 2c.6 4.6 2.4 6.4 7 7-4.6.6-6.4 2.4-7 7-.6-4.6-2.4-6.4-7-7 4.6-.6 6.4-2.4 7-7z" fill="currentColor"/></symbol>' +
    '<symbol id="i-wash" viewBox="0 0 24 24"><path d="M3 7h18l-2 12a2 2 0 0 1-2 1.7H7A2 2 0 0 1 5 19z" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/><path d="M3 7c2 2 4 2 6 0s4-2 6 0 4 2 6 0" fill="none" stroke="currentColor" stroke-width="1.7"/><path d="M10 13h4" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></symbol>' +
    '<symbol id="i-bag" viewBox="0 0 24 24"><path d="M5 8h14l-1.2 12.2a1 1 0 0 1-1 .8H7.2a1 1 0 0 1-1-.8L5 8z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="M9 10V6.5a3 3 0 0 1 6 0V10" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></symbol>' +
    '<symbol id="i-x" viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></symbol>' +
    '<symbol id="i-plus" viewBox="0 0 24 24"><path d="M12 5v14M5 12h14" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></symbol>' +
    '<symbol id="i-minus" viewBox="0 0 24 24"><path d="M5 12h14" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></symbol>' +
    '<symbol id="i-arrow" viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></symbol>' +
    '<symbol id="i-star" viewBox="0 0 24 24"><path d="M12 2.8l2.8 5.9 6.4.8-4.7 4.4 1.2 6.4L12 17.2l-5.7 3.1 1.2-6.4-4.7-4.4 6.4-.8z" fill="currentColor"/></symbol>' +
    '<symbol id="i-check" viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7.5" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></symbol>' +
    '<symbol id="i-shield" viewBox="0 0 24 24"><path d="M12 3l7 3v5.5c0 4.4-3 8.2-7 9.5-4-1.3-7-5.1-7-9.5V6z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="M9 12l2 2 4-4" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></symbol>' +
    '<symbol id="i-truck" viewBox="0 0 24 24"><path d="M3 6h11v10H3zM14 9.5h4l3 3.2V16h-7z" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/><circle cx="7" cy="17.5" r="1.8" fill="none" stroke="currentColor" stroke-width="1.7"/><circle cx="17" cy="17.5" r="1.8" fill="none" stroke="currentColor" stroke-width="1.7"/></symbol>' +
    '<symbol id="i-gift" viewBox="0 0 24 24"><path d="M4 10h16v10H4zM3 7h18v3H3zM12 7v13" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/><path d="M12 7C10 3.5 6.5 4 7 6.2 7.3 7.3 12 7 12 7zm0 0c2-3.5 5.5-3 5-.8-.3 1.1-5 .8-5 .8z" fill="none" stroke="currentColor" stroke-width="1.6"/></symbol>' +
    "</svg>";

  /* ---------- styles for drawer / toast / layout pill ---------- */
  var CSS =
    ":where(:root){--kit-bg:#15121c;--kit-fg:#f4f1fa;--kit-muted:#a69fb6;--kit-accent:#a7e35a;--kit-accent-fg:#111;--kit-line:rgba(255,255,255,.12);--kit-radius:14px;--kit-font:inherit;--kit-scrim:rgba(8,6,12,.55)}" +
    ".kit-scrim{position:fixed;inset:0;background:var(--kit-scrim);opacity:0;pointer-events:none;transition:opacity .35s;z-index:9990;backdrop-filter:blur(2px)}" +
    ".kit-scrim.on{opacity:1;pointer-events:auto}" +
    ".kit-drawer{position:fixed;top:0;right:0;height:100%;width:min(420px,100%);background:var(--kit-bg);color:var(--kit-fg);font-family:var(--kit-font);z-index:9991;display:flex;flex-direction:column;transform:translateX(104%);transition:transform .55s cubic-bezier(.2,.8,.2,1),box-shadow .55s}" +
    ".kit-drawer.on{transform:none;box-shadow:-30px 0 60px rgba(0,0,0,.25)}" +
    ".kit-head{display:flex;align-items:center;justify-content:space-between;padding:20px 20px 12px;border-bottom:1px solid var(--kit-line)}" +
    ".kit-title{margin:0;font-size:20px;font-weight:700;letter-spacing:-.01em}" +
    ".kit-ib{appearance:none;border:1px solid var(--kit-line);background:transparent;color:inherit;width:36px;height:36px;border-radius:50%;display:grid;place-items:center;cursor:pointer}" +
    ".kit-ib svg{width:16px;height:16px}.kit-ib:hover{border-color:var(--kit-accent)}" +
    ".kit-ship{padding:14px 20px;border-bottom:1px solid var(--kit-line);font-size:13px;color:var(--kit-muted)}" +
    ".kit-ship p{margin:8px 0 0}.kit-ship b{color:var(--kit-fg)}" +
    ".kit-bar{height:6px;border-radius:6px;background:var(--kit-line);overflow:hidden}.kit-bar i{display:block;height:100%;width:0;background:var(--kit-accent);border-radius:inherit;transition:width .6s cubic-bezier(.2,.8,.2,1)}" +
    ".kit-lines{list-style:none;margin:0;padding:8px 20px;overflow:auto;flex:1}" +
    ".kit-line{display:grid;grid-template-columns:64px 1fr auto;gap:12px;align-items:center;padding:12px 0;border-bottom:1px solid var(--kit-line);animation:kitIn .4s both}" +
    "@keyframes kitIn{from{opacity:0;transform:translateX(20px)}}" +
    ".kit-thumb{width:64px;height:64px;border-radius:12px;background:var(--kit-line);display:grid;place-items:center;overflow:hidden}.kit-thumb img{height:90%;width:auto}.kit-thumb svg{width:28px;height:28px}" +
    ".kit-line h3{margin:0;font-size:14px;line-height:1.25;font-weight:600}.kit-line small{display:block;color:var(--kit-muted);font-size:12px;margin-top:2px}" +
    ".kit-q{display:inline-flex;align-items:center;gap:6px;margin-top:8px;border:1px solid var(--kit-line);border-radius:99px;padding:2px}" +
    ".kit-q button{appearance:none;border:0;background:transparent;color:inherit;width:24px;height:24px;border-radius:50%;cursor:pointer;display:grid;place-items:center}.kit-q button:hover{background:var(--kit-line)}.kit-q svg{width:12px;height:12px}" +
    ".kit-q span{min-width:18px;text-align:center;font-size:13px;font-variant-numeric:tabular-nums}" +
    ".kit-price{font-size:14px;font-variant-numeric:tabular-nums;text-align:right}" +
    ".kit-rm{display:block;margin-top:6px;font-size:11px;color:var(--kit-muted);background:none;border:0;cursor:pointer;padding:0;text-decoration:underline;font-family:inherit}" +
    ".kit-empty{padding:40px 0;text-align:center;color:var(--kit-muted)}.kit-empty svg{width:40px;height:64px;display:block;margin:0 auto 12px;opacity:.9}" +
    ".kit-foot{padding:16px 20px 20px;border-top:1px solid var(--kit-line);font-size:14px}" +
    ".kit-row{display:flex;justify-content:space-between;margin:4px 0;font-variant-numeric:tabular-nums}.kit-row.save{color:var(--kit-accent)}.kit-row.total{font-size:18px;font-weight:700;margin-top:10px}" +
    ".kit-go{width:100%;margin-top:14px;appearance:none;border:0;border-radius:var(--kit-radius);background:var(--kit-accent);color:var(--kit-accent-fg);font:inherit;font-weight:700;padding:15px;cursor:pointer;transition:transform .2s}.kit-go:hover{transform:translateY(-2px)}" +
    ".kit-note{margin:10px 0 0;font-size:11px;color:var(--kit-muted);text-align:center}" +
    ".kit-toast{position:fixed;left:50%;bottom:24px;transform:translate(-50%,calc(100% + 48px));visibility:hidden;background:var(--kit-fg);color:var(--kit-bg);font-family:var(--kit-font);font-size:14px;font-weight:600;padding:12px 18px;border-radius:99px;z-index:9995;transition:transform .45s cubic-bezier(.2,.9,.2,1.2),visibility 0s .45s;max-width:calc(100% - 32px);text-align:center;box-shadow:0 10px 30px rgba(0,0,0,.25)}" +
    ".kit-toast.on{transform:translate(-50%,0);visibility:visible;transition:transform .45s cubic-bezier(.2,.9,.2,1.2)}" +
    ".kit-fly{position:fixed;z-index:9996;pointer-events:none;width:110px;height:auto;filter:drop-shadow(0 8px 14px rgba(0,0,0,.3))}" +
    ".kit-bump{animation:kitBump .5s cubic-bezier(.3,1.6,.5,1)}@keyframes kitBump{40%{transform:scale(1.35)}}" +
    ".kit-pill{position:fixed;left:16px;bottom:16px;z-index:9980;display:flex;align-items:center;gap:2px;background:rgba(15,13,20,.86);color:#f3effa;font:600 12px/1 ui-sans-serif,system-ui,sans-serif;border-radius:99px;padding:4px;backdrop-filter:blur(8px);box-shadow:0 6px 20px rgba(0,0,0,.25);border:1px solid rgba(255,255,255,.12)}" +
    ".kit-pill a{color:inherit;text-decoration:none;padding:8px 10px;border-radius:99px;white-space:nowrap}.kit-pill a:hover,.kit-pill a:focus-visible{background:rgba(255,255,255,.14)}" +
    ".kit-pill .kit-n{opacity:.6;padding:0 6px 0 2px;font-variant-numeric:tabular-nums}" +
    "@media (max-width:520px){.kit-pill .kit-lbl{display:none}}" +
    "@media (prefers-reduced-motion:reduce){.kit-drawer,.kit-scrim,.kit-toast,.kit-bar i{transition:none}.kit-line,.kit-bump{animation:none}}";

  var drawer, scrim, toastEl, linesEl, footEl, shipEl, lastFocus;

  function el(html) { var d = document.createElement("div"); d.innerHTML = html.trim(); return d.firstChild; }

  function mount() {
    var st = document.createElement("style"); st.textContent = CSS; document.head.appendChild(st);
    document.body.insertAdjacentHTML("afterbegin", SPRITE);
    scrim = el('<div class="kit-scrim" data-kit-close></div>');
    drawer = el(
      '<aside class="kit-drawer" role="dialog" aria-modal="true" aria-label="Shopping cart" aria-hidden="true" tabindex="-1">' +
      '<div class="kit-head"><div class="kit-title" role="heading" aria-level="2">Your cart</div><button class="kit-ib" data-kit-close aria-label="Close cart"><svg><use href="#i-x"/></svg></button></div>' +
      '<div class="kit-ship"><div class="kit-bar"><i></i></div><p></p></div>' +
      '<ul class="kit-lines"></ul><div class="kit-foot"></div></aside>');
    toastEl = el('<div class="kit-toast" role="status" aria-live="polite"></div>');
    document.body.appendChild(scrim); document.body.appendChild(drawer); document.body.appendChild(toastEl);
    linesEl = drawer.querySelector(".kit-lines"); footEl = drawer.querySelector(".kit-foot"); shipEl = drawer.querySelector(".kit-ship");
    drawer.inert = true;

    document.addEventListener("click", function (e) {
      var t = e.target.closest("[data-cart-open],[data-kit-close],[data-kit-inc],[data-kit-dec],[data-kit-rm],[data-kit-go]");
      if (!t) return;
      if (t.hasAttribute("data-cart-open")) { e.preventDefault(); open(); }
      else if (t.hasAttribute("data-kit-close")) close();
      else if (t.hasAttribute("data-kit-go")) toast("Demo checkout — this template does not take payments");
      else {
        var key = t.getAttribute("data-kit-inc") || t.getAttribute("data-kit-dec") || t.getAttribute("data-kit-rm");
        var line = lines.filter(function (l) { return l.key === key; })[0]; if (!line) return;
        if (t.hasAttribute("data-kit-inc")) line.qty = Math.min(99, line.qty + 1);
        else if (t.hasAttribute("data-kit-dec")) line.qty -= 1;
        else line.qty = 0;
        lines = lines.filter(function (l) { return l.qty > 0; });
        emit(); bump();
      }
    });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && drawer.classList.contains("on")) close(); });
    window.addEventListener("storage", function (e) { if (e.key === KEY) { lines = load(); render(); listeners.forEach(function (f) { f(totals()); }); } });
    render();
  }

  function render() {
    var t = totals();
    document.querySelectorAll("[data-cart-count]").forEach(function (n) { n.textContent = t.count; n.setAttribute("data-count", t.count); });
    if (!linesEl) return;
    var pct = Math.min(100, (t.total / PRODUCT.freeShip) * 100);
    shipEl.querySelector("i").style.width = (t.count ? pct : 0) + "%";
    shipEl.querySelector("p").innerHTML = !t.count ? "Free shipping on orders over <b>" + money(PRODUCT.freeShip) + "</b>"
      : t.toFree > 0 ? "You're <b>" + money(t.toFree) + "</b> away from free shipping" : "<b>Free shipping unlocked</b>";
    if (!lines.length) {
      linesEl.innerHTML = '<li class="kit-empty"><svg viewBox="0 0 40 64"><use href="#i-can"/></svg>Your cart is empty.<br>Two plushies save 10%, three save 15%.</li>';
      footEl.innerHTML = "";
      return;
    }
    linesEl.innerHTML = lines.map(function (l) {
      return '<li class="kit-line"><div class="kit-thumb">' + (l.img ? '<img src="' + l.img + '" alt="">' : '<svg viewBox="0 0 24 24" style="color:var(--kit-accent)"><use href="#i-gift"/></svg>') + "</div>" +
        "<div><h3>" + esc(l.name) + "</h3><small>" + esc(l.variant) + " · " + money(l.price) + "</small>" +
        '<div class="kit-q"><button data-kit-dec="' + l.key + '" aria-label="Decrease quantity"><svg><use href="#i-minus"/></svg></button><span>' + l.qty +
        '</span><button data-kit-inc="' + l.key + '" aria-label="Increase quantity"><svg><use href="#i-plus"/></svg></button></div></div>' +
        '<div class="kit-price">' + money(l.qty * l.price) + '<button class="kit-rm" data-kit-rm="' + l.key + '">Remove</button></div></li>';
    }).join("");
    footEl.innerHTML =
      '<div class="kit-row"><span>Subtotal</span><span>' + money(t.subtotal) + "</span></div>" +
      (t.saving ? '<div class="kit-row save"><span>Bundle deal −' + Math.round(t.off * 100) + "% on plushies</span><span>−" + money(t.saving) + "</span></div>" : "") +
      '<div class="kit-row"><span>Shipping</span><span>' + (t.toFree > 0 ? "$3.99" : "Free") + "</span></div>" +
      '<div class="kit-row total"><span>Total</span><span>' + money(t.total + (t.toFree > 0 ? 3.99 : 0)) + "</span></div>" +
      '<button class="kit-go" data-kit-go>Checkout</button><p class="kit-note">Demo store · sample prices</p>';
  }

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }

  function open() {
    lastFocus = document.activeElement;
    drawer.inert = false; drawer.classList.add("on"); scrim.classList.add("on"); drawer.setAttribute("aria-hidden", "false");
    setTimeout(function () { var b = drawer.querySelector("[data-kit-close]"); if (b) b.focus(); }, 50);
  }
  function close() {
    drawer.classList.remove("on"); scrim.classList.remove("on"); drawer.setAttribute("aria-hidden", "true"); drawer.inert = true;
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }

  var toastTimer;
  function toast(msg) {
    if (!toastEl) return;
    toastEl.textContent = msg; toastEl.classList.add("on");
    clearTimeout(toastTimer); toastTimer = setTimeout(function () { toastEl.classList.remove("on"); }, 2600);
  }

  function bump() {
    document.querySelectorAll("[data-cart-open]").forEach(function (b) {
      b.classList.remove("kit-bump"); void b.offsetWidth; b.classList.add("kit-bump");
    });
  }

  function cartTarget() {
    var c = Array.prototype.filter.call(document.querySelectorAll("[data-cart-open]"), function (b) {
      var r = b.getBoundingClientRect(); return r.width && r.bottom > 0 && r.top < innerHeight;
    });
    return c[0];
  }

  function fly(from, src) {
    if (reduced || !from || !from.getBoundingClientRect) return;
    var to = cartTarget(); if (!to) return;
    var a = from.getBoundingClientRect(), b = to.getBoundingClientRect();
    var im = document.createElement("img"); im.src = src; im.alt = ""; im.className = "kit-fly";
    var x0 = a.left + a.width / 2 - 55, y0 = a.top + a.height / 2 - 50, x1 = b.left + b.width / 2 - 55, y1 = b.top + b.height / 2 - 50;
    im.style.left = x0 + "px"; im.style.top = y0 + "px";
    document.body.appendChild(im);
    var dx = x1 - x0, dy = y1 - y0;
    var anim = im.animate([
      { transform: "translate(0,0) scale(1) rotate(0)", opacity: 1 },
      { transform: "translate(" + dx * 0.45 + "px," + (Math.min(dy, 0) * 0.5 - 140) + "px) scale(.8) rotate(-18deg)", opacity: 1, offset: 0.45 },
      { transform: "translate(" + dx + "px," + dy + "px) scale(.15) rotate(-40deg)", opacity: 0.2 }
    ], { duration: 850, easing: "cubic-bezier(.45,0,.25,1)" });
    anim.onfinish = function () { im.remove(); };
  }

  /* ---------- small motion helpers ---------- */
  function magnetic(nodes, strength) {
    if (reduced || !finePointer) return;
    strength = strength || 0.35;
    Array.prototype.forEach.call(nodes, function (n) {
      n.addEventListener("pointermove", function (e) {
        var r = n.getBoundingClientRect();
        n.style.transform = "translate(" + (e.clientX - r.left - r.width / 2) * strength + "px," + (e.clientY - r.top - r.height / 2) * strength + "px)";
      });
      n.addEventListener("pointerleave", function () { n.style.transform = ""; });
    });
  }

  function tilt(node, max, inner) {
    if (reduced || !finePointer || !node) return;
    max = max || 10;
    var raf, tx = 0, ty = 0, cx = 0, cy = 0;
    function loop() {
      cx += (tx - cx) * 0.12; cy += (ty - cy) * 0.12;
      (inner || node).style.transform = "perspective(900px) rotateX(" + (-cy * max).toFixed(2) + "deg) rotateY(" + (cx * max).toFixed(2) + "deg)";
      if (Math.abs(tx - cx) > 0.001 || Math.abs(ty - cy) > 0.001) raf = requestAnimationFrame(loop); else raf = 0;
    }
    node.addEventListener("pointermove", function (e) {
      var r = node.getBoundingClientRect();
      tx = (e.clientX - r.left) / r.width - 0.5; ty = (e.clientY - r.top) / r.height - 0.5;
      if (!raf) raf = requestAnimationFrame(loop);
    });
    node.addEventListener("pointerleave", function () { tx = 0; ty = 0; if (!raf) raf = requestAnimationFrame(loop); });
  }

  /* numbers already show their final value in the HTML; when scrolled into view they count up once */
  function countUp(nodes) {
    if (reduced || !("IntersectionObserver" in window)) return;
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        io.unobserve(e.target);
        var n = e.target, end = parseFloat(n.getAttribute("data-count-to") || n.textContent), dec = (String(end).split(".")[1] || "").length;
        var t0 = performance.now(), d = 1400;
        (function step(t) {
          var k = Math.min(1, (t - t0) / d); k = 1 - Math.pow(1 - k, 3);
          n.textContent = (end * k).toFixed(dec); if (k < 1) requestAnimationFrame(step);
        })(t0);
      });
    }, { threshold: 0.6 });
    Array.prototype.forEach.call(nodes, function (n) { io.observe(n); });
  }

  /* split text into word/char spans (keeps an aria-label with the original text) */
  function split(node, mode) {
    if (!node) return [];
    var text = node.textContent; node.setAttribute("aria-label", text.trim());
    var out = [];
    node.innerHTML = "";
    text.split(/(\s+)/).forEach(function (w) {
      if (/^\s+$/.test(w)) { node.appendChild(document.createTextNode(" ")); return; }
      if (!w) return;
      var ws = document.createElement("span"); ws.className = "w"; ws.setAttribute("aria-hidden", "true");
      if (mode === "chars") {
        w.split("").forEach(function (c) { var s = document.createElement("span"); s.className = "c"; s.textContent = c; ws.appendChild(s); out.push(s); });
      } else { ws.textContent = w; out.push(ws); }
      node.appendChild(ws);
    });
    return out;
  }

  function layoutPill(index) {
    var i = index - 1, n = LAYOUTS.length;
    var prev = LAYOUTS[(i - 1 + n) % n], next = LAYOUTS[(i + 1) % n];
    var pill = el('<nav class="kit-pill" aria-label="Layouts">' +
      '<a href="../index.html" title="All layouts">All<span class="kit-lbl"> layouts</span></a>' +
      '<a href="' + prev[0] + '" aria-label="Previous layout: ' + prev[1] + '">←</a>' +
      '<span class="kit-n">' + String(index).padStart(2, "0") + "/" + n + "</span>" +
      '<a href="' + next[0] + '" aria-label="Next layout: ' + next[1] + '">→</a></nav>');
    document.body.appendChild(pill);
  }

  function deliveryWindow(minDays, maxDays) {
    var f = { month: "short", day: "numeric" };
    var a = new Date(), b = new Date();
    a.setDate(a.getDate() + (minDays || 7)); b.setDate(b.getDate() + (maxDays || 12));
    return a.toLocaleDateString(undefined, f) + " – " + b.toLocaleDateString(undefined, f);
  }

  window.KIT = {
    PRODUCT: PRODUCT, LAYOUTS: LAYOUTS, ASSET: ASSET, reduced: reduced, finePointer: finePointer,
    img: img, way: way, size: size, addon: addon, money: money, bundleOff: bundleOff,
    add: add, open: open, close: close, toast: toast, fly: fly, totals: totals,
    onChange: function (f) { listeners.push(f); f(totals()); },
    magnetic: magnetic, tilt: tilt, countUp: countUp, split: split, layoutPill: layoutPill, deliveryWindow: deliveryWindow
  };

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", mount); else mount();
})();
