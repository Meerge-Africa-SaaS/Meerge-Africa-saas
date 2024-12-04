(() => {
    /**@type {HTMLDivElement} */
    const modal = document.getElementById('view-stock-item-modal');
    /**@type {HTMLButtonElement} */
    const cancelBtn = modal.querySelector('button.cancel');
    /**@type {HTMLButtonElement} */
    const addBtn = modal.querySelector('button.add');
    

    /**@type {HTMLDivElement} */
    const emailInput = document.getElementById("email-input")
    /**@type {HTMLDivElement} */
    const roleInput = document.getElementById("role-input")
    /**@type {HTMLTableCellElement} */
    const stock_id = document.getElementById("restaurant_stock_id")
    /**@type {HTMLDivElement} */
    const testdiv = document.getElementById("testdiv")

    cancelBtn?.addEventListener('click', () => {
        modal.classList.remove('active');
    })

    addBtn?.addEventListener('click', () => {
        modal.classList.remove('active')
    });

    

    
})();