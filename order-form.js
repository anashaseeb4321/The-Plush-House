/* =========================================================
   The Plush House — "Place your order" form
   Shared by the homepage and every sofa page.

   Usage:  tphOrder.open({
             product: "Lilly Corner",                 // for tracking
             lines:   [["Lilly Corner sofa", 799],    // what is being ordered
                       ["Ashton Stool", 179]],
             total:   978
           });

   Four required fields only: name, contact number, delivery
   address, postcode. Fabric, colour and sizes are agreed on
   WhatsApp. The form is built the first time it is opened, so
   it costs nothing on page load.
   ========================================================= */
(function () {
  "use strict";
  var WA = "447350939623";
  var built = false, ov, ctx = null, lastFocus = null;

  var CSS = '' +
  '.op-ov{position:fixed;inset:0;z-index:5000;display:none;align-items:center;justify-content:center;padding:20px;background:rgba(8,6,10,.78);backdrop-filter:blur(5px)}' +
  '.op-ov.open{display:flex}' +
  '.op-box{position:relative;width:100%;max-width:560px;max-height:92vh;overflow-y:auto;background:var(--bg-2,#1B1521);border:1px solid var(--line,rgba(201,168,106,.22));border-top:3px solid var(--brass,#C9A86A);border-radius:8px;color:var(--ivory,#F2ECE3);box-shadow:0 30px 60px -25px rgba(0,0,0,.7)}' +
  '.op-head{padding:28px 30px 18px}' +
  '.op-eyebrow{font-size:.7rem;letter-spacing:.24em;text-transform:uppercase;color:var(--wa,#25D366);font-weight:700}' +
  '.op-title{font-family:"Cormorant Garamond","Cormorant FB1","Cormorant FB2",serif;font-size:2rem;font-weight:600;line-height:1.1;margin:6px 0 0}' +
  '.op-x{position:absolute;top:14px;right:14px;width:36px;height:36px;border-radius:50%;background:var(--surface,#221C2A);border:1px solid var(--line-soft,rgba(242,236,227,.08));color:var(--muted,#A99FB0);font-size:1.3rem;line-height:1;cursor:pointer;display:flex;align-items:center;justify-content:center}' +
  '.op-x:hover{color:var(--ivory,#F2ECE3)}' +
  '.op-sum{margin:0 30px;padding:14px 16px;background:var(--surface,#221C2A);border:1px solid var(--line-soft,rgba(242,236,227,.08));border-radius:6px}' +
  '.op-line{display:flex;justify-content:space-between;gap:12px;font-size:.88rem;color:var(--muted,#A99FB0);padding:3px 0}' +
  '.op-line b{color:var(--ivory,#F2ECE3);font-weight:500}' +
  '.op-tot{display:flex;justify-content:space-between;align-items:baseline;border-top:1px solid var(--line-soft,rgba(242,236,227,.08));margin-top:8px;padding-top:10px}' +
  '.op-tot span{font-size:.72rem;letter-spacing:.14em;text-transform:uppercase;font-weight:700}' +
  '.op-tot strong{font-family:"Cormorant Garamond","Cormorant FB1","Cormorant FB2",serif;font-size:1.8rem;color:var(--brass-bright,#E0C58C);font-weight:600}' +
  '.op-form{padding:18px 30px 6px}' +
  '.op-row{display:grid;grid-template-columns:1fr 1fr;gap:14px}' +
  '.op-f{margin-bottom:14px}' +
  '.op-f label{display:block;font-size:.72rem;letter-spacing:.14em;text-transform:uppercase;color:var(--muted,#A99FB0);margin-bottom:6px;font-weight:600}' +
  '.op-f label i{color:var(--brass-bright,#E0C58C);font-style:normal}' +
  '.op-f input,.op-f textarea{width:100%;background:var(--bg,#16121A);border:1px solid var(--line-soft,rgba(242,236,227,.12));border-radius:4px;color:var(--ivory,#F2ECE3);font:inherit;font-size:.95rem;padding:12px 13px}' +
  '.op-f textarea{min-height:72px;resize:vertical;line-height:1.45}' +
  '.op-f input:focus,.op-f textarea:focus{outline:none;border-color:var(--brass,#C9A86A)}' +
  '.op-f.bad input,.op-f.bad textarea{border-color:#e08273}' +
  '.op-err{display:none;font-size:.78rem;color:#e08273;margin-top:5px}' +
  '.op-f.bad .op-err{display:block}' +
  '.op-send{width:100%;display:flex;align-items:center;justify-content:center;gap:10px;border:0;border-radius:4px;background:var(--wa,#25D366);color:#07301A;font:inherit;font-weight:700;font-size:1rem;padding:15px;cursor:pointer;margin-top:4px}' +
  '.op-send:hover{background:#1FBE5B}' +
  '.op-send svg{width:1.15em;height:1.15em;fill:currentColor}' +
  '.op-note{font-size:.78rem;color:var(--muted-2,#958BA0);text-align:center;margin:10px 0 0;line-height:1.5}' +
  '.op-or{display:flex;align-items:center;gap:12px;margin:20px 30px 0;font-size:.7rem;letter-spacing:.2em;text-transform:uppercase;color:var(--muted-2,#958BA0)}' +
  '.op-or:before,.op-or:after{content:"";flex:1;height:1px;background:var(--line-soft,rgba(242,236,227,.08))}' +
  '.op-ask{display:flex;align-items:center;justify-content:center;gap:9px;margin:14px 30px 26px;padding:13px;border:1px solid var(--line,rgba(201,168,106,.22));border-radius:4px;color:var(--ivory,#F2ECE3);font-size:.92rem;font-weight:600;text-decoration:none}' +
  '.op-ask:hover{border-color:var(--brass,#C9A86A);color:var(--brass-bright,#E0C58C);text-decoration:none}' +
  '.op-ask small{display:block;font-weight:400;font-size:.76rem;color:var(--muted,#A99FB0)}' +
  '@media(max-width:560px){.op-ov{padding:0;align-items:flex-end}.op-box{max-height:94vh;border-radius:14px 14px 0 0}' +
  '.op-head{padding:24px 20px 14px}.op-sum{margin:0 20px}.op-form{padding:16px 20px 4px}.op-row{grid-template-columns:1fr;gap:0}' +
  '.op-or{margin:18px 20px 0}.op-ask{margin:12px 20px 22px}.op-title{font-size:1.7rem}}';

  var WA_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2 22l5.25-1.38a9.9 9.9 0 0 0 4.79 1.22h.01c5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.82 9.82 0 0 0 12.04 2Zm4.52 13.97c-.25-.12-1.47-.72-1.69-.81-.23-.08-.39-.12-.56.13-.16.25-.64.81-.79.97-.14.17-.29.19-.54.06-.25-.12-1.05-.39-1.99-1.23-.74-.66-1.23-1.47-1.38-1.72-.14-.25-.01-.38.11-.51.11-.11.25-.29.37-.43.13-.14.17-.25.25-.41.08-.17.04-.31-.02-.43-.06-.12-.56-1.34-.76-1.84-.2-.48-.4-.42-.56-.43h-.48c-.17 0-.43.06-.66.31-.22.25-.86.85-.86 2.07 0 1.22.89 2.4 1.01 2.56.12.17 1.75 2.67 4.23 3.74.59.26 1.05.41 1.41.52.59.19 1.13.16 1.56.1.48-.07 1.47-.6 1.68-1.18.21-.58.21-1.07.14-1.18-.06-.1-.22-.16-.47-.28Z"/></svg>';

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }

  function build() {
    if (built) return; built = true;
    var st = document.createElement("style"); st.textContent = CSS; document.head.appendChild(st);
    ov = document.createElement("div");
    ov.className = "op-ov"; ov.id = "opOverlay";
    ov.setAttribute("role", "dialog"); ov.setAttribute("aria-modal", "true"); ov.setAttribute("aria-labelledby", "opTitle");
    ov.innerHTML =
      '<div class="op-box">' +
        '<button type="button" class="op-x" aria-label="Close">&times;</button>' +
        '<div class="op-head"><div class="op-eyebrow">No payment now</div><h2 class="op-title" id="opTitle">Place your order</h2></div>' +
        '<div class="op-sum" id="opSum"></div>' +
        '<form class="op-form" id="opForm" novalidate>' +
          '<div class="op-row">' +
            '<div class="op-f"><label for="opName">Full name <i>*</i></label><input id="opName" autocomplete="name" placeholder="e.g. Sarah Ahmed"><div class="op-err">Please enter your name.</div></div>' +
            '<div class="op-f"><label for="opPhone">Contact number <i>*</i></label><input id="opPhone" type="tel" inputmode="tel" autocomplete="tel" placeholder="07xxx xxxxxx"><div class="op-err">Please enter a UK mobile or landline number.</div></div>' +
          '</div>' +
          '<div class="op-f"><label for="opAddr">Delivery address <i>*</i></label><textarea id="opAddr" autocomplete="street-address" placeholder="House number, street and town"></textarea><div class="op-err">Please enter the full delivery address.</div></div>' +
          '<div class="op-f" style="max-width:220px"><label for="opPost">Postcode <i>*</i></label><input id="opPost" autocomplete="postal-code" autocapitalize="characters" placeholder="e.g. M1 2AB"><div class="op-err">Please enter a valid UK postcode.</div></div>' +
          '<button type="submit" class="op-send">' + WA_SVG + '<span>Send my order on WhatsApp</span></button>' +
          '<p class="op-note">We confirm on WhatsApp, then deliver, assemble and place it in your home within 24&ndash;72 hours. You settle in cash only once you are happy.</p>' +
        '</form>' +
        '<div class="op-or">or</div>' +
        '<a class="op-ask" id="opAsk" href="#" target="_blank" rel="noopener">' + WA_SVG.replace('<svg', '<svg style="width:1.1em;height:1.1em;fill:currentColor"') +
          '<span>Ask a question first<small>Talk to our team on WhatsApp &mdash; fabric, size, delivery</small></span></a>' +
      '</div>';
    document.body.appendChild(ov);

    ov.addEventListener("click", function (e) { if (e.target === ov || e.target.closest(".op-x")) close(); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && ov.classList.contains("open")) close(); });
    // the "ask" path leaves this form; whatever handles WhatsApp links on the page takes over
    // pointerdown fires before any page-level click handler that takes over WhatsApp links
    ov.querySelector("#opAsk").addEventListener("pointerdown", function () { setTimeout(close, 0); });
    ov.querySelector("#opAsk").addEventListener("click", function () { setTimeout(close, 0); });
    ov.querySelector("#opForm").addEventListener("submit", submit);
    ["opName", "opPhone", "opAddr", "opPost"].forEach(function (id) {
      ov.querySelector("#" + id).addEventListener("input", function () { this.closest(".op-f").classList.remove("bad"); this.removeAttribute("aria-invalid"); });
    });
  }

  function val(id) { return (ov.querySelector("#" + id).value || "").trim(); }
  function bad(id, isBad) {
    var f = ov.querySelector("#" + id).closest(".op-f");
    f.classList.toggle("bad", isBad);
    if (isBad) ov.querySelector("#" + id).setAttribute("aria-invalid", "true");
    return isBad;
  }
  function ukPhone(v) {
    var d = v.replace(/[\s().-]/g, "");
    return /^(\+44|0044|44)?0?\d{9,10}$/.test(d) && d.replace(/\D/g, "").length >= 10;
  }
  function ukPost(v) { return /^[A-Z]{1,2}\d[A-Z\d]?\s*\d[A-Z]{2}$/i.test(v.replace(/\s+/g, " ").trim()); }

  function submit(e) {
    e.preventDefault();
    var name = val("opName"), phone = val("opPhone"), addr = val("opAddr"), post = val("opPost").toUpperCase();
    var errs = [
      bad("opName", name.length < 2),
      bad("opPhone", !ukPhone(phone)),
      bad("opAddr", addr.length < 6),
      bad("opPost", !ukPost(post))
    ];
    var first = ["opName", "opPhone", "opAddr", "opPost"][errs.indexOf(true)];
    if (first) { ov.querySelector("#" + first).focus(); return; }

    var m = "Hi The Plush House! I'd like to place an order:\n\n";
    ctx.lines.forEach(function (l) { m += "• " + l[0] + " — £" + l[1] + "\n"; });
    m += "*Total: £" + ctx.total + "*\n\n";
    m += "Name: " + name + "\nContact number: " + phone + "\nAddress: " + addr.replace(/\s*\n\s*/g, ", ") + "\nPostcode: " + post + "\n\n";
    m += "Payment: in cash, after you deliver, assemble & place it";
    try { if (typeof fbq === "function") fbq("track", "Lead", { content_name: ctx.product, value: ctx.total, currency: "GBP" }); } catch (x) {}
    try { if (typeof gtag === "function") gtag("event", "generate_lead", { product: ctx.product, value: ctx.total, currency: "GBP" }); } catch (x) {}
    window.open("https://wa.me/" + WA + "?text=" + encodeURIComponent(m), "_blank", "noopener");
    close();
  }

  function open(c) {
    build();
    ctx = c;
    var h = "";
    c.lines.forEach(function (l) { h += '<div class="op-line"><b>' + esc(l[0]) + '</b><span>£' + esc(l[1]) + '</span></div>'; });
    h += '<div class="op-tot"><span>Total</span><strong>£' + esc(c.total) + '</strong></div>';
    ov.querySelector("#opSum").innerHTML = h;
    ov.querySelector("#opAsk").href = "https://wa.me/" + WA + "?text=" +
      encodeURIComponent("Hi The Plush House! I have a question about the *" + c.product + "* before I order.");
    ov.querySelectorAll(".op-f.bad").forEach(function (f) { f.classList.remove("bad"); });
    lastFocus = document.activeElement;
    ov.classList.add("open");
    document.documentElement.style.overflow = "hidden";
    setTimeout(function () { var n = ov.querySelector("#opName"); if (n) n.focus({ preventScroll: true }); }, 30);
    try { if (typeof fbq === "function") fbq("track", "InitiateCheckout", { content_name: c.product, value: c.total, currency: "GBP" }); } catch (x) {}
    try { if (typeof gtag === "function") gtag("event", "begin_checkout", { product: c.product, value: c.total, currency: "GBP" }); } catch (x) {}
  }

  function close() {
    if (!ov) return;
    ov.classList.remove("open");
    document.documentElement.style.overflow = "";
    if (lastFocus && lastFocus.focus) try { lastFocus.focus({ preventScroll: true }); } catch (x) {}
  }

  window.tphOrder = { open: open, close: close };
})();
