const sidebarTrigger = document.getElementById('sidebar-trigger');
const sidebar = document.getElementById('sidebar');
const sidebarOverlay = document.getElementById('sidebar-overlay')

sidebarTrigger.addEventListener('click', () => {
    sidebar.classList.toggle('active');
});

function collapseSidebar() {
    sidebar.classList.remove('active');
}

window.addEventListener('resize', () => {
    if (window.innerWidth < 1024) {
        collapseSidebar();
    } else if (window.innerWidth >= 1024) {
        sidebar.classList.add('active');
    }
});

window.addEventListener("load", () => {
    if (window.innerWidth < 1024) {
        collapseSidebar()
    } else if (window.innerWidth >= 1024) {
        sidebar.classList.add('active')
    }
    // collapseSidebar()
})

sidebarOverlay?.addEventListener('click', () => {
    collapseSidebar();
})