# -*- coding: utf-8 -*-
"""
The Plush House — static page generator.

Builds one URL per sofa (/sofas/<slug>.html) and one per category
(/<category>-sofas.html) from the PRODUCTS table below, plus sitemap.xml.

Run after any price, name or image change:    python3 build-pages.py

Keep PRODUCTS here in sync with the PRODUCTS array inside index.html.
"""
import os, io, json, datetime

SITE   = "https://theplushhouse.co.uk"
WA     = "447350939623"
EMAIL  = "info@theplushhouse.co.uk"
TODAY  = "2026-10-13"

# slug = image folder name. url = page filename inside /sofas/.
PRODUCTS = [
 dict(slug="lilly-corner",  url="lilly-corner-sofa",          name="Lilly Corner",         price=799,  cat="corner",
      desc="Soft channel-stitched styling with plush, pillow-back comfort. The Lilly corner is a warm, inviting centrepiece for any family living room.",
      long="The Lilly is the sofa most of our customers come back to. Deep channel stitching across the back, a generous pillow-back that you sink into rather than perch on, and a corner footprint that turns an awkward wall into the best seat in the house. Made to your own measurements, in any of our fabrics or in leather."),
 dict(slug="ashton-corner", url="ashton-corner-sofa",         name="Ashton Corner",        price=849,  cat="corner",
      desc="A clean-lined corner sofa with deep cushioning and a contemporary silhouette. Perfect for modern living spaces.",
      long="Where the Lilly is soft and relaxed, the Ashton is sharp. Straight arms, a tailored back and deep seats that hold their shape — a corner sofa for a room where the lines matter. Available in leather or any of our fabrics, and built to the measurements of your space."),
 dict(slug="verona-corner", url="verona-corner-sofa",         name="Verona Corner",        price=699,  cat="corner",
      desc="Italian-inspired elegance meets everyday comfort. The Verona is a statement piece for any living room.",
      long="Italian-inspired proportions with a low, elegant profile and a corner that wraps the room without crowding it. The Verona is our most accessible corner sofa and still built the same way as the rest of the range — solid frame, deep fill, made to your measurements."),
 dict(slug="shannon-corner",url="harrison-corner-sofa",       name="Harrison Corner",      price=749,  cat="corner",
      desc="Timeless and robust, the Harrison brings classic British furniture craftsmanship to your home.",
      long="A classic British corner sofa: rolled arms, stud detailing and a scatter-back that softens the whole room. The Harrison suits a traditional room without feeling dated, and it is built to take years of family use."),
 dict(slug="olympia-corner",url="olympia-corner-sofa",        name="Olympia Corner",       price=749,  cat="corner",
      desc="Grand and inviting, the Olympia offers generous seating with an elegant corner configuration.",
      long="The Olympia is the most generous corner in the range — wide seats, a tall back and room for the whole household without the sofa dominating the floor. A good choice for a large open-plan living room."),
 dict(slug="borius",        url="borius-corner-sofa",         name="Borius",               price=799,  cat="corner",
      desc="Bold proportions and sumptuous cushioning. The Borius makes a powerful statement without sacrificing everyday comfort.",
      long="Bold, squared-off proportions on slim metal feet, with cushioning deep enough to disappear into. The Borius is a corner sofa with presence — it anchors a room rather than lining its walls."),

 dict(slug="ushape",        url="u-shape-sofa",               name="U-Shape",              price=799,  cat="ushape",
      desc="The ultimate family sofa. Our U-Shape collection wraps your room in comfort with generous seating for the whole household.",
      long="A U-shape puts everybody in the conversation. Seating for six to eight, a wraparound footprint that makes a large room feel finished, and the same deep-fill cushioning as the rest of the range. Built to your own measurements so it fits the room exactly."),
 dict(slug="lilly-ushape",  url="lilly-u-shape-sofa",         name="Lilly U-Shape",        price=849,  cat="ushape",
      desc="The Lilly in a wraparound U-shape — generous family seating with the same soft channel-stitched finish.",
      long="The Lilly design opened out into a full U-shape: the same channel-stitched back and plush pillow cushions, wrapped around three sides of the room. The family sofa for people who do not want to compromise on the finish."),

 dict(slug="lshape",        url="l-shape-sofa",               name="L-Shape",              price=849,  cat="lshape",
      desc="A space-smart L-shape sofa that fits neatly into modern rooms without sacrificing comfort or seating.",
      long="An L-shape gives you corner seating in a smaller footprint — six seats in a frame that still leaves the room breathing space. A good answer for a modern living room that cannot take a full corner."),
 dict(slug="lilly-lshape",  url="lilly-l-shape-sofa",         name="Lilly L-Shape",        price=849,  cat="lshape",
      desc="The Lilly in a space-smart L-shape — plush channel-stitched comfort that fits neatly into modern rooms.",
      long="The Lilly finish on a compact L-shape frame. Channel-stitched back, deep pillow seats and a shorter return so it slots into a room a full corner would overwhelm."),
 dict(slug="ashton-lshape", url="ashton-l-shape-sofa",        name="Ashton L-Shape",       price=849,  cat="lshape",
      desc="The Ashton in a compact L-shape — contemporary styling and deep comfort, perfect for modern living spaces.",
      long="Clean Ashton lines on an L-shape frame — tailored, contemporary and sized for a modern living room. Made to your measurements in leather or any of our fabrics."),

 dict(slug="lilly-set",     url="lilly-2-and-3-seater-sofa",  name="Lilly 2+3 Seater",     price=1149, cat="sets",
      desc="The Lilly two-seater and three-seater set — the same plush channel-stitched design, sold as a matching pair to fill your living room.",
      long="A matching two-seater and three-seater in the Lilly design. Two sofas facing each other change a room far more than one large corner, and this pair arrives, is built and is placed in a single visit."),
 dict(slug="shannon-set",   url="harrison-2-and-3-seater-sofa",name="Harrison 2+3 Seater", price=799,  cat="sets",
      desc="The Harrison two-seater and three-seater set — timeless British craftsmanship, sold as a matching pair.",
      long="The classic Harrison in a matching pair — rolled arms, stud detail and scatter cushions across both pieces. A traditional living room set, delivered and placed together."),
 dict(slug="verona-set",    url="olympia-2-and-3-seater-sofa",name="Olympia 2+3 Seater",   price=799,  cat="sets",
      desc="The Olympia two-seater and three-seater set — grand, elegant proportions, sold as a matching pair.",
      long="The Olympia proportions split across a two-seater and a three-seater. Generous seats, an elegant profile and the flexibility to lay out a room however you like."),
 dict(slug="elaska",        url="elaska-sofa",                name="Elaska",               price=1149, cat="sets",
      desc="Scandinavian-influenced design with clean geometric lines. The Elaska brings sophisticated minimalism to your home.",
      long="Deep button tufting on the arms and base, bolster cushions and a low, geometric frame. The Elaska is the quietest piece in the range and the one that reads most expensive in a plain room."),

 dict(slug="ashton-set",    url="italian-chesterfield-sofa",  name="Italian Chesterfield", price=949,  cat="chesterfield",
      desc="A deep-buttoned Italian take on the Chesterfield — two-seater and three-seater, sold as a matching pair.",
      long="An Italian reading of the Chesterfield: the deep buttoning and the low back are there, but the arms are cleaner and the proportions lighter. Supplied as a matching two-seater and three-seater."),
 dict(slug="chesterfield",  url="ambassador-sofa",            name="Ambassador",           price=1049, cat="chesterfield",
      desc="An icon of British design — deep button tufting, rolled arms and a polished gold base. Sold as a complete set, or piece by piece.",
      long="The Ambassador is the most decorative piece we make: full diamond buttoning, rolled arms and a polished gold base that lifts the whole thing off the floor. Take the three-and-two set, add the single chair for a full suite, or buy a single piece and build up over time.",
      setsFirst=True,
      sets=[["3+2 Seater Set",1049,"Save £149"],["Full Set 3+2+1",1349,"Save £248"]],
      tiers=[["1 Seater",399],["2 Seater",549],["3 Seater",649]],
      setNote="Any matching table or stool is £179 with a sofa · delivered and placed with it"),
 dict(slug="ambassador",    url="chesterfield-sofa",          name="Chesterfield",         price=1249, cat="chesterfield",
      desc="Commanding presence, exceptional comfort. The Chesterfield is built for those who don't compromise on their living space.",
      long="The full Chesterfield, built the traditional way — deep buttoning across the back and arms, a low rolled silhouette and a frame made to outlast the room it sits in. Available with or without the matching table.",
      tiers=[["Without table",1249],["With table",1449]]),
]

