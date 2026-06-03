(function () {
  var measurementId = "G-YQE09MPX5H";
  var scriptLoaded = false;

  function cleanText(value) {
    return String(value || "")
      .replace(/\s+/g, " ")
      .trim()
      .slice(0, 120);
  }

  function getSiteArea() {
    return "logistics";
  }

  function loadScript() {
    if (scriptLoaded) return;
    var script = document.createElement("script");
    script.async = true;
    script.src =
      "https://www.googletagmanager.com/gtag/js?id=" +
      encodeURIComponent(measurementId);
    script.setAttribute("data-fa-ga4-loader", "true");
    document.head.appendChild(script);
    scriptLoaded = true;
  }

  function baseParams() {
    return {
      site_area: getSiteArea(),
      product_line: "fa_logistics",
      page_path: window.location.pathname + window.location.search,
      page_location: window.location.href,
      page_title: document.title,
    };
  }

  function cleanParams(params) {
    var cleaned = {};
    Object.keys(params || {}).forEach(function (key) {
      var value = params[key];
      if (value === undefined || value === null || value === "") return;
      cleaned[key] = value;
    });
    return cleaned;
  }

  function track(eventName, params) {
    if (!window.gtag) return;
    window.gtag(
      "event",
      eventName,
      cleanParams(Object.assign(baseParams(), params || {})),
    );
  }

  window.dataLayer = window.dataLayer || [];
  window.gtag =
    window.gtag ||
    function () {
      window.dataLayer.push(arguments);
    };

  window.gtag("consent", "default", {
    analytics_storage: "granted",
    ad_storage: "denied",
    ad_user_data: "denied",
    ad_personalization: "denied",
  });
  window.gtag("js", new Date());
  window.gtag("config", measurementId, { send_page_view: false });

  loadScript();
  track("page_view");

  document.addEventListener("click", function (event) {
    var target = event.target;
    var link = target && target.closest ? target.closest("a[href]") : null;
    if (!link) return;

    var url;
    try {
      url = new URL(link.href, window.location.href);
    } catch (error) {
      return;
    }

    var params = {
      link_url: url.href,
      link_text: cleanText(link.textContent || link.getAttribute("aria-label")),
      destination_host: url.hostname,
    };

    if (/wa\.me|wa\.link|whatsapp\.com/i.test(url.hostname)) {
      track("whatsapp_click", params);
      return;
    }

    if (
      url.hostname === "smm.fastaccs.com" ||
      url.pathname.indexOf("/smm") === 0
    ) {
      track("smm_entry_click", params);
      return;
    }

    if (url.hostname && url.hostname !== window.location.hostname) {
      track("outbound_click", params);
    }
  });
})();
