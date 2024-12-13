(() => {
    document.querySelectorAll('.modal').forEach(modal => {
        const modalHide = document.querySelectorAll(`[data-modal-hide="${modal.id}"]`)
        const modalTrigger = document.querySelectorAll(`[data-modal-trigger="${modal.id}"]`)
        const modalToggle = document.querySelectorAll(`[data-modal-toggle="${modal.id}"]`)
        const modalContent = modal.querySelector('.modal-content')

        modalTrigger.forEach(trigger => {
            trigger.addEventListener('click', () => {
                modal.classList.add('active')
                modal.scrollIntoView({ behavior: 'smooth' })
            })
        })

        modalToggle.forEach(toggle => {
            toggle.addEventListener('click', () => {
                modal.classList.toggle('active')
                if (modal.classList.contains('active')) {
                    modal.scrollIntoView({ behavior: 'smooth' })
                }
            })
        })

        modalHide.forEach(close => {
            close.addEventListener('click', () => {
                modal.classList.remove('active')
            })
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