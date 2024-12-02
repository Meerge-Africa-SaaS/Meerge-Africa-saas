(() => {
    /**@type {HTMLDivElement} */
    const modal = document.getElementById('add-stock-item-modal');
    /**@type {HTMLButtonElement} */
    const cancelBtn = modal.querySelector('button.cancel');
    /**@type {HTMLButtonElement} */
    const addBtn = modal.querySelector('button.add');
    /**@type {HTMLButtonElement} */
    const uploadFileBtn = modal.querySelector('button#upload-stock-item-image');

    /**@type {HTMLInputElement} */
    const stockItemImage = modal.querySelector('button#stock-item-image');
    //const stockItemImage = document.getElementById('stock-item-image');

    /**@type {HTMLFormElement} */
    const addStockItemForm = modal.querySelector('form#add-stock-item-form');

    /**@type {HTMLDivElement} */
    const emailInput = document.getElementById("email-input")
    /**@type {HTMLDivElement} */
    const roleInput = document.getElementById("role-input")

    cancelBtn?.addEventListener('click', () => {
        modal.classList.remove('active');
    })

    addBtn?.addEventListener('click', () => {
        modal.classList.remove('active')
    });

    uploadFileBtn?.addEventListener('click', () => {
        stockItemImage.click()
    })

    addStockItemForm?.addEventListener('submit', () => {
        //location.reload()
    }) 

    document.addEventListener("htmx:afterRequest", (event) => {
        response = JSON.parse(event.detail.xhr.responseText)
        if (response["status_code"] == 200){
            location.reload()
        }        
      })
    

})();