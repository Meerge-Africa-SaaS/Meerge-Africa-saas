const menuBtn = document.getElementById("menu-btn");
const menu = document.getElementById("menu");

menuBtn.addEventListener("click", () => {
  const nav = document.querySelector("nav");
  menu.classList.toggle("hidden");
  nav.classList.toggle("bg-white");
  this.classList.toggle("text-black");
});

window.addEventListener("scroll", function () {
  const nav = document.querySelector("nav");
  const links = document.querySelectorAll("nav a");
  const button = document.querySelector("nav button");
  if (window.scrollY > 50) {
    nav.classList.add("bg-white", "shadow-lg");
  } else {
    nav.classList.remove("bg-white", "shadow-lg");
  }
});
