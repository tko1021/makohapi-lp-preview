(() => {
  "use strict";
  // ---- 計測の設定（2026-10-20）----
  // GA4 の測定ID（例 "G-XXXXXXXXXX"）。空のままなら何も送らない（dataLayer に積むだけ＝従来どおり）。
  // 【空のまま】値は本人が GA4 管理画面 → データストリーム → ウェブ で発行してここに入れる。
  const GA4_ID = "";

  window.dataLayer = window.dataLayer || [];
  const page = document.body.classList.contains("complete-page") ? "complete" : "lp";
  const live = /^G-[A-Z0-9]{6,}$/.test(GA4_ID);

  // 流入元パラメータ（utm_source 等）を、最初に来たときだけ覚える（同じ閲覧中は上書きしない）
  const utm = {};
  try {
    const q = new URLSearchParams(location.search);
    ["utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term"].forEach((k) => {
      const v = q.get(k);
      if (v) utm[k] = v;
    });
    if (Object.keys(utm).length) sessionStorage.setItem("mh_utm", JSON.stringify(utm));
    else Object.assign(utm, JSON.parse(sessionStorage.getItem("mh_utm") || "{}"));
  } catch (e) { /* 保存できない環境では何もしない */ }

  if (live) {
    const s = document.createElement("script");
    s.async = true;
    s.src = "https://www.googletagmanager.com/gtag/js?id=" + GA4_ID;
    document.head.appendChild(s);
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag("js", new Date());
    window.gtag("config", GA4_ID, { page_type: page });
  }

  const send = (name, params) => {
    const p = Object.assign({ page_type: page, measurement_mode: live ? "ga4" : "preview_only" }, utm, params || {});
    if (live) window.gtag("event", name, p);
    else window.dataLayer.push(Object.assign({ event: name }, p));
  };

  send("page_view_ready");
  document.querySelectorAll("[data-track]").forEach((element) => {
    element.addEventListener("click", () => send("cta_click", { cta_id: element.dataset.track }));
  });
})();
