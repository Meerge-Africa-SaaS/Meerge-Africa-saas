(() => {
    /**@type {HTMLDivElement} */
    const modal = document.getElementById('add-employee-modal');
    /**@type {HTMLButtonElement} */
    const cancelBtn = modal.querySelector('button.cancel');
    /**@type {HTMLButtonElement} */
    const addBtn = modal.querySelector('button.add');

    /**@type {HTMLDivElement} */
    const emailInput = document.getElementById("email-input")
    /**@type {HTMLDivElement} */
    const roleInput = document.getElementById("role-input")

    cancelBtn?.addEventListener('click', () => {
        modal.classList.remove('active')
    })

    addBtn?.addEventListener('click', () => {
        modal.classList.remove('active')
    });
})();