/**
 * 
 * @param {HTMLElement} element 
 */
function togglePasswordVisibility(element) {
    // find the closest parent element with class "password-input-group"
    const passwordInput = element.closest(".password-input-group").querySelector("input");
    if (passwordInput.type === "password") {
        passwordInput.type = "text";
    }
    else {
        passwordInput.type = "password";
    }
    // set data-visible attribute to the opposite of its current value
    element.setAttribute("data-visible", element.getAttribute("data-visible") === "false");
}

/**
 * Debounce function
 * @param {(...args: T[]) => void} func
 * @param {number} timeout 
 * @returns {(...args: T[]) => void}
 */
function debounce(func, timeout = 300) {
    let timer
    return (...args) => {
        clearTimeout(timer)
        timer = setTimeout(() => {
            timer = null
            func(...args)
        }, timeout)
    }
}