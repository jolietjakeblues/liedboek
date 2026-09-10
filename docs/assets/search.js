(() => {
  const input = document.getElementById("song-search");
  const items = [...document.querySelectorAll("#song-list .song-list-item")];
  const groups = [...document.querySelectorAll("#song-list .song-group")];
  const buttons = [...document.querySelectorAll(".song-filters .filter")];
  const empty = document.getElementById("song-empty");

  if (!input || !items.length) return;

  let activeFilter = "all";

  const matchesFilter = (item) => {
    if (activeFilter === "all") return true;
    if (activeFilter === "chords") return item.dataset.chords === "true";
    return item.dataset.language === activeFilter;
  };

  const update = () => {
    const q = input.value.trim().toLowerCase();
    let visibleCount = 0;

    items.forEach((item) => {
      const haystack = `${item.dataset.title} ${item.dataset.tags}`.toLowerCase();
      const visible = (!q || haystack.includes(q)) && matchesFilter(item);
      item.hidden = !visible;
      if (visible) visibleCount += 1;
    });

    groups.forEach((group) => {
      const hasVisibleItems = [...group.querySelectorAll(".song-list-item")]
        .some((item) => !item.hidden);
      group.hidden = !hasVisibleItems;
    });

    if (empty) empty.hidden = visibleCount !== 0;
  };

  buttons.forEach((button) => {
    button.addEventListener("click", () => {
      activeFilter = button.dataset.filter || "all";
      buttons.forEach((candidate) => {
        const active = candidate === button;
        candidate.classList.toggle("is-active", active);
        candidate.setAttribute("aria-pressed", active ? "true" : "false");
      });
      update();
    });
  });

  input.addEventListener("input", update);
  update();
})();
