// Interior ERP Micro-Interactions & Premium Enhancements

// 1. Page Transitions
frappe.router.on('change', () => {
    // Fade in content on route change
    $('.layout-main-section').hide().fadeIn(300);
});

// 2. Confetti on Project Completion (Success trigger)
function triggerConfetti() {
    if (!window.confetti) {
        // Load canvas-confetti dynamically
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js';
        script.onload = () => {
            window.confetti({
                particleCount: 150,
                spread: 70,
                origin: { y: 0.6 },
                colors: ['#C8A97E', '#1F2937', '#FFFFFF']
            });
        };
        document.head.appendChild(script);
    } else {
        window.confetti({
            particleCount: 150,
            spread: 70,
            origin: { y: 0.6 },
            colors: ['#C8A97E', '#1F2937', '#FFFFFF']
        });
    }
}

// Global listener for "Completed" status in Proposal BOQ or Site Visit
$(document).on('page-change', function() {
    setTimeout(() => {
        if (frappe.get_route()[0] === 'Form') {
            const doc = cur_frm?.doc;
            if (doc && doc.status === 'Approved' && !doc._confetti_fired) {
                triggerConfetti();
                doc._confetti_fired = true;
            }
        }
    }, 500);
});

// 3. Skeleton Loaders (Injected before data load in List views)
frappe.listview_settings['Site Visit'] = {
    onload: function(listview) {
        listview.page.wrapper.addClass('loading-skeleton');
    },
    on_render: function(listview) {
        listview.page.wrapper.removeClass('loading-skeleton');
    }
};

frappe.listview_settings['Proposal BOQ'] = {
    onload: function(listview) {
        listview.page.wrapper.addClass('loading-skeleton');
    },
    on_render: function(listview) {
        listview.page.wrapper.removeClass('loading-skeleton');
    }
};

// 4. Custom Drag and Drop UI enhancement
$(document).on('dragover', function(e) {
    if ($('.file-upload').length) {
        $('.file-upload').addClass('drag-over-active');
    }
});
$(document).on('dragleave drop', function(e) {
    if ($('.file-upload').length) {
        $('.file-upload').removeClass('drag-over-active');
    }
});
