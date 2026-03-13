// UI helpers shared across instrument pages
// - sidebar toggle
// - mobile hamburger navigation

function initUI() {
    // hamburger nav for small screens
    const navBtn = document.querySelector('.site-nav__hamburger');
    const navOverlay = document.querySelector('.site-nav__overlay');
    const navClose = document.querySelector('.site-nav__close');
    
    if (navBtn && navOverlay) {
        navBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            navOverlay.classList.toggle('open');
        });
        
        navOverlay.addEventListener('click', (e) => {
            if (e.target === navOverlay) {
                navOverlay.classList.remove('open');
            }
        });
    }
    
    if (navClose && navOverlay) {
        navClose.addEventListener('click', (e) => {
            e.stopPropagation();
            navOverlay.classList.remove('open');
        });
    }

    // sidebar filters toggle
    const sidebarToggle = document.querySelector('.sidebar-toggle');
    const sidebar = document.querySelector('.sidebar');
    const sidebarOverlay = document.querySelector('.sidebar-overlay');
    const sidebarCloseBtn = document.querySelector('.sidebar-close-btn');
    
    if (sidebarToggle && sidebar) {
        // Set initial state
        if (!sidebar.classList.contains('closed')) {
            sidebar.classList.add('closed');
        }
        sidebarToggle.classList.remove('hidden');
        sidebarOverlay?.classList.remove('visible');

        // Toggle button click
        sidebarToggle.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            const isClosed = sidebar.classList.contains('closed');
            if (isClosed) {
                sidebar.classList.remove('closed');
                sidebarToggle.classList.add('hidden');
                sidebarOverlay?.classList.add('visible');
            } else {
                sidebar.classList.add('closed');
                sidebarToggle.classList.remove('hidden');
                sidebarOverlay?.classList.remove('visible');
            }
        });

        // Overlay click
        if (sidebarOverlay) {
            sidebarOverlay.addEventListener('click', (e) => {
                sidebar.classList.add('closed');
                sidebarToggle.classList.remove('hidden');
                sidebarOverlay.classList.remove('visible');
            });
        }

        // Close button click
        if (sidebarCloseBtn) {
            sidebarCloseBtn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                sidebar.classList.add('closed');
                sidebarToggle.classList.remove('hidden');
                sidebarOverlay?.classList.remove('visible');
            });
        }
    }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initUI);
} else {
    initUI();
}
