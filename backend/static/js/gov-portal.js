// Government Portal - Enhanced Features JavaScript

document.addEventListener('DOMContentLoaded', function() {
    
    // ===== Accessibility Controls =====
    const accessibilityToggle = document.getElementById('accessibility-toggle');
    const accessibilityPanel = document.getElementById('accessibility-panel');
    const textSizeButtons = document.querySelectorAll('.text-size-btn');
    const darkModeToggle = document.getElementById('dark-mode-toggle');
    
    // Toggle accessibility panel
    if (accessibilityToggle) {
        accessibilityToggle.addEventListener('click', function() {
            accessibilityPanel.style.display = accessibilityPanel.style.display === 'none' ? 'block' : 'none';
        });
    }
    
    // Text size controls
    textSizeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const size = this.dataset.size;
            textSizeButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            let fontSize = '1rem';
            switch(size) {
                case 'small': fontSize = '0.9rem'; break;
                case 'large': fontSize = '1.1rem'; break;
                case 'normal': fontSize = '1rem'; break;
            }
            
            document.body.style.fontSize = fontSize;
            localStorage.setItem('textSize', size);
        });
    });
    
    // Dark mode toggle
    if (darkModeToggle) {
        // Check for saved dark mode preference
        if (localStorage.getItem('darkMode') === 'true') {
            document.body.classList.add('dark-mode');
            darkModeToggle.checked = true;
        }
        
        darkModeToggle.addEventListener('change', function() {
            document.body.classList.toggle('dark-mode');
            localStorage.setItem('darkMode', this.checked);
        });
    }
    
    // Restore saved text size preference
    const savedTextSize = localStorage.getItem('textSize');
    if (savedTextSize) {
        const btn = document.querySelector(`[data-size="${savedTextSize}"]`);
        if (btn) btn.click();
    }
    
    // ===== Animations =====
    // Animate stat cards on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-slide-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe all stat cards
    document.querySelectorAll('.stat-card-enhanced').forEach(card => {
        observer.observe(card);
    });
    
    // ===== Form Enhancements =====
    // Character count for textareas
    const textareas = document.querySelectorAll('textarea[maxlength]');
    textareas.forEach(textarea => {
        const maxLength = textarea.getAttribute('maxlength');
        
        // Create char count element
        const charCount = document.createElement('div');
        charCount.className = 'char-count';
        charCount.textContent = `0/${maxLength}`;
        textarea.parentNode.insertBefore(charCount, textarea.nextSibling);
        
        // Update on input
        textarea.addEventListener('input', function() {
            charCount.textContent = `${this.value.length}/${maxLength}`;
            if (this.value.length >= maxLength * 0.8) {
                charCount.style.color = '#e65100';
            } else {
                charCount.style.color = '#999';
            }
        });
    });
    
    // ===== Table Enhancements =====
    // Add row hover effects and action buttons
    const tables = document.querySelectorAll('.table-gov');
    tables.forEach(table => {
        const rows = table.querySelectorAll('tbody tr');
        rows.forEach(row => {
            row.style.cursor = 'pointer';
            row.addEventListener('mouseenter', function() {
                this.style.background = '#f5f5f5';
            });
            row.addEventListener('mouseleave', function() {
                this.style.background = 'white';
            });
        });
    });
    
    // ===== Status Badge Color =====
    // Dynamically apply status colors
    const statusBadges = document.querySelectorAll('[data-status]');
    statusBadges.forEach(badge => {
        const status = badge.dataset.status;
        badge.className = 'badge-status badge-' + status;
    });
    
    // ===== Tooltip Initialization =====
    // Simple tooltip for help icons
    const helpIcons = document.querySelectorAll('.form-help i');
    helpIcons.forEach(icon => {
        icon.addEventListener('mouseenter', function() {
            const helpText = this.parentElement.title;
            if (helpText) {
                this.title = helpText;
            }
        });
    });
    
    // ===== Loading States =====
    // Show loading skeleton on form submission
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = this.querySelector('[type="submit"]');
            if (submitBtn) {
                const originalText = submitBtn.textContent;
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
                
                // Restore after 30 seconds (safety timeout)
                setTimeout(() => {
                    submitBtn.disabled = false;
                    submitBtn.textContent = originalText;
                }, 30000);
            }
        });
    });
    
    // ===== Alert Auto-dismiss =====
    // Auto dismiss success alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert-success');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.3s ease';
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });
    
    // ===== Print Functionality =====
    // Add print button functionality
    const printButtons = document.querySelectorAll('[data-print]');
    printButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const target = document.querySelector(this.dataset.print);
            if (target) {
                const printWindow = window.open('', '', 'height=600,width=800');
                printWindow.document.write('<html><head><title>Print</title>');
                printWindow.document.write('<link rel="stylesheet" href="/static/css/gov-portal.css">');
                printWindow.document.write('</head><body>');
                printWindow.document.write(target.innerHTML);
                printWindow.document.write('</body></html>');
                printWindow.document.close();
                printWindow.print();
            }
        });
    });
    
    // ===== Export Functionality =====
    // Simple CSV export for tables
    const exportButtons = document.querySelectorAll('[data-export]');
    exportButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const target = document.querySelector(this.dataset.export);
            if (target) {
                const table = target.tagName === 'TABLE' ? target : target.querySelector('table');
                if (table) {
                    exportTableToCSV(table, this.dataset.filename || 'export.csv');
                }
            }
        });
    });
    
    // ===== Breadcrumb Navigation =====
    // Ensure breadcrumbs are accessible
    const breadcrumbs = document.querySelectorAll('.breadcrumb-item');
    breadcrumbs.forEach((item, index) => {
        if (index === breadcrumbs.length - 1) {
            item.setAttribute('aria-current', 'page');
        }
    });
});

// CSV Export Helper Function
function exportTableToCSV(table, filename) {
    let csv = [];
    const rows = table.querySelectorAll('tr');
    
    rows.forEach(row => {
        let csvRow = [];
        const cells = row.querySelectorAll('td, th');
        cells.forEach(cell => {
            csvRow.push('"' + cell.textContent.trim().replace(/"/g, '""') + '"');
        });
        csv.push(csvRow.join(','));
    });
    
    // Create blob and download
    const csvContent = 'data:text/csv;charset=utf-8,' + csv.join('\n');
    const link = document.createElement('a');
    link.setAttribute('href', encodeURI(csvContent));
    link.setAttribute('download', filename);
    link.click();
}

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            e.preventDefault();
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});

// Keyboard shortcuts
document.addEventListener('keydown', function(event) {
    // Alt + S: Skip to content
    if (event.altKey && event.key === 's') {
        const skipLink = document.querySelector('.skip-link');
        if (skipLink) skipLink.focus();
    }
    
    // Alt + H: Show help
    if (event.altKey && event.key === 'h') {
        const accessibilityToggle = document.getElementById('accessibility-toggle');
        if (accessibilityToggle) accessibilityToggle.click();
    }
});

// Prevent console errors in production
if (typeof console === 'undefined') {
    window.console = { log: () => {}, warn: () => {}, error: () => {} };
}
