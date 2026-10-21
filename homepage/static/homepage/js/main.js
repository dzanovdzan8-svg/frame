// Текущий год в подвале страницы
const yearElement = document.getElementById("current-year");

if (yearElement) {
    yearElement.textContent = new Date().getFullYear();
}

// Подсветка пункта навигации: выбирается самый длинный подходящий адрес,
// чтобы /notes/statistics/ не подсвечивал одновременно «Заметки»
const currentPath = window.location.pathname;
const links = Array.from(document.querySelectorAll(".site-nav .nav-link"));

let best = null;

links.forEach((link) => {
    const href = link.getAttribute("href");
    const matches = href === "/"
        ? currentPath === "/"
        : currentPath.startsWith(href);

    if (matches && (best === null
        || href.length > best.getAttribute("href").length)) {
        best = link;
    }
});

if (best) {
    best.classList.add("active");
}
