(function () {
  var script = document.currentScript;
  var targetId = script.getAttribute("data-target");
  var url = script.getAttribute("data-url");
  var target = document.getElementById(targetId);
  if (!target || !url) return;

  function refresh() {
    fetch(url, { cache: "no-store" })
      .then(function (res) {
        return res.ok ? res.text() : null;
      })
      .then(function (html) {
        if (html !== null) target.innerHTML = html;
      })
      .catch(function () {});
  }

  refresh();
  setInterval(refresh, 2000);
})();