CATS = {
 "corner": dict(file="corner-sofas.html", h1="Corner Sofas",
   title="Corner Sofas | Handmade & Delivered Across the UK — The Plush House",
   desc="Handmade corner sofas from The Plush House. Any size, any fabric or leather. We deliver, assemble and place it in your home — you settle only once you are happy.",
   eyebrow="Corner Collection",
   intro="A corner sofa is the piece that decides how a living room works. Ours are made to your own measurements, in any of our fabrics or in leather, and our own team brings each one into your home, assembles it and places it exactly where you want it.",
   body=[("Choosing the right corner for your room",
          "The thing most people get wrong is the return — the short arm of the L. Measure the wall it will sit against, then take 15cm off for skirting and sockets. Send us those measurements on WhatsApp and we will build the sofa to them rather than asking you to live with a standard size."),
         ("What you are actually buying",
          "A hardwood frame, high-density foam with a fibre wrap so the seats keep their shape, and a cover in your choice of around 72 fabrics and 32 colours, or leather. Every corner sofa on this page can be built left-hand or right-hand facing.")]),
 "ushape": dict(file="u-shape-sofas.html", h1="U-Shape Sofas",
   title="U-Shape Sofas | Large Family Sofas, Made to Measure — The Plush House",
   desc="U-shape sofas seating six to eight, made to your own measurements in any fabric or leather. Delivered, assembled and placed in your home by our own team.",
   eyebrow="U-Shape Collection",
   intro="A U-shape is the answer when the whole household wants to sit down at once. Seating for six to eight, wrapped around three sides of the room, built to the measurements of your space rather than to a catalogue size.",
   body=[("Will it fit?",
          "A U-shape needs more floor than people expect, but less than they fear — because we assemble it inside your home, it does not need to come through the door in one piece. Send us your room dimensions and we will tell you honestly whether it works."),
         ("Made for the way a family actually sits",
          "Deep seats, a high back and cushioning dense enough to stay supportive after years of use. Choose from around 72 fabrics and 32 colours, or leather, and add matching stools or a coffee table in the same cover.")]),
 "lshape": dict(file="l-shape-sofas.html", h1="L-Shape Sofas",
   title="L-Shape Sofas | Compact Corner Seating, Made to Measure — The Plush House",
   desc="L-shape sofas that give you corner seating in a smaller footprint. Made to measure in any fabric or leather, delivered and assembled in your home.",
   eyebrow="L-Shape Collection",
   intro="An L-shape gives you most of what a corner sofa gives you, in a frame that leaves the room breathing space. It is the right choice for a modern living room that a full corner would swallow.",
   body=[("L-shape or corner?",
          "A corner sofa has two full-length arms; an L-shape has a shorter return, so it seats nearly as many people while taking up noticeably less wall. If you are unsure, send us the room measurements and we will tell you which one we would put in that space."),
         ("Built to your measurements",
          "Every L-shape here can be built left- or right-hand facing and to your own dimensions, in around 72 fabrics and 32 colours or in leather.")]),
 "sets": dict(file="2-and-3-seater-sofas.html", h1="2 & 3 Seater Sofa Sets",
   title="2 & 3 Seater Sofa Sets | Matching Pairs, Made to Measure — The Plush House",
   desc="Matching two-seater and three-seater sofa sets, made to measure in any fabric or leather. Delivered, assembled and placed in your home in one visit.",
   eyebrow="Sofa Sets",
   intro="Two sofas facing each other change a room more than one large corner does. Every set here arrives as a matching pair, and our team builds and places both pieces in a single visit.",
   body=[("Why a pair instead of a corner",
          "A pair gives you the option to change the room later — angle them, split them across two rooms, or face them across a rug. A corner sofa commits you to one layout for as long as you own it."),
         ("One delivery, both pieces, one settlement",
          "Both sofas come on the same day. Our team carries them in, assembles them, places them where you want them and takes the packaging away — and you settle once for the pair, in cash, when you are happy.")]),
 "chesterfield": dict(file="chesterfield-sofas.html", h1="Chesterfield Sofas",
   title="Chesterfield Sofas | Deep-Buttoned, Handmade — The Plush House",
   desc="Handmade Chesterfield sofas with deep button tufting and rolled arms, in velvet, fabric or leather. Delivered, assembled and placed in your home.",
   eyebrow="Chesterfield Collection",
   intro="Deep diamond buttoning, rolled arms and a low, confident profile. The Chesterfield is the most decorative thing we make, and the pieces on this page are built the traditional way in your choice of velvet, fabric or leather.",
   body=[("Buy the set, or build it up",
          "The Ambassador can be taken as a three-and-two set, as a full suite with the single chair, or one piece at a time. Several of our customers start with the three-seater and add to it later in the same fabric — we keep a record of your cover so the pieces match."),
         ("Velvet, fabric or leather",
          "Buttoning shows best on velvet, wears best in leather and is most forgiving in a textured fabric. Tell us how the room is used and we will tell you which one we would put in it.")]),
}

# ----------------------------------------------------------------------------
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
 '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
 '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600&family=Manrope:wght@400;500;600;700&display=swap" media="print" onload="this.media=\'all\'">'
 '<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600&family=Manrope:wght@400;500;600;700&display=swap"></noscript>')

