// Main JavaScript file for the Sorting Algorithm Visualizer web app

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the application
    initializeApp();
});

function initializeApp() {
    // Add smooth scrolling for navigation links
    addSmoothScrolling();
    
    // Add loading animations
    addLoadingAnimations();
    
    // Add interactive elements
    addInteractiveElements();
}

function addSmoothScrolling() {
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

function addLoadingAnimations() {
    // Add fade-in animation to elements
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe elements for animation
    document.querySelectorAll('.feature-card, .algorithm-card, .tip-card, .step').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
}

function addInteractiveElements() {
    // Add hover effects to buttons
    document.querySelectorAll('.btn').forEach(btn => {
        btn.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });
        
        btn.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Add click effects to cards
    document.querySelectorAll('.feature-card, .algorithm-card, .tip-card').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
}

// Utility functions
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 8px;
        color: white;
        font-weight: 500;
        z-index: 1000;
        transform: translateX(100%);
        transition: transform 0.3s ease;
    `;
    
    // Set background color based on type
    switch (type) {
        case 'success':
            notification.style.backgroundColor = '#22c55e';
            break;
        case 'error':
            notification.style.backgroundColor = '#ef4444';
            break;
        case 'warning':
            notification.style.backgroundColor = '#f59e0b';
            break;
        default:
            notification.style.backgroundColor = '#3b82f6';
    }
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

function formatNumbers(numbers) {
    if (numbers.length <= 10) {
        return numbers.join(', ');
    } else {
        return numbers.slice(0, 5).join(', ') + ' ... ' + numbers.slice(-5).join(', ');
    }
}

function validateNumberInput(input) {
    const trimmed = input.trim();
    if (!trimmed) return { valid: true, numbers: null, message: 'Empty input - will use random numbers' };
    
    const numbers = trimmed.replace(/,/g, ' ').split(/\s+/).filter(n => n);
    const validNumbers = [];
    const errors = [];
    
    for (const numStr of numbers) {
        const num = parseInt(numStr);
        if (isNaN(num)) {
            errors.push(`"${numStr}" is not a number`);
        } else if (num < 1 || num > 1000) {
            errors.push(`${num} is out of range (1-1000)`);
        } else {
            validNumbers.push(num);
        }
    }
    
    if (errors.length > 0) {
        return { valid: false, error: errors.join(', ') };
    }
    
    if (validNumbers.length > 25) {
        return { 
            valid: true, 
            numbers: validNumbers.slice(0, 25), 
            message: `Too many numbers. Using first 25: ${validNumbers.slice(0, 25).join(', ')}` 
        };
    }
    
    return { 
        valid: true, 
        numbers: validNumbers, 
        message: `Valid numbers: ${validNumbers.join(', ')}` 
    };
}

// Export functions for use in other scripts
window.SortingVisualizer = {
    showNotification,
    formatNumbers,
    validateNumberInput
};

