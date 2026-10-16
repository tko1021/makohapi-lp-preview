(() => {
  "use strict";
  window.dataLayer = window.dataLayer || [];
  const page = document.body.classList.contains("complete-page") ? "complete" : "lp";
  window.dataLayer.push({ event: "page_view_ready", page_type: page, measurement_mode: "preview_only" });
  document.querySelectorAll("[data-track]").forEach((element) => {
    element.addEventListener("click", () => {
      window.dataLayer.push({
        event: "cta_click",
        cta_id: element.dataset.track,
        page_type: page
      });
    });
  });
})();
