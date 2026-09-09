(() => {
  const input = document.getElementById("song-search");
  const items = [...document.querySelectorAll("#song-list li")];
  if (!input) return;

  input.addEventListener("input", () => {
    const q = input.value.trim().toLowerCase();
    items.forEach((item) => {
      item.hidden = q && !item.dataset.title.includes(q);
    });
  });
})();
