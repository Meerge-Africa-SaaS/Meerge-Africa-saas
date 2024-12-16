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

/**@type {HTMLInputElement} */
const menuToggle = document.querySelector('#menu-toggle > input[type=checkbox]')
const menuLinks = document.querySelectorAll('.mobile-menu-link')
const menu = document.getElementById('mobile-menu')
menuToggle.addEventListener('change', (ev) => {
  const isShown = menu.getAttribute('data-shown') === 'true'
  if (menuToggle.checked) {
    menu.setAttribute('data-shown', 'true')
  } else {
    menu.setAttribute('data-shown', 'false')
  }
})
menuLinks.forEach((link) => {
  link.addEventListener('click', () => {
    menu.setAttribute('data-shown', 'false')
  })
})