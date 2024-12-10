class SearchableMultiselect {
    /**
     * 
     * @param {HTMLDivElement} element 
     */
    constructor(element) {
        this.wrapper = element;
        this.originalSelect = element.querySelector('select');
        this.searchInput = element.querySelector('[data-multiselect-search]');
        this.dropdown = element.querySelector('[data-multiselect-dropdown]');
        this.optionsContainer = element.querySelector('[data-multiselect-options]');
        this.selectedContainer = element.querySelector('[data-multiselect-selected]');
        this.emptyMessage = element.querySelector('[data-multiselect-empty]');
        this.createEvent = element.attributes['data-multiselect-create-event']?.value;
        this.searchResultsEvent = element.attributes['data-multiselect-search-results-event']?.value;
        
        this.options = this.getOptions();
        this.selectedValues = new Set();
        
        this.setupEventListeners();
        this.initializeSelection();
    }
    
    getOptions() {
        return Array.from(this.originalSelect.options).map(option => ({
            value: option.value,
            label: option.text,
            selected: option.selected
        }));
    }
    
    initializeSelection() {
        // Initialize selected values from original select
        Array.from(this.originalSelect.selectedOptions).forEach(option => {
            this.selectedValues.add(option.value);
            this.addSelectedItem(option.value, option.text);
        });
    }
    
    setupEventListeners() {
        // Toggle dropdown
        this.wrapper.querySelector('[data-multiselect-toggle]').addEventListener('click', () => {
            this.toggleDropdown();
        });

        this.wrapper.addEventListener(this.searchResultsEvent, (e) => {
            this.options = e.detail.options;
        });

        this.wrapper.addEventListener(this.createEvent, (e) => {
            this.options.push(e.detail.option);
        });


        this.searchInput.addEventListener('focus', () => {
            this.showDropdown();
        });
        
        // Search functionality
        this.searchInput.addEventListener('input', () => {
            this.handleSearch();
        });
        
        // Close dropdown when clicking outside
        document.addEventListener('click', (e) => {
            if (!this.wrapper.contains(e.target)) {
                this.hideDropdown();
            }
        });
        
        // Option selection
        this.optionsContainer.addEventListener('click', (e) => {
            const option = e.target.closest('[data-multiselect-option]');
            if (option) {
                this.handleOptionSelect(option);
            }
        });
        
        // Remove selected item
        this.selectedContainer.addEventListener('click', (e) => {
            const removeButton = e.target.closest('[data-multiselect-remove]');
            if (removeButton) {
                const item = removeButton.closest('[data-value]');
                this.removeSelectedItem(item.dataset.value);
            }
        });
        
        // Edit selected item
        this.selectedContainer.addEventListener('click', (e) => {
            const editButton = e.target.closest('[data-multiselect-edit]');
            if (editButton) {
                const item = editButton.closest('[data-value]');
                this.handleEdit(item.dataset.value);
            }
        });
        
        // Create new item
        this.wrapper.querySelector('[data-multiselect-create]')?.addEventListener('click', () => {
            this.handleCreate();
        });
    }
    
    toggleDropdown() {
        if (this.dropdown.classList.contains('hidden')) {
            this.showDropdown();
        } else {
            this.hideDropdown();
        }
    }
    
    showDropdown() {
        this.dropdown.classList.remove('hidden');
        this.searchInput.focus();
    }
    
    hideDropdown() {
        this.dropdown.classList.add('hidden');
        this.searchInput.value = '';
        this.handleSearch(); // Reset search results
    }
    
    handleSearch() {
        const searchTerm = this.searchInput.value.toLowerCase();
        let hasResults = false;
        
        // Filter options
        this.options.forEach(option => {
            const optionElement = this.optionsContainer.querySelector(`[data-value="${option.value}"]`);
            if (!optionElement) return;
            
            const matches = option.label.toLowerCase().includes(searchTerm);
            const isVisible = matches && !this.selectedValues.has(option.value);
            
            optionElement.classList.toggle('hidden', !isVisible);
            if (isVisible) hasResults = true;
        });
        
        // Toggle empty message
        this.emptyMessage.classList.toggle('hidden', hasResults);
    }
    
    handleOptionSelect(optionElement) {
        const value = optionElement.dataset.value;
        const label = optionElement.textContent.trim();
        
        this.selectedValues.add(value);
        this.addSelectedItem(value, label);
        this.updateOriginalSelect();
        // this.hideDropdown();
        this.handleSearch(); // Reset search results
    }
    
    addSelectedItem(value, label) {
        const itemHtml = `
            <div class="inline-flex items-center bg-slate-50 text-primary rounded-md px-3 py-1 text-sm m-1" data-value="${value}">
                <span>${label}</span>
                <button type="button" class="ml-1 !p-0 no-ring no-outline no-shadow text-blue-400 hover:text-blue-600" data-multiselect-edit>
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"/>
                    </svg>
                </button>
                <button type="button" class="ml-1 !p-0 no-ring no-outline no-shadow text-red-400 hover:text-red-600" data-multiselect-remove>
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                    </svg>
                </button>
            </div>
        `;
        this.selectedContainer.insertAdjacentHTML('beforeend', itemHtml);
    }
    
    removeSelectedItem(value) {
        const item = this.selectedContainer.querySelector(`[data-value="${value}"]`);
        if (item) {
            item.remove();
            this.selectedValues.delete(value);
            this.updateOriginalSelect();
            this.handleSearch(); // Reset search results
        }
    }
    
    updateOriginalSelect() {
        Array.from(this.originalSelect.options).forEach(option => {
            option.selected = this.selectedValues.has(option.value);
        });
        
        // Dispatch change event
        this.originalSelect.dispatchEvent(new Event('change'));
    }
    
    handleEdit(value) {
        // Implement your edit modal/form logic here
        console.log('Edit item:', value);
        // Example: you might want to emit a custom event
        const event = new CustomEvent('multiselect-edit', {
            detail: { value }
        });
        this.wrapper.dispatchEvent(event);
    }
    
    handleCreate() {
        // Implement your create modal/form logic here
        const searchTerm = this.searchInput.value;
        console.log('Create new item with term:', searchTerm);
        // Example: you might want to emit a custom event
        const event = new CustomEvent('multiselect-create', {
            detail: { searchTerm }
        });
        this.wrapper.dispatchEvent(event);
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[data-multiselect]').forEach(element => {
        new SearchableMultiselect(element);
    });
});

// Example usage of edit and create events
document.querySelector('[data-multiselect]').addEventListener('multiselect-edit', (e) => {
    const value = e.detail.value;
    // Open your edit modal here
    console.log('Opening edit modal for value:', value);
});

document.querySelector('[data-multiselect]').addEventListener('multiselect-create', (e) => {
    const searchTerm = e.detail.searchTerm;
    // Open your create modal here
    console.log('Opening create modal with term:', searchTerm);
});