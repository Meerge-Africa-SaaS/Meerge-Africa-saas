(() => {
    /**@type {HTMLDivElement} */
    const addEmployeeModal = document.getElementById('add-employee-modal');
    /**@type {HTMLButtonElement} */
    const cancelBtn = addEmployeeModal.querySelector('button.cancel');
    /**@type {HTMLButtonElement} */
    const addBtn = addEmployeeModal.querySelector('button.add');

    /**@type {HTMLDivElement} */
    const emailInput = document.getElementById("email-input")
    /**@type {HTMLDivElement} */
    const roleInput = document.getElementById("role-input")

    cancelBtn?.addEventListener('click', () => {
        addEmployeeModal.classList.remove('active')
    })

    addBtn?.addEventListener('click', () => {
        addEmployeeModal.classList.remove('active')
    });
})();