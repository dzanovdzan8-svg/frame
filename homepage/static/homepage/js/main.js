// Текущий год в подвале страницы
const yearElement = document.getElementById("current-year");

if (yearElement) {
    yearElement.textContent = new Date().getFullYear();
}

// Подсветка пункта навигации, соответствующего текущему разделу
const currentPath = window.location.pathname;

document.querySelectorAll(".site-nav .nav-link").forEach((link) => {
    const href = link.getAttribute("href");
    const isHome = href === "/" && currentPath === "/";
    const isSection = href !== "/" && currentPath.startsWith(href);

    if (isHome || isSection) {
        link.classList.add("active");
    }
});