FAVICON = ('<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2048%2048%22%3E%3Crect%20width%3D%2248%22%20height%3D%2248%22%20rx%3D%2211%22%20fill%3D%22%2316121A%22%2F%3E%3Ccircle%20cx%3D%2224%22%20cy%3D%2224%22%20r%3D%2216.5%22%20fill%3D%22none%22%20stroke%3D%22%23C9A86A%22%20stroke-width%3D%221.6%22%2F%3E%3Cg%20fill%3D%22none%22%20stroke%3D%22%23F2ECE3%22%20stroke-width%3D%222.2%22%20stroke-linecap%3D%22round%22%20stroke-linejoin%3D%22round%22%3E%3Cpath%20d%3D%22M15%2023%20q0%20-4%204%20-4%20h10%20q4%200%204%204%20v3%22%2F%3E%3Cpath%20d%3D%22M13%2029%20q0%20-3%203%20-3%20h16%20q3%200%203%203%20v3%20q0%202%20-2%202%20H15%20q-2%200%20-2%20-2%20z%22%2F%3E%3Cpath%20d%3D%22M16%2036%20v2.5%20M32%2036%20v2.5%22%2F%3E%3C%2Fg%3E%3C%2Fsvg%3E" />')

EMBLEM = ('<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
 '<circle cx="24" cy="24" r="21" stroke="var(--brass)" stroke-width="1.4"/>'
 '<g stroke="var(--ivory)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
 '<path d="M14 23 q0 -4 4 -4 h12 q4 0 4 4 v3"/>'
 '<path d="M12 30 q0 -3 3 -3 h18 q3 0 3 3 v3 q0 2 -2 2 H14 q-2 0 -2 -2 z"/>'
 '<path d="M15 37 v2.5 M33 37 v2.5"/></g></svg>')

WA_IC = ('<svg class="wa-ic" viewBox="0 0 24 24"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2 22l5.25-1.38a9.9 9.9 0 0 0 4.79 1.22h.01c5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.82 9.82 0 0 0 12.04 2Zm0 18.13c-1.5 0-2.97-.4-4.25-1.16l-.3-.18-3.12.82.83-3.04-.2-.31a8.2 8.2 0 0 1-1.26-4.35c0-4.54 3.7-8.23 8.25-8.23 2.2 0 4.27.86 5.82 2.42a8.18 8.18 0 0 1 2.41 5.82c0 4.54-3.7 8.21-8.23 8.21Zm4.52-6.16c-.25-.12-1.47-.72-1.69-.81-.23-.08-.39-.12-.56.13-.16.25-.64.81-.79.97-.14.17-.29.19-.54.06-.25-.12-1.05-.39-1.99-1.23-.74-.66-1.23-1.47-1.38-1.72-.14-.25-.01-.38.11-.51.11-.11.25-.29.37-.43.13-.14.17-.25.25-.41.08-.17.04-.31-.02-.43-.06-.12-.56-1.34-.76-1.84-.2-.48-.4-.42-.56-.43h-.48c-.17 0-.43.06-.66.31-.22.25-.86.85-.86 2.07 0 1.22.89 2.4 1.01 2.56.12.17 1.75 2.67 4.23 3.74.59.26 1.05.41 1.41.52.59.19 1.13.16 1.56.1.48-.07 1.47-.6 1.68-1.18.21-.58.21-1.07.14-1.18-.06-.1-.22-.16-.47-.28Z"/></svg>')

