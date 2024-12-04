(() => {
    /**@type {HTMLDivElement} */
    const modal = document.getElementById('create-store-modal');
    /**@type {HTMLButtonElement} */
    const cancelBtn = modal.querySelector('button.cancel');
    /**@type {HTMLButtonElement} */
    const addBtn = modal.querySelector('button.add');

    /**@type {HTMLDivElement} */
    /**@type {HTMLDivElement} */

    cancelBtn?.addEventListener('click', () => {
        modal.classList.remove('active');
    })
    addBtn?.addEventListener('click', () => {
        modal.classList.remove('active')
        location.reload()
    });
    

})();