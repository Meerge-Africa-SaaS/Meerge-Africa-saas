(() => {
    /**@type {HTMLDivElement} */
    const modal = document.getElementById('view-or-deactivate-stock-item-modal');
    /**@type {HTMLButtonElement} */
    const viewBtn = modal.querySelector('button#view');
    /**@type {HTMLButtonElement} */
    const deactivateBtn = modal.querySelector('button#deactivate');
    

    cancelBtn?.addEventListener('click', () => {
        modal.classList.remove('active');
    })

    addBtn?.addEventListener('click', () => {
        modal.classList.remove('active')
    });

})();