CSS = """
:root{--bg:#16121A;--bg-2:#1B1521;--surface:#221C2A;--surface-2:#2A2233;
--line:rgba(201,168,106,.22);--line-soft:rgba(242,236,227,.08);
--brass:#C9A86A;--brass-bright:#E0C58C;--plum:#3A2A42;--ivory:#F2ECE3;
--muted:#A99FB0;--muted-2:#7C7286;--wa:#25D366;--shadow:0 30px 60px -25px rgba(0,0,0,.7)}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--ivory);font-family:'Manrope',sans-serif;font-size:16px;line-height:1.7;-webkit-font-smoothing:antialiased}
img{max-width:100%;display:block}
a{color:var(--brass-bright);text-decoration:none}
a:hover{text-decoration:underline}
.serif{font-family:'Cormorant Garamond',serif}
.wrap{width:min(1180px,92vw);margin:0 auto}
.wrap-n{width:min(860px,92vw);margin:0 auto}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:9px;font-size:.9rem;font-weight:600;
 letter-spacing:.02em;padding:.95em 1.6em;border-radius:2px;border:1px solid transparent;cursor:pointer;
 font-family:'Manrope',sans-serif;transition:background .22s,border-color .22s,color .22s}
.btn:hover{text-decoration:none}
.btn-wa{background:var(--wa);color:#07301A}
.btn-wa:hover{background:#1FBE5B}
.btn-primary{background:var(--brass);color:#16121A}
.btn-primary:hover{background:var(--brass-bright)}
.btn-ghost{background:transparent;border-color:var(--line);color:var(--ivory)}
.btn-ghost:hover{border-color:var(--brass);color:var(--brass-bright)}
.wa-ic{width:1.15em;height:1.15em;fill:currentColor}
.ribbon{background:linear-gradient(90deg,var(--bg-2),var(--plum),var(--bg-2));border-bottom:1px solid var(--line-soft);
 color:var(--ivory);font-size:.78rem;letter-spacing:.06em;text-transform:uppercase;text-align:center;padding:9px 16px;line-height:1.45}
.ribbon b{color:var(--brass-bright);font-weight:600}
header{position:sticky;top:0;z-index:50;background:rgba(22,18,26,.86);backdrop-filter:blur(14px);border-bottom:1px solid var(--line-soft)}
.nav{display:flex;align-items:center;justify-content:space-between;height:74px;gap:18px}
.brand{display:flex;align-items:center;gap:12px;color:var(--ivory)}
.brand:hover{text-decoration:none}
.brand-mark{width:40px;height:40px;flex-shrink:0}
.brand-mark svg{width:100%;height:100%}
.brand .name{font-size:1.22rem}
.brand .name b{color:var(--brass-bright);font-weight:500}
.nav-links{display:flex;align-items:center;gap:26px}
.nav-links .link{font-size:.88rem;color:var(--muted);letter-spacing:.03em}
.nav-links .link:hover{color:var(--brass-bright);text-decoration:none}
.crumbs{padding:22px 0 0;font-size:.8rem;color:var(--muted-2);letter-spacing:.03em}
.crumbs a{color:var(--muted)}
.crumbs span{margin:0 7px;opacity:.5}
.eyebrow{display:block;font-size:.7rem;letter-spacing:.3em;text-transform:uppercase;color:var(--brass);margin-bottom:14px}
/* product */
.pdp{display:grid;grid-template-columns:1.15fr 1fr;gap:54px;padding:34px 0 70px;align-items:start}
.pgal-main{background:#F2ECE3;border:1px solid var(--line-soft);border-radius:3px;overflow:hidden;aspect-ratio:4/3}
.pgal-main img{width:100%;height:100%;object-fit:cover}
.pgal-thumbs{display:flex;gap:10px;margin-top:12px;flex-wrap:wrap}
.pgal-thumbs button{width:76px;aspect-ratio:1;background:#F2ECE3;border:1px solid var(--line-soft);border-radius:2px;
 overflow:hidden;cursor:pointer;padding:0;transition:border-color .2s}
.pgal-thumbs button.active,.pgal-thumbs button:hover{border-color:var(--brass)}
.pgal-thumbs img{width:100%;height:100%;object-fit:cover}
.pbuy h1{font-family:'Cormorant Garamond',serif;font-size:clamp(2.2rem,4.3vw,3.1rem);font-weight:500;line-height:1.08;margin-bottom:10px}
.pbuy .sub{color:var(--muted);margin-bottom:22px}
.pprice{font-family:'Cormorant Garamond',serif;font-size:2.6rem;font-weight:600;color:var(--brass-bright);line-height:1}
.pprice small{display:block;font-family:'Manrope',sans-serif;font-size:.72rem;font-weight:500;color:var(--muted);
 letter-spacing:.12em;text-transform:uppercase;margin-top:8px}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin:22px 0}
.chips span{font-size:.74rem;color:var(--muted);border:1px solid var(--line-soft);border-radius:2px;padding:6px 11px;letter-spacing:.03em}
.builder{background:var(--surface);border:1px solid var(--line);border-top:2px solid var(--brass);border-radius:3px;padding:22px;margin-bottom:18px}
.builder .bl{font-size:.68rem;letter-spacing:.26em;text-transform:uppercase;color:var(--brass);margin-bottom:14px}
.opt{display:flex;align-items:center;justify-content:space-between;gap:10px;border:1px solid var(--line-soft);
 border-radius:2px;padding:13px 15px;margin-bottom:8px;cursor:pointer;transition:border-color .2s,background .2s}
.opt:hover{border-color:var(--line)}
.opt.active{border-color:var(--brass);background:rgba(201,168,106,.07)}
.opt .l{display:flex;align-items:center;gap:11px;font-size:.92rem}
.radio{width:15px;height:15px;border-radius:50%;border:1.5px solid var(--muted-2);flex-shrink:0;position:relative}
.opt.active .radio{border-color:var(--brass)}
.opt.active .radio::after{content:"";position:absolute;inset:3px;border-radius:50%;background:var(--brass)}
.opt .p{font-family:'Cormorant Garamond',serif;font-size:1.3rem;color:var(--brass-bright)}
.save{font-size:.66rem;font-weight:700;color:var(--wa);background:rgba(37,211,102,.1);border:1px solid rgba(37,211,102,.25);padding:2px 7px;border-radius:2px;letter-spacing:.04em}
.divider{font-size:.66rem;letter-spacing:.22em;text-transform:uppercase;color:var(--muted-2);margin:16px 0 10px}
.note{font-size:.76rem;color:var(--muted-2);margin-top:10px;line-height:1.5}
.builder .addon-wrap{max-height:300px;overflow-y:auto;padding-right:4px}
.addon{display:flex;align-items:center;gap:13px;border:1px solid var(--line-soft);border-radius:2px;padding:11px 13px;margin-bottom:8px;cursor:pointer;transition:border-color .2s,background .2s}
.addon:hover{border-color:var(--line)}
.addon.active{border-color:var(--brass);background:rgba(201,168,106,.07)}
.addon .box{width:15px;height:15px;border:1.5px solid var(--muted-2);border-radius:2px;flex-shrink:0;position:relative}
.addon.active .box{border-color:var(--brass);background:var(--brass)}
.addon.active .box::after{content:"";position:absolute;left:4px;top:1px;width:4px;height:8px;border:solid #16121A;border-width:0 2px 2px 0;transform:rotate(45deg)}
.addon img{width:46px;height:46px;object-fit:cover;border-radius:2px;background:#F2ECE3}
.addon .t{flex:1;font-size:.88rem}
.addon .t small{display:block;color:var(--muted-2);font-size:.73rem}
.addon .p{font-size:.9rem;color:var(--brass-bright);font-weight:600}
.total{display:flex;align-items:baseline;justify-content:space-between;border-top:1px solid var(--line-soft);margin-top:16px;padding-top:16px}
.total .tl{font-size:.7rem;letter-spacing:.22em;text-transform:uppercase;color:var(--muted)}
.total .tv{font-family:'Cormorant Garamond',serif;font-size:2.1rem;font-weight:600;color:var(--brass-bright)}
.pacts{display:flex;flex-direction:column;gap:10px}
.pacts .btn{width:100%;padding:1.1em 1.6em;font-size:.96rem}
.cod{font-size:.78rem;color:var(--muted-2);text-align:center;line-height:1.6;margin-top:14px}
.oform{display:none;background:var(--surface);border:1px solid var(--line);border-radius:3px;padding:22px;margin-bottom:14px}
.oform.open{display:block}
.oform .bl{font-size:.68rem;letter-spacing:.26em;text-transform:uppercase;color:var(--brass);margin-bottom:14px}
.fld{margin-bottom:12px}
.fld label{display:block;font-size:.75rem;color:var(--muted);letter-spacing:.06em;text-transform:uppercase;margin-bottom:6px}
.fld input,.fld textarea{width:100%;background:var(--bg);border:1px solid var(--line-soft);border-radius:2px;
 color:var(--ivory);font-family:'Manrope',sans-serif;font-size:.92rem;padding:11px 13px}
.fld input:focus,.fld textarea:focus{outline:none;border-color:var(--brass)}
.fld textarea{min-height:76px;resize:vertical}
.two{display:grid;grid-template-columns:1fr 1fr;gap:12px}
/* content blocks */
.sec{padding:clamp(52px,7vw,86px) 0;border-top:1px solid var(--line-soft)}
.sec.alt{background:var(--bg-2)}
.sec h1{font-family:'Cormorant Garamond',serif;font-size:clamp(2.3rem,5vw,3.5rem);font-weight:500;line-height:1.08;margin-bottom:18px}
.sec h2{font-family:'Cormorant Garamond',serif;font-size:clamp(1.9rem,3.6vw,2.6rem);font-weight:500;line-height:1.12;margin-bottom:18px}
.sec h3{font-family:'Cormorant Garamond',serif;font-size:1.45rem;font-weight:500;color:var(--brass-bright);margin-bottom:10px}
.sec p{color:var(--muted);margin-bottom:16px;max-width:72ch}
.incl{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--line-soft);border:1px solid var(--line-soft);margin-top:12px}
.incl div{background:var(--bg-2);padding:26px 22px}
.incl .n{font-family:'Cormorant Garamond',serif;font-size:2rem;color:var(--brass);line-height:1}
.incl h4{font-size:1rem;font-weight:600;margin:10px 0 6px}
.incl p{font-size:.86rem;margin:0}
/* grid of sofas */
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:26px}
.card{background:var(--surface);border:1px solid var(--line-soft);border-radius:3px;overflow:hidden;
 display:flex;flex-direction:column;transition:border-color .25s,transform .25s}
.card:hover{border-color:var(--line);transform:translateY(-3px)}
.card:hover{text-decoration:none}
.card-img{aspect-ratio:4/3;background:#F2ECE3;overflow:hidden}
.card-img img{width:100%;height:100%;object-fit:cover;transition:transform .5s}
.card:hover .card-img img{transform:scale(1.04)}
.card-b{padding:22px 22px 24px;display:flex;flex-direction:column;flex:1}
.card-b h3{font-family:'Cormorant Garamond',serif;font-size:1.5rem;font-weight:500;color:var(--ivory);margin-bottom:6px}
.card-b p{color:var(--muted);font-size:.86rem;margin-bottom:16px;flex:1}
.card-p{font-family:'Cormorant Garamond',serif;font-size:1.8rem;font-weight:600;color:var(--brass-bright);line-height:1}
.card-p small{display:block;font-family:'Manrope',sans-serif;font-size:.68rem;font-weight:500;color:var(--muted-2);letter-spacing:.08em;text-transform:uppercase;margin-top:5px}
/* footer */
footer{border-top:1px solid var(--line-soft);background:var(--bg-2);padding:52px 0 30px}
.fgrid{display:grid;grid-template-columns:1.6fr 1fr 1fr 1fr;gap:38px;margin-bottom:36px}
.fgrid p{color:var(--muted);font-size:.88rem;margin-top:14px;max-width:300px}
.fcol h4{font-size:.72rem;letter-spacing:.26em;text-transform:uppercase;color:var(--brass);margin-bottom:16px}
.fcol a{display:block;color:var(--muted);font-size:.9rem;margin-bottom:10px}
.fcol a:hover{color:var(--ivory)}
.fbot{border-top:1px solid var(--line-soft);padding-top:20px;display:flex;justify-content:space-between;
 flex-wrap:wrap;gap:10px;color:var(--muted-2);font-size:.78rem}
@media(max-width:980px){.pdp{grid-template-columns:1fr;gap:34px}.incl{grid-template-columns:1fr 1fr}.grid{grid-template-columns:1fr 1fr}.fgrid{grid-template-columns:1fr 1fr}}
@media(max-width:640px){.nav-links .link{display:none}.incl,.grid,.fgrid,.two{grid-template-columns:1fr}
 .ribbon{font-size:.66rem;letter-spacing:.03em}.brand .name{font-size:1.05rem}}
"""

TRACK = """
<script>
!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;
n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,
document,'script','https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '2826953844350921');
fbq('consent', 'revoke');
try{ if(localStorage.getItem('tph_consent')==='granted') fbq('consent','grant'); }catch(e){}
fbq('track', 'PageView');
</script>
<noscript><img height="1" width="1" style="display:none"
src="https://www.facebook.com/tr?id=2826953844350921&ev=PageView&noscript=1"/></noscript>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('consent','default',{ad_storage:'denied',analytics_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',wait_for_update:500});
  try{ if(localStorage.getItem('tph_consent')==='granted'){
    gtag('consent','update',{ad_storage:'granted',analytics_storage:'granted',ad_user_data:'granted',ad_personalization:'granted'});
  } }catch(e){}
</script>
<script src="/analytics.js" defer></script>
"""

CONSENT = """
<style>
 #tphConsent{position:fixed;left:16px;right:16px;bottom:16px;z-index:9999;max-width:560px;margin:0 auto;
  background:var(--surface);color:var(--ivory);border:1px solid var(--line);border-top:3px solid var(--brass);
  border-radius:4px;padding:20px 22px;box-shadow:var(--shadow);display:none}
 #tphConsent.show{display:block}
 #tphConsent p{font-size:13.5px;line-height:1.6;color:var(--muted);margin:0 0 14px}
 #tphConsent a{color:var(--brass-bright);text-decoration:underline}
 #tphConsent .b{display:flex;gap:10px;flex-wrap:wrap}
 #tphConsent button{font-family:inherit;font-size:13.5px;font-weight:600;padding:10px 20px;border-radius:2px;cursor:pointer;border:none}
 #tphConsent .a{background:var(--brass);color:#16121A}
 #tphConsent .r{background:transparent;color:var(--muted);border:1px solid var(--line-soft)}
</style>
<div id="tphConsent" role="dialog" aria-label="Cookie consent">
  <p>We use cookies to run this site and to measure our advertising (Google &amp; Meta). You can accept these or continue with only what is essential. See our <a href="/privacy.html">Privacy Policy</a>.</p>
  <div class="b"><button class="a" id="tphAccept">Accept all</button><button class="r" id="tphReject">Essential only</button></div>
</div>
<script>
(function(){var K='tph_consent',x=document.getElementById('tphConsent');
 function g(){try{gtag('consent','update',{ad_storage:'granted',analytics_storage:'granted',ad_user_data:'granted',ad_personalization:'granted'});}catch(e){}
  try{fbq('consent','grant');}catch(e){}}
 var c=null;try{c=localStorage.getItem(K);}catch(e){}
 if(c==='granted'){g();}else if(c!=='denied'){if(x)x.classList.add('show');}
 var a=document.getElementById('tphAccept'),r=document.getElementById('tphReject');
 if(a)a.onclick=function(){g();try{localStorage.setItem(K,'granted');}catch(e){}x.classList.remove('show');};
 if(r)r.onclick=function(){try{localStorage.setItem(K,'denied');}catch(e){}x.classList.remove('show');};
})();
</script>
"""

def header(depth=0):
    root = "/" if depth == 0 else "/"
    return """<div class="ribbon">We deliver it, assemble it in your home and place it where you want it — <b>you settle only when you are happy</b></div>
<header>
  <div class="wrap nav">
    <a href="/" class="brand"><span class="brand-mark">%s</span><span class="name serif">The Plush <b>House</b></span></a>
    <nav class="nav-links">
      <a href="/corner-sofas.html" class="link">Corner</a>
      <a href="/u-shape-sofas.html" class="link">U-Shape</a>
      <a href="/l-shape-sofas.html" class="link">L-Shape</a>
      <a href="/2-and-3-seater-sofas.html" class="link">2 &amp; 3 Seater</a>
      <a href="/chesterfield-sofas.html" class="link">Chesterfield</a>
      <a class="btn btn-wa" href="https://wa.me/%s?text=%s">%s Order on WhatsApp</a>
    </nav>
  </div>
</header>""" % (EMBLEM, WA, "Hello%2C%20I%20would%20like%20to%20enquire%20about%20your%20sofas.", WA_IC)

def footer():
    return """<footer>
  <div class="wrap">
    <div class="fgrid">
      <div>
        <a href="/" class="brand"><span class="brand-mark">%s</span><span class="name serif">The Plush <b>House</b></span></a>
        <p>Handcrafted luxury sofas, delivered and assembled in your home across the United Kingdom &mdash; you settle only once it is in place and you are happy.</p>
      </div>
      <div class="fcol"><h4>Sofas</h4>
        <a href="/corner-sofas.html">Corner Sofas</a>
        <a href="/u-shape-sofas.html">U-Shape Sofas</a>
        <a href="/l-shape-sofas.html">L-Shape Sofas</a>
        <a href="/2-and-3-seater-sofas.html">2 &amp; 3 Seater Sets</a>
        <a href="/chesterfield-sofas.html">Chesterfield Sofas</a>
      </div>
      <div class="fcol"><h4>Get in touch</h4>
        <a href="https://wa.me/%s">WhatsApp us</a>
        <a href="mailto:%s">%s</a>
        <a href="/#faq">FAQ</a>
        <a href="/#how">How It Works</a>
      </div>
      <div class="fcol"><h4>Information</h4>
        <a href="/delivery.html">Delivery &amp; Assembly</a>
        <a href="/returns.html">Returns &amp; Refunds</a>
        <a href="/privacy.html">Privacy Policy</a>
        <a href="/terms.html">Terms &amp; Conditions</a>
      </div>
    </div>
    <div class="fbot">
      <span>&copy; 2026 The Plush House. All rights reserved.</span>
      <span>Delivered, assembled and placed in your home across the United Kingdom</span>
    </div>
  </div>
</footer>""" % (EMBLEM, WA, EMAIL, EMAIL)

