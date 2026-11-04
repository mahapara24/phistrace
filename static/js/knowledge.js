const input = document.querySelector("#kb-filter");
const cards = [...document.querySelectorAll("[data-kb]")];
const empty = document.querySelector("#kb-empty");

if (input) {
  input.addEventListener("input", () => {
    const query = input.value.trim().toLowerCase();
    let shown = 0;
    for (const card of cards) {
      const match = !query || card.dataset.kb.includes(query);
      card.hidden = !match;
      if (match) shown += 1;
    }
    if (empty) empty.hidden = shown !== 0;
  });
}
