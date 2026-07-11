const header = document.querySelector("[data-header]");
const nav = document.querySelector("[data-nav]");
const navToggle = document.querySelector("[data-nav-toggle]");
const year = document.querySelector("[data-year]");

function syncHeaderState() {
  header.classList.toggle("is-scrolled", window.scrollY > 12);
}

navToggle.addEventListener("click", () => {
  const isOpen = nav.classList.toggle("is-open");
  header.classList.toggle("is-open", isOpen);
  navToggle.setAttribute("aria-expanded", String(isOpen));
});

nav.addEventListener("click", (event) => {
  if (event.target instanceof HTMLAnchorElement) {
    nav.classList.remove("is-open");
    header.classList.remove("is-open");
    navToggle.setAttribute("aria-expanded", "false");
  }
});

year.textContent = new Date().getFullYear();
syncHeaderState();
window.addEventListener("scroll", syncHeaderState, { passive: true });
