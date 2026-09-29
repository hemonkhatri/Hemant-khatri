// Small enhancements only — every page works without JavaScript.

// Dismiss flash messages when clicked.
document.querySelectorAll(".flash-item").forEach(function (item) {
  item.addEventListener("click", function () {
    item.remove();
  });
});

// Fill the skill meters once, after load, so the numbers land rather than crawl.
const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
if (!reduced) {
  document.querySelectorAll(".meter-fill").forEach(function (fill) {
    const target = fill.style.width;
    fill.style.width = "0%";
    requestAnimationFrame(function () {
      fill.style.transition = "width 700ms cubic-bezier(.2,.7,.3,1)";
      fill.style.width = target;
    });
  });
}