INCLUDED = """<div class="incl">
  <div><div class="n serif">01</div><h4>We bring it in</h4><p>Our own team carries it into the room you have chosen &mdash; no courier, no kerbside drop.</p></div>
  <div><div class="n serif">02</div><h4>We assemble it</h4><p>Built in your home, so doorways and stairs are rarely a problem.</p></div>
  <div><div class="n serif">03</div><h4>We place it</h4><p>Positioned exactly where you want it, and the packaging leaves with us.</p></div>
  <div><div class="n serif">04</div><h4>You settle</h4><p>In cash, once it is standing there and you are happy. Not a penny before.</p></div>
</div>"""

def imgs(slug):
    """Actual numbered photos in the folder, in order. Numbering can have gaps."""
    d = os.path.join("images", slug)
    if not os.path.isdir(d): return []
    out = []
    for f in os.listdir(d):
        stem, ext = os.path.splitext(f)
        if ext.lower() in (".jpg", ".jpeg", ".png", ".webp") and stem.isdigit():
            out.append((int(stem), f))
    return [f for _, f in sorted(out)]

def shell(title, desc, canonical, body, extra_head="", extra_js=""):
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>%s</title>
<meta name="description" content="%s" />
<link rel="canonical" href="%s" />
<meta name="robots" content="index, follow" />
%s
<meta property="og:type" content="website" />
<meta property="og:site_name" content="The Plush House" />
<meta property="og:locale" content="en_GB" />
<meta property="og:url" content="%s" />
<meta property="og:title" content="%s" />
<meta property="og:description" content="%s" />
<meta name="twitter:card" content="summary_large_image" />
%s
%s
<style>%s</style>
%s
</head>
<body>
%s
%s
%s
%s
%s
</body>
</html>
""" % (title, desc, canonical, FAVICON, canonical, title, desc, FONTS, TRACK, CSS, extra_head,
       header(), body, footer(), CONSENT, extra_js)

CAT_NAME = {"corner":"Corner Sofas","ushape":"U-Shape Sofas","lshape":"L-Shape Sofas",
            "sets":"2 & 3 Seater Sofa Sets","chesterfield":"Chesterfield Sofas"}

ADDONS = [("Coffee Table","Panelled · inset glass top","images/accessories/coffeetable1.jpg",179),
          ("Ashton Coffee Table","Button tufted · glass top","images/accessories/ashton-coffee-table.jpg",179),
          ("Lilly Coffee Table","Fluted panels · glass top","images/accessories/lilly-coffee-table.jpg",179),
          ("Lilly Coffee Table \u2014 Charcoal","Fluted · deep charcoal velvet","images/accessories/lilly-coffee-table-charcoal.jpg",179),
          ("Chesterfield Coffee Table","Turned legs · brass caps","images/accessories/chesterfield-coffee-table.jpg",179),
          ("Ashton Stool","Square · chrome feet","images/accessories/ashton-stool.jpg",179),
          ("Chesterfield Stool","Generous square ottoman","images/accessories/chesterfield-stool.jpg",179),
          ("Round Ottoman Stool","Round · button tufted","images/accessories/round-ottoman-stool.jpg",179)]

def product_page(p):
    photos = imgs(p["slug"]) or ["1.jpg"]
    n = len(photos)
    cat = CATS[p["cat"]]; catname = CAT_NAME[p["cat"]]
    url = "%s/sofas/%s.html" % (SITE, p["url"])
    hero = "%s/images/%s/%s" % (SITE, p["slug"], photos[0])
    title = "%s Sofa | Made to Measure, Delivered &amp; Assembled — The Plush House" % p["name"]
    desc  = ("%s From £%s, made to your own measurements in any fabric or leather. "
             "We deliver, assemble and place it in your home — you settle only once you are happy."
             ) % (p["desc"].split(".")[0] + ".", p["price"])

    thumbs = "".join(
      '<button data-f="%s"%s><img src="/images/%s/%s" alt="%s sofa, view %d" loading="lazy"></button>'
      % (f, ' class="active"' if i==0 else '', p["slug"], f, p["name"], i+1)
      for i, f in enumerate(photos))

    # option list
    opts = ""
    if p.get("sets") or p.get("tiers"):
        opts += '<div class="bl">Choose your configuration</div>'
        first = True
        if p.get("setsFirst") and p.get("sets"):
            for lbl, pr, *sv in p["sets"]:
                save = '<span class="save">%s</span>' % sv[0] if sv else ""
                opts += '<div class="opt%s" data-price="%d" data-label="%s"><span class="l"><span class="radio"></span>%s%s</span><span class="p serif">£%d</span></div>' % (" active" if first else "", pr, lbl, lbl, save, pr)
                first = False
            if p.get("tiers"):
                opts += '<div class="divider">Or buy by the piece</div>'
                for lbl, pr in p["tiers"]:
                    opts += '<div class="opt" data-price="%d" data-label="%s"><span class="l"><span class="radio"></span>%s</span><span class="p serif">£%d</span></div>' % (pr, lbl, lbl, pr)
        else:
            for lbl, pr in p.get("tiers", []):
                opts += '<div class="opt%s" data-price="%d" data-label="%s"><span class="l"><span class="radio"></span>%s</span><span class="p serif">£%d</span></div>' % (" active" if first else "", pr, lbl, lbl, pr)
                first = False
            for lbl, pr, *sv in p.get("sets", []):
                save = '<span class="save">%s</span>' % sv[0] if sv else ""
                opts += '<div class="opt" data-price="%d" data-label="%s"><span class="l"><span class="radio"></span>%s%s</span><span class="p serif">£%d</span></div>' % (pr, lbl, lbl, save, pr)
        if p.get("setNote"):
            opts += '<div class="note">%s</div>' % p["setNote"]
        opts += '<div class="divider">Complete the room</div>'
    else:
        opts += '<div class="bl">Complete the room</div>'

    opts += '<div class="addon-wrap">'
    for nm, sb, img, pr in ADDONS:
        opts += ('<div class="addon" data-price="%d" data-label="%s"><span class="box"></span>'
                 '<img src="/%s" alt="%s" loading="lazy" decoding="async">'
                 '<span class="t">%s<small>%s</small></span><span class="p">+£%d</span></div>'
                 ) % (pr, nm, img, nm, nm, sb, pr)
    opts += '</div><div class="note">\u00a3199 on its own \u00b7 \u00a3179 with your sofa</div>'

    related = [q for q in PRODUCTS if q["cat"] == p["cat"] and q["slug"] != p["slug"]][:3]
    rel = "".join(
      '<a class="card" href="/sofas/%s.html"><div class="card-img"><img src="/images/%s/%s" alt="%s sofa" loading="lazy"></div>'
      '<div class="card-b"><h3 class="serif">%s</h3><p>%s</p>'
      '<div class="card-p serif">£%d<small>Delivered &amp; assembled</small></div></div></a>'
      % (q["url"], q["slug"], (imgs(q["slug"]) or ["1.jpg"])[0], q["name"], q["name"], q["desc"], q["price"]) for q in related)

    schema = {
      "@context":"https://schema.org","@type":"Product","name":p["name"]+" Sofa",
      "image":["%s/images/%s/%s" % (SITE,p["slug"],f) for f in photos[:4]],
      "description":p["long"],"brand":{"@type":"Brand","name":"The Plush House"},
      "category":catname,
      "offers":{"@type":"Offer","url":url,"priceCurrency":"GBP","price":str(p["price"]),
                "availability":"https://schema.org/InStock","itemCondition":"https://schema.org/NewCondition",
                "priceValidUntil":"2027-12-31",
                "seller":{"@type":"Organization","name":"The Plush House"},
                "shippingDetails":{"@type":"OfferShippingDetails",
                  "shippingRate":{"@type":"MonetaryAmount","value":"0","currency":"GBP"},
                  "shippingDestination":{"@type":"DefinedRegion","addressCountry":"GB"}}}}
    crumbs = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
      {"@type":"ListItem","position":1,"name":"Home","item":SITE+"/"},
      {"@type":"ListItem","position":2,"name":catname,"item":"%s/%s" % (SITE,cat["file"])},
      {"@type":"ListItem","position":3,"name":p["name"]+" Sofa","item":url}]}
    head = ('<link rel="preload" as="image" href="%s" fetchpriority="high">\n'
            '<meta property="og:image" content="%s" />\n<meta name="twitter:image" content="%s" />\n'
            '<script type="application/ld+json">%s</script>\n<script type="application/ld+json">%s</script>'
            ) % (hero, hero, hero, json.dumps(schema), json.dumps(crumbs))

    body = """
<div class="wrap">
  <div class="crumbs"><a href="/">Home</a><span>/</span><a href="/%s">%s</a><span>/</span>%s</div>
  <div class="pdp">
    <div>
      <div class="pgal-main"><img id="gmain" src="/images/%s/%s" alt="%s sofa" width="1200" height="900" fetchpriority="high" decoding="async"></div>
      <div class="pgal-thumbs" id="gthumbs">%s</div>
    </div>
    <div class="pbuy">
      <span class="eyebrow">%s</span>
      <h1 class="serif">%s Sofa</h1>
      <p class="sub">%s</p>
      <div class="pprice"><span id="ptotal">£%d</span><small id="plabel">Delivered, assembled and placed in your home</small></div>
      <div class="chips"><span>24&ndash;72hr delivery</span><span>Any fabric or leather</span><span>Made to your measurements</span><span>14-day returns</span></div>

      <div class="builder" id="builder">%s<div class="total"><span class="tl">Your total</span><span class="tv" id="ttl">£%d</span></div></div>

      <form class="oform" id="oform">
        <div class="bl">Your details</div>
        <div class="fld"><label for="f-name">Full name</label><input id="f-name" required></div>
        <div class="two">
          <div class="fld"><label for="f-phone">Phone number</label><input id="f-phone" type="tel" required></div>
          <div class="fld"><label for="f-post">Postcode</label><input id="f-post" required></div>
        </div>
        <div class="fld"><label for="f-addr">Delivery address</label><input id="f-addr" required></div>
        <div class="two">
          <div class="fld"><label for="f-town">Town / city</label><input id="f-town" required></div>
          <div class="fld"><label for="f-fab">Fabric / colour</label><input id="f-fab" placeholder="Not sure yet"></div>
        </div>
        <div class="fld"><label for="f-notes">Measurements or anything else</label><textarea id="f-notes" placeholder="Room size, custom dimensions, questions..."></textarea></div>
        <button type="submit" class="btn btn-wa" style="width:100%%">%s Send my order on WhatsApp</button>
      </form>

      <div class="pacts">
        <button class="btn btn-wa" id="placeBtn">%s Order now &mdash; no payment required</button>
        <a class="btn btn-ghost" id="askBtn" href="#" target="_blank" rel="noopener">Ask a question on WhatsApp</a>
      </div>
      <p class="cod">No payment now. Confirm on WhatsApp, our team delivers it within 24&ndash;72 hours, assembles it in your home and places it where you want it &mdash; and you settle in cash only once you are happy with it.</p>
    </div>
  </div>
</div>

<section class="sec alt">
  <div class="wrap">
    <h2 class="serif">About the %s</h2>
    <p>%s</p>
    <h3 class="serif">What happens when it arrives</h3>
    %s
  </div>
</section>

%s
""" % (cat["file"], catname, p["name"], p["slug"], photos[0], p["name"], thumbs,
       catname, p["name"], p["desc"], p["price"], opts, p["price"],
       WA_IC, WA_IC, p["name"], p["long"], INCLUDED,
       ('<section class="sec"><div class="wrap"><h2 class="serif">More from the %s collection</h2>'
        '<div class="grid" style="margin-top:28px">%s</div></div></section>' % (catname, rel)) if rel else "")

    js = """
