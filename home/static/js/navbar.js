window.addEventListener('scroll', () => {
  const nav = document.querySelector('nav')
  if (window.scrollY > 50) {
    nav.classList.add("scrolled")
    document.querySelectorAll('nav a').forEach((link) => {
      link.classList.remove('text-white')
      link.classList.add('text-gray-800')
    })
  } else {
    nav.classList.remove("scrolled")
    document.querySelectorAll('nav a').forEach((link) => {
      link.classList.add('text-white')
      link.classList.remove('text-gray-800')
    })
  }
})

const menuBtn = document.getElementById('menu-btn')
const closeBtn = document.getElementById('close-menu-btn')
const menuLinks = document.querySelectorAll('.mobile-menu-link')
const menu = document.getElementById('mobile-menu')
menuBtn.addEventListener('click', () => {
  const isShown = menu.getAttribute('data-shown') === 'true'
  if (isShown) {
    menu.setAttribute('data-shown', 'false')
  } else {
    menu.setAttribute('data-shown', 'true')
  }
})
closeBtn.addEventListener('click', () => {
  menu.setAttribute('data-shown', 'false')
})
menuLinks.forEach((link) => {
  link.addEventListener('click', () => {
    menu.setAttribute('data-shown', 'false')
  })
})