/**
 * Medium Articles Search - Main JavaScript
 */

// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });
    
    // Initialize article image modals
    setupImageModals();
    
    // Add smooth scrolling to anchor links
    setupSmoothScrolling();
    
    // Back to top button
    setupBackToTopButton();
});

/**
 * Sets up modals for article images
 */
function setupImageModals() {
    const articleImages = document.querySelectorAll('.article-image');
    
    articleImages.forEach(img => {
        img.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Create modal dynamically
            const modal = document.createElement('div');
            modal.classList.add('modal', 'fade');
            modal.id = 'imageModal';
            modal.setAttribute('tabindex', '-1');
            modal.setAttribute('aria-labelledby', 'imageModalLabel');
            modal.setAttribute('aria-hidden', 'true');
            
            const modalContent = `
                <div class="modal-dialog modal-lg modal-dialog-centered">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="imageModalLabel">Image Preview</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body text-center">
                            <img src="${img.src}" class="img-fluid" alt="Full size image">
                        </div>
                    </div>
                </div>
            `;
            
            modal.innerHTML = modalContent;
            document.body.appendChild(modal);
            
            // Create and show bootstrap modal
            const modalInstance = new bootstrap.Modal(modal);
            modalInstance.show();
            
            // Remove modal from DOM after it's hidden
            modal.addEventListener('hidden.bs.modal', function() {
                document.body.removeChild(modal);
            });
        });
    });
}

/**
 * Sets up smooth scrolling for anchor links
 */
function setupSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            
            if (href !== '#') {
                e.preventDefault();
                
                document.querySelector(href).scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
}

/**
 * Sets up back to top button functionality
 */
function setupBackToTopButton() {
    // Create the button if it doesn't exist
    if (!document.getElementById('backToTop')) {
        const button = document.createElement('button');
        button.id = 'backToTop';
        button.innerHTML = '<i class="fas fa-arrow-up"></i>';
        button.setAttribute('aria-label', 'Back to top');
        button.setAttribute('title', 'Back to top');
        
        // Add styles
        button.style.position = 'fixed';
        button.style.bottom = '20px';
        button.style.right = '20px';
        button.style.display = 'none';
        button.style.padding = '10px 15px';
        button.style.borderRadius = '50%';
        button.style.backgroundColor = '#6a0dad';
        button.style.color = '#fff';
        button.style.border = 'none';
        button.style.cursor = 'pointer';
        button.style.zIndex = '1000';
        button.style.boxShadow = '0 2px 5px rgba(106, 13, 173, 0.3)';
        
        document.body.appendChild(button);
        
        // Add scroll event listener
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                button.style.display = 'block';
            } else {
                button.style.display = 'none';
            }
        });
        
        // Add click event listener
        button.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
}

/**
 * Formats article content for better readability
 */
function formatArticleContent() {
    const contentElement = document.querySelector('.article-content');
    
    if (contentElement) {
        // Add paragraph tags to text blocks separated by double newlines
        let content = contentElement.innerHTML;
        content = content.replace(/\n\n/g, '</p><p>');
        content = '<p>' + content + '</p>';
        
        // Fix any empty paragraphs
        content = content.replace(/<p>\s*<\/p>/g, '<br>');
        
        contentElement.innerHTML = content;
    }
}

/**
 * Handles form validation for search form
 */
function validateSearchForm(formElement) {
    const keywordInput = formElement.querySelector('#keyword');
    
    if (!keywordInput.value.trim()) {
        // Show error
        keywordInput.classList.add('is-invalid');
        
        // Create error message if it doesn't exist
        let errorMessage = formElement.querySelector('.invalid-feedback');
        if (!errorMessage) {
            errorMessage = document.createElement('div');
            errorMessage.classList.add('invalid-feedback');
            errorMessage.textContent = 'Please enter a search keyword';
            keywordInput.parentNode.appendChild(errorMessage);
        }
        
        return false;
    }
    
    return true;
}