// Main JavaScript for AdTrack Investor Portal

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Initialize Bootstrap popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl)
    });

    // Page view tracking
    const trackPageView = () => {
        // This is a placeholder for actual tracking
        // In a real implementation, this would send data to the server
        console.log('Page view tracked:', window.location.pathname);
        
        // Start timer for time spent on page
        window.pageViewStartTime = new Date();
    };

    // Track time spent on page before leaving
    window.addEventListener('beforeunload', function() {
        if (window.pageViewStartTime) {
            const timeSpent = Math.round((new Date() - window.pageViewStartTime) / 1000);
            console.log('Time spent on page:', timeSpent, 'seconds');
            
            // In a real implementation, this would send data to the server
            // using navigator.sendBeacon to ensure the data is sent even when the page is unloading
            // navigator.sendBeacon('/track-time-spent', JSON.stringify({ timeSpent: timeSpent }));
        }
    });

    // Track initial page view
    trackPageView();

    // Prevent right-click on content to discourage saving
    document.addEventListener('contextmenu', function(e) {
        if (!e.target.closest('a')) {
            e.preventDefault();
            return false;
        }
    });

    // Disable keyboard shortcuts for saving/printing
    document.addEventListener('keydown', function(e) {
        // Ctrl+S, Ctrl+P, Ctrl+Shift+S
        if ((e.ctrlKey && (e.key === 's' || e.key === 'p')) || 
            (e.ctrlKey && e.shiftKey && e.key === 's')) {
            e.preventDefault();
            return false;
        }
    });

    // Handle form submissions with validation
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
});
