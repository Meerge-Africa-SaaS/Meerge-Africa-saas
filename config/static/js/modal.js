(() => {
    document.querySelectorAll('.modal').forEach(modal => {
        const triggerBtn = document.querySelector(`[data-modal-trigger="${modal.id}"]`)
        const modalContent = modal.querySelector('.modal-content')

        triggerBtn?.addEventListener('click', () => {
            modal.classList.add('active')
        })

        modalContent?.addEventListener('click', e => {
            e.stopPropagation()
        })

        modal?.addEventListener('click', () => {
            modal.classList.remove('active')
        })

        modal.querySelector('.close')?.addEventListener('click', () => {
            modal.classList.remove('active')
        })
    });

})()