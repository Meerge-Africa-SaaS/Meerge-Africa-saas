const menuBtn = document.getElementById("menu-btn");
const menu = document.getElementById("menu");

menuBtn.addEventListener("click", () => {
  menu.classList.toggle("hidden");
});

window.addEventListener("scroll", function () {
  const nav = document.querySelector("nav");
  const links = document.querySelectorAll("nav a");
  if (window.scrollY > 50) {
    nav.classList.add("bg-white", "shadow-lg");
    links.forEach((link) => {
      link.classList.remove("text-white");
      link.classList.add("text-black");
    });
  } else {
    nav.classList.remove("bg-white", "shadow-lg");
    links.forEach((link) => {
      link.classList.remove("text-black");
      link.classList.add("text-white");
    });
  }
});
