/**
 * Crop Price Predictor - Main JavaScript
 * Handles interactive features and form validations
 */

// ========== Document Ready ==========
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    initTooltips();
    
    // Auto-dismiss alerts after 5 seconds
    autoDismissAlerts();
    
    // Add fade-in animation to cards
    animateOnScroll();
});

// ========== Tooltip Initialization ==========
function initTooltips() {
    const tooltipTriggerList = [].slice.call(
        document.querySelectorAll('[data-bs-toggle="tooltip"]')
    );
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// ========== Auto Dismiss Alerts ==========
function autoDismissAlerts() {
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
}

// ========== Scroll Animation ==========
function animateOnScroll() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, {
        threshold: 0.1
    });

    const elements = document.querySelectorAll('.card, .feature-card');
    elements.forEach(el => observer.observe(el));
}

// ========== Form Validation ==========
// Validate prediction form
const predictionForm = document.getElementById('predictionForm');
if (predictionForm) {
    predictionForm.addEventListener('submit', function(e) {
        const month = parseInt(document.getElementById('month').value);
        const year = parseInt(document.getElementById('year').value);
        const rainfall = parseFloat(document.getElementById('rainfall').value);

        // Validate month
        if (month < 1 || month > 12) {
            e.preventDefault();
            showAlert('Please select a valid month (1-12)', 'danger');
            return false;
        }

        // Validate year
        const currentYear = new Date().getFullYear();
        if (year < 2000 || year > currentYear + 10) {
            e.preventDefault();
            showAlert(`Please enter a valid year (2000-${currentYear + 10})`, 'danger');
            return false;
        }

        // Validate rainfall (if provided)
        if (rainfall && (rainfall < 0 || rainfall > 5000)) {
            e.preventDefault();
            showAlert('Please enter a valid rainfall value (0-5000 mm)', 'danger');
            return false;
        }
    });
}

// ========== Show Alert Function ==========
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        <i class="fas fa-info-circle me-2"></i>${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        
        // Auto dismiss after 5 seconds
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alertDiv);
            bsAlert.close();
        }, 5000);
    }
}

// ========== Loading Spinner ==========
function showLoadingSpinner() {
    const spinner = document.createElement('div');
    spinner.id = 'globalSpinner';
    spinner.className = 'position-fixed top-50 start-50 translate-middle';
    spinner.innerHTML = `
        <div class="spinner-border text-success" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
    `;
    document.body.appendChild(spinner);
}

function hideLoadingSpinner() {
    const spinner = document.getElementById('globalSpinner');
    if (spinner) {
        spinner.remove();
    }
}

// ========== Number Formatting ==========
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR'
    }).format(amount);
}

// ========== Smooth Scroll ==========
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            e.preventDefault();
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// ========== Copy to Clipboard ==========
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showAlert('Copied to clipboard!', 'success');
    }).catch(err => {
        showAlert('Failed to copy', 'danger');
    });
}

// ========== Export Table to CSV ==========
function exportTableToCSV(tableId, filename = 'export.csv') {
    const table = document.getElementById(tableId);
    if (!table) return;

    let csv = [];
    const rows = table.querySelectorAll('tr');

    rows.forEach(row => {
        const cols = row.querySelectorAll('td, th');
        const rowData = Array.from(cols).map(col => col.textContent.trim());
        csv.push(rowData.join(','));
    });

    // Create download link
    const csvContent = csv.join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.click();
    window.URL.revokeObjectURL(url);
}

// ========== Back to Top Button ==========
window.addEventListener('scroll', function() {
    const backToTop = document.getElementById('backToTop');
    if (backToTop) {
        if (window.scrollY > 300) {
            backToTop.classList.add('show');
        } else {
            backToTop.classList.remove('show');
        }
    }
});

// ========== Print Page ==========
function printPage() {
    window.print();
}

// ========== Console Welcome Message ==========
console.log('%c🌾 Crop Price Predictor', 'color: #2ecc71; font-size: 24px; font-weight: bold;');
console.log('%cEmpowering farmers with AI-powered predictions', 'color: #95a5a6; font-size: 14px;');