<script>
(function(){
  var PRODUCT=%s, WA=%s, SLUG=%s, NIMG=%d;
  var base=%d, label=%s;
  var main=document.getElementById('gmain'), thumbs=document.getElementById('gthumbs');
  if(thumbs) thumbs.addEventListener('click',function(e){
    var b=e.target.closest('button'); if(!b) return;
    main.src='/images/'+SLUG+'/'+b.dataset.f;
    thumbs.querySelectorAll('button').forEach(function(x){x.classList.remove('active')});
    b.classList.add('active');
  });
  var box=document.getElementById('builder');
  function total(){
    var t=base;
    box.querySelectorAll('.addon.active').forEach(function(a){ t+=parseInt(a.dataset.price,10); });
    return t;
  }
  function paint(){
    var t=total();
    document.getElementById('ttl').textContent='£'+t;
    document.getElementById('ptotal').textContent='£'+t;
    document.getElementById('plabel').textContent=label+' · delivered, assembled and placed in your home';
    var extras=[]; box.querySelectorAll('.addon.active').forEach(function(a){ extras.push(a.dataset.label+' (+£'+a.dataset.price+')'); });
    var msg='Hi The Plush House! I would like to order the *'+PRODUCT+'* ('+label+' — £'+base+').';
    if(extras.length) msg+='\\nAdding: '+extras.join(', ');
    msg+='\\nTotal: £'+t;
    document.getElementById('askBtn').href='https://wa.me/'+WA+'?text='+encodeURIComponent('Hi The Plush House! I have a question about the *'+PRODUCT+'* sofa. Could you help me please?');
    window.__msg=msg; window.__total=t;
  }
  box.addEventListener('click',function(e){
    var o=e.target.closest('.opt');
    if(o){ box.querySelectorAll('.opt').forEach(function(x){x.classList.remove('active')}); o.classList.add('active');
           base=parseInt(o.dataset.price,10); label=o.dataset.label; paint(); return; }
    var a=e.target.closest('.addon');
    if(a){ a.classList.toggle('active'); paint(); }
  });
  paint();
  var form=document.getElementById('oform');
  document.getElementById('placeBtn').addEventListener('click',function(){
    if(!form.classList.contains('open')){
      form.classList.add('open');
      form.scrollIntoView({behavior:'smooth',block:'center'});
      try{ if(typeof fbq==='function') fbq('track','InitiateCheckout',{content_name:PRODUCT,value:window.__total,currency:'GBP'}); }catch(e){}
    } else { form.requestSubmit(); }
  });
  form.addEventListener('submit',function(e){
    e.preventDefault();
    var v=function(id){ return (document.getElementById(id).value||'').trim(); };
    var m=window.__msg;
    m+='\\n\\nName: '+v('f-name')+'\\nPhone: '+v('f-phone');
    m+='\\nAddress: '+v('f-addr')+', '+v('f-town')+', '+v('f-post');
    if(v('f-fab')) m+='\\nFabric / colour: '+v('f-fab');
    if(v('f-notes')) m+='\\nNotes: '+v('f-notes');
    m+='\\n\\nPayment: In cash, after you deliver, assemble & place it';
    try{ if(typeof fbq==='function') fbq('track','Lead',{content_name:PRODUCT,value:window.__total,currency:'GBP'}); }catch(e){}
    try{ if(typeof gtag==='function') gtag('event','generate_lead',{product:PRODUCT,value:window.__total,currency:'GBP'}); }catch(e){}
    window.open('https://wa.me/'+WA+'?text='+encodeURIComponent(m),'_blank','noopener');
  });
  try{ if(typeof fbq==='function') fbq('track','ViewContent',{content_name:PRODUCT,value:base,currency:'GBP'}); }catch(e){}
  try{ if(typeof gtag==='function') gtag('event','view_item',{product:PRODUCT,value:base,currency:'GBP'}); }catch(e){}
})();
</script>""" % (json.dumps(p["name"]), json.dumps(WA), json.dumps(p["slug"]), n, p["price"],
                json.dumps((p.get("sets") or p.get("tiers") or [["Standard", p["price"]]])[0][0]))

    return shell(title, desc, url, body, head, js)

def category_page(key):
    c = CATS[key]; items = [p for p in PRODUCTS if p["cat"] == key]
    url = "%s/%s" % (SITE, c["file"])
    hero = "%s/images/%s/%s" % (SITE, items[0]["slug"], (imgs(items[0]["slug"]) or ["1.jpg"])[0])
    cards = "".join(
      '<a class="card" href="/sofas/%s.html"><div class="card-img"><img src="/images/%s/%s" alt="%s sofa" loading="lazy"></div>'
      '<div class="card-b"><h3 class="serif">%s</h3><p>%s</p>'
      '<div class="card-p serif">£%d<small>Delivered &amp; assembled</small></div></div></a>'
      % (p["url"], p["slug"], (imgs(p["slug"]) or ["1.jpg"])[0], p["name"], p["name"], p["desc"], p["price"]) for p in items)

    blocks = "".join('<h3 class="serif">%s</h3><p>%s</p>' % (h, t) for h, t in c["body"])

    schema = {"@context":"https://schema.org","@type":"CollectionPage","name":c["h1"],
      "url":url,"description":c["desc"],
      "mainEntity":{"@type":"ItemList","itemListElement":[
        {"@type":"ListItem","position":i+1,"name":p["name"]+" Sofa",
         "url":"%s/sofas/%s.html" % (SITE,p["url"])} for i,p in enumerate(items)]}}
    crumbs = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
      {"@type":"ListItem","position":1,"name":"Home","item":SITE+"/"},
      {"@type":"ListItem","position":2,"name":c["h1"],"item":url}]}
    head = ('<meta property="og:image" content="%s" />\n<meta name="twitter:image" content="%s" />\n'
            '<script type="application/ld+json">%s</script>\n<script type="application/ld+json">%s</script>'
            ) % (hero, hero, json.dumps(schema), json.dumps(crumbs))

    body = """
<div class="wrap">
  <div class="crumbs"><a href="/">Home</a><span>/</span>%s</div>
</div>
<section class="sec" style="border-top:0;padding-top:34px">
  <div class="wrap">
    <span class="eyebrow">%s</span>
    <h1 class="serif">%s</h1>
    <p style="font-size:1.05rem">%s</p>
    <div class="grid" style="margin-top:40px">%s</div>
  </div>
</section>

<section class="sec alt">
  <div class="wrap">
    <h2 class="serif">What happens when it arrives</h2>
    %s
  </div>
</section>

<section class="sec">
  <div class="wrap-n">
    %s
    <p style="margin-top:26px"><a class="btn btn-wa" href="https://wa.me/%s?text=%s">%s Ask us about %s</a></p>
  </div>
</section>
""" % (c["h1"], c["eyebrow"], c["h1"], c["intro"], cards, INCLUDED, blocks, WA,
       "Hi%20The%20Plush%20House!%20I%27m%20looking%20at%20your%20" + c["h1"].replace(" ", "%20") + ".",
       WA_IC, c["h1"].lower())

    return shell(c["title"], c["desc"], url, body, head)


def sitemap():
    u = ['  <url><loc>%s/</loc><lastmod>%s</lastmod><changefreq>weekly</changefreq><priority>1.0</priority></url>' % (SITE, TODAY)]
    for k, c in CATS.items():
        u.append('  <url><loc>%s/%s</loc><lastmod>%s</lastmod><changefreq>weekly</changefreq><priority>0.9</priority></url>' % (SITE, c["file"], TODAY))
    for p in PRODUCTS:
        u.append('  <url><loc>%s/sofas/%s.html</loc><lastmod>%s</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>' % (SITE, p["url"], TODAY))
    for f, pr in [("delivery.html","0.5"),("returns.html","0.5"),("privacy.html","0.3"),("terms.html","0.3")]:
        u.append('  <url><loc>%s/%s</loc><lastmod>%s</lastmod><changefreq>yearly</changefreq><priority>%s</priority></url>' % (SITE, f, TODAY, pr))
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(u) + "\n</urlset>\n"


if __name__ == "__main__":
    os.makedirs("sofas", exist_ok=True)
    for p in PRODUCTS:
        with io.open("sofas/%s.html" % p["url"], "w", encoding="utf-8") as f:
            f.write(product_page(p))
        print("sofas/%s.html" % p["url"])
    for k in CATS:
        with io.open(CATS[k]["file"], "w", encoding="utf-8") as f:
            f.write(category_page(k))
        print(CATS[k]["file"])
    with io.open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(sitemap())
    print("sitemap.xml  (%d urls)" % (1 + len(CATS) + len(PRODUCTS) + 4))
