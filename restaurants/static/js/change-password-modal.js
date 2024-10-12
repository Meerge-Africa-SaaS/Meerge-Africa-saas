(function () {
    /**@type {HTMLDivElement} */
    const modal = document.getElementById('change-password-modal')

    /**@type {HTMLElement} */
    const triggerBtn = document.querySelector('.change-password-trigger')
    /**@type {HTMLButtonElement} */
    const cancelBtn = modal.querySelector('button.cancel')
    /**@type {HTMLButtonElement} */
    const updateBtn = modal.querySelector('button.update')


    /**@type {HTMLDivElement} */
    const currentPassworContainer = document.getElementById('current-password-container')
    /**@type {HTMLDivElement} */
    const currentPasswordInput = document.getElementById('current-password-input')
    /**@type {HTMLInputElement} */
    const currentPassword = currentPasswordInput.querySelector('input')

    /**@type {HTMLDivElement} */
    const newPasswordContainer = document.getElementById('new-password-container')
    /**@type {HTMLDivElement} */
    const newPasswordInput = document.getElementById('new-password-input')
    /**@type {HTMLInputElement} */
    const newPassword = newPasswordInput.querySelector('input')
    /**@type {HTMLDivElement} */
    const confirmPasswordInput = document.getElementById('confirm-password-input')
    /**@type {HTMLInputElement} */
    const confirmPassword = confirmPasswordInput.querySelector('input')

    triggerBtn?.addEventListener('click', () => {
        modal.classList.remove('hidden')
        modal.classList.add('flex')
    })

    cancelBtn?.addEventListener('click', () => {
        modal.classList.add('hidden')
        modal.classList.remove('flex')
    })

    updateBtn?.addEventListener('click', () => {
        modal.classList.add('hidden')
        modal.classList.remove('flex')
    });

    currentPassword.addEventListener('input', debounce(() => {
        const loader = currentPasswordInput.querySelector('svg')
        loader.classList.remove('hidden')
        currentPassword.setCustomValidity('')
        setTimeout(() => {
            if (currentPassword.value === 'password') {
                currentPassword.setCustomValidity('')
                loader.classList.add('hidden')
                newPasswordContainer.classList.remove('hidden')
            } else {
                currentPassword.setCustomValidity('Password is incorrect')
                newPasswordContainer.classList.add('hidden')
            }
            loader.classList.add('hidden')
        }, 2000)
    }, 500))

    function checkPasswordMatch() {
        if (newPassword.value !== confirmPassword.value) {
            confirmPassword.setCustomValidity('Passwords do not match')
        } else {
            confirmPassword.setCustomValidity('')
        }
        // check if newPassord is valid
        if (currentPassword.checkValidity() && newPassword.checkValidity() && confirmPassword.checkValidity()) {
            updateBtn.removeAttribute('disabled')
        } else {
            updateBtn.setAttribute('disabled', 'disabled')
        }
    }

    function validatePassword() {
        const value = newPassword.value
        if (value.length < 8) {
            newPassword.setCustomValidity('Password must be at least 8 characters')
        } else if (value.length > 64) {
            newPassword.setCustomValidity('Password must be at most 64 characters')
        } else if (!/[a-z]/.test(value)) {
            newPassword.setCustomValidity('Password must contain at least one lowercase letter')
        } else if (!/[A-Z]/.test(value)) {
            newPassword.setCustomValidity('Password must contain at least one uppercase letter')
        } else if (!/[0-9]/.test(value)) {
            newPassword.setCustomValidity('Password must contain at least one digit')
        } else if (!/[^a-zA-Z0-9]/.test(value)) {
            newPassword.setCustomValidity('Password must contain at least one special character')
        } else {
            newPassword.setCustomValidity('')
        }
        // check if newPassord is valid
        if (currentPassword.checkValidity() && newPassword.checkValidity() && confirmPassword.checkValidity()) {
            updateBtn.removeAttribute('disabled')
        } else {
            updateBtn.setAttribute('disabled', 'disabled')
        }
    }

    newPassword.addEventListener('input', debounce(validatePassword, 500));
    newPassword.addEventListener('input', debounce(checkPasswordMatch, 500));
    confirmPassword.addEventListener('input', debounce(checkPasswordMatch, 500));
})()