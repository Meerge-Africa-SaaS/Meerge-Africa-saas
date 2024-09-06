const modal = document.getElementById('deactivate-account-modal')
const triggerBtn = document.querySelector('.deactivate-account-trigger')
const cancelBtn = modal.querySelectorAll('button.cancel')
const proceedBtn = modal.querySelector('button.proceed')
const deactivateBtn = modal.querySelector('button.deactivate')
const step1 = modal.querySelector('.step-1')
const step2 = modal.querySelector('.step-2')
const passwordInput = modal.querySelector('.password-input')
const passwordInputField = passwordInput.querySelector('input')

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

passwordInputField.addEventListener(
    'input',
    debounce(() => {
        const loader = passwordInput.querySelector('svg')
        loader.classList.remove('hidden')
        setTimeout(() => {
            if (passwordInputField.value === 'password') {
                passwordInputField.setCustomValidity('')
                loader.classList.add('hidden')
                deactivateBtn.attributes.removeNamedItem('disabled')
            } else {
                passwordInputField.setCustomValidity('Password is incorrect')
                deactivateBtn.setAttribute('disabled', true)
            }
            loader.classList.add('hidden')
        }, 2000)
    }, 500)
)

triggerBtn.addEventListener('click', () => {
    modal.classList.remove('hidden')
    modal.classList.add('flex')
})

cancelBtn.forEach((btn) => {
    btn.addEventListener('click', () => {
        modal.classList.add('hidden')
        modal.classList.remove('flex')
    })
})

proceedBtn.addEventListener('click', () => {
    step1.classList.add('hidden')
    step2.classList.remove('hidden')
})

deactivateBtn.addEventListener('click', () => {
    modal.classList.add('hidden')
    modal.classList.remove('flex')
})