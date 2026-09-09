/* =========================================================
   The Plush House — Google Analytics 4 (base loader only)
   Per-sofa events (view_item, whatsapp_click) are fired
   from inside index.html where the real product name is
   known. This file just loads GA4 + the homepage pageview.

   >>> ACTION REQUIRED <<<
   Replace G-XXXXXXXXXX below with The Plush House's own
   Measurement ID from Google Analytics (Admin -> Data
   streams). Do NOT reuse the UK Sofa Hub ID, or the two
   brands' data will mix.
   ========================================================= */

const GA_MEASUREMENT_ID = 'G-XXXXXXXXXX';   // The Plush House

(function () {
  var s = document.createElement('script');
  s.async = true;
  s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_MEASUREMENT_ID;
  document.head.appendChild(s);
})();
window.dataLayer = window.dataLayer || [];
function gtag() { dataLayer.push(arguments); }
gtag('js', new Date());
gtag('config', GA_MEASUREMENT_ID);
