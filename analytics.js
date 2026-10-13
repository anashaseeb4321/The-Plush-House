/* =========================================================
   The Plush House — Google Analytics 4 (base loader only)
   Per-sofa events (view_item, whatsapp_click) are fired
   from inside the pages where the real product name is
   known. This file just loads GA4 + the pageview.

   Measurement ID = stream "my site" (theplushhouse.co.uk)
   in the THE PLUSH HOUSE property. Kept separate from
   Sofa Stitch so the two brands' data never mix.

   gtag.js (~150 KB) is fetched only after the page has
   painted — see window.__tphLater in the page head. The
   config call below is queued in dataLayer and replayed
   when it arrives, so nothing is lost.
   ========================================================= */

const GA_MEASUREMENT_ID = 'G-GWFCTTV6ED';   // The Plush House — "my site" stream

window.dataLayer = window.dataLayer || [];
function gtag() { dataLayer.push(arguments); }
gtag('js', new Date());
gtag('config', GA_MEASUREMENT_ID);

(window.__tphLater || function (f) { f(); })(function () {
  var s = document.createElement('script');
  s.async = true;
  s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_MEASUREMENT_ID;
  document.head.appendChild(s);
});
