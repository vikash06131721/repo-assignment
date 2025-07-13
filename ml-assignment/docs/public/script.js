// DOM Elements
const endpointSelect = document.getElementById('endpoint-select');
const requestBody = document.getElementById('request-body');
const testButton = document.getElementById('test-button');
const responseOutput = document.getElementById('response-output');
const serverStatusIndicator = document.getElementById('server-status-indicator');
const serverStatusText = document.getElementById('server-status-text');
const tabButtons = document.querySelectorAll('.tab-button');
const tabPanes = document.querySelectorAll('.tab-pane');
const navLinks = document.querySelectorAll('.nav-link');

// API Configuration
const API_BASE_URL = 'http://localhost:8002';

// Sample request bodies for different endpoints
const sampleRequests = {
    'calculate-features': {
        "id": "test_123",
        "application_date": "2024-02-12T19:24:29.135000",
        "contracts": [
            {
                "contract_id": "522530",
                "bank": "003",
                "summa": "500000000",
                "loan_summa": "0",
                "claim_date": "13.02.2020",
                "claim_id": "609965",
                "contract_date": "17.02.2020"
            },
            {
                "contract_id": "522531",
                "bank": "LIZ",
                "summa": "1000000",
                "loan_summa": "1000000",
                "claim_date": "15.01.2024",
                "claim_id": "609966",
                "contract_date": "20.01.2024"
            }
        ]
    },
    'calculate-features-from-json': {
        "id": "test_456",
        "application_date": "2024-02-12 19:24:29.135000+00:00",
        "contracts": "[{\"contract_id\": 522530, \"bank\": \"003\", \"summa\": 500000000, \"loan_summa\": 0, \"claim_date\": \"13.02.2020\", \"claim_id\": \"609965\", \"contract_date\": \"17.02.2020\"}]"
    },
    'health': null
};

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Check server status
    checkServerStatus();
    
    // Set up event listeners
    setupEventListeners();
    
    // Load initial sample request
    loadSampleRequest();
    
    // Initialize tab functionality
    initializeTabs();
    
    // Initialize smooth scrolling
    initializeSmoothScrolling();
    
    // Check server status periodically
    setInterval(checkServerStatus, 30000); // Check every 30 seconds
}

function setupEventListeners() {
    // Endpoint selection change
    endpointSelect.addEventListener('change', loadSampleRequest);
    
    // Test button click
    testButton.addEventListener('click', sendTestRequest);
    
    // Tab button clicks
    tabButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            const tabName = e.target.getAttribute('data-tab');
            switchTab(tabName);
        });
    });
    
    // Navigation link clicks
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href').substring(1);
            scrollToSection(targetId);
        });
    });
    
    // Enter key in textarea
    requestBody.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.key === 'Enter') {
            sendTestRequest();
        }
    });
}

function loadSampleRequest() {
    const selectedEndpoint = endpointSelect.value;
    const sample = sampleRequests[selectedEndpoint];
    
    if (sample) {
        requestBody.value = JSON.stringify(sample, null, 2);
    } else {
        requestBody.value = '';
    }
    
    // Update placeholder text
    if (selectedEndpoint === 'health') {
        requestBody.placeholder = 'No request body needed for health check';
        requestBody.disabled = true;
    } else {
        requestBody.placeholder = 'Enter JSON request body...';
        requestBody.disabled = false;
    }
}

async function checkServerStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (response.ok) {
            updateServerStatus(true, 'API server is online');
        } else {
            updateServerStatus(false, 'API server returned error');
        }
    } catch (error) {
        updateServerStatus(false, 'API server is offline');
    }
}

function updateServerStatus(isOnline, message) {
    serverStatusIndicator.className = `status-indicator ${isOnline ? 'online' : 'offline'}`;
    serverStatusText.textContent = message;
}

async function sendTestRequest() {
    const selectedEndpoint = endpointSelect.value;
    const url = `${API_BASE_URL}/${selectedEndpoint}`;
    
    // Disable button and show loading state
    testButton.disabled = true;
    testButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
    
    try {
        let requestOptions = {
            method: selectedEndpoint === 'health' ? 'GET' : 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        };
        
        // Add request body for POST requests
        if (selectedEndpoint !== 'health') {
            const bodyText = requestBody.value.trim();
            if (!bodyText) {
                throw new Error('Request body is required');
            }
            
            // Validate JSON
            try {
                JSON.parse(bodyText);
                requestOptions.body = bodyText;
            } catch (e) {
                throw new Error('Invalid JSON format');
            }
        }
        
        const startTime = Date.now();
        const response = await fetch(url, requestOptions);
        const endTime = Date.now();
        const responseTime = endTime - startTime;
        
        const responseData = await response.json();
        
        // Format response
        const formattedResponse = {
            status: response.status,
            statusText: response.statusText,
            responseTime: `${responseTime}ms`,
            headers: Object.fromEntries(response.headers.entries()),
            data: responseData
        };
        
        // Display response with syntax highlighting
        responseOutput.textContent = JSON.stringify(formattedResponse, null, 2);
        responseOutput.style.color = response.ok ? '#10b981' : '#ef4444';
        
        // Show success/error message
        if (response.ok) {
            showNotification('Request successful!', 'success');
        } else {
            showNotification('Request failed', 'error');
        }
        
    } catch (error) {
        const errorResponse = {
            error: error.message,
            timestamp: new Date().toISOString()
        };
        
        responseOutput.textContent = JSON.stringify(errorResponse, null, 2);
        responseOutput.style.color = '#ef4444';
        
        showNotification(`Error: ${error.message}`, 'error');
    } finally {
        // Re-enable button
        testButton.disabled = false;
        testButton.innerHTML = '<i class="fas fa-play"></i> Send Request';
    }
}

function initializeTabs() {
    // Set first tab as active if none is active
    if (!document.querySelector('.tab-button.active')) {
        tabButtons[0].classList.add('active');
        tabPanes[0].classList.add('active');
    }
}

function switchTab(tabName) {
    // Remove active class from all tabs
    tabButtons.forEach(btn => btn.classList.remove('active'));
    tabPanes.forEach(pane => pane.classList.remove('active'));
    
    // Add active class to selected tab
    const selectedButton = document.querySelector(`[data-tab="${tabName}"]`);
    const selectedPane = document.getElementById(tabName);
    
    if (selectedButton && selectedPane) {
        selectedButton.classList.add('active');
        selectedPane.classList.add('active');
    }
}

function initializeSmoothScrolling() {
    // Add smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            scrollToSection(targetId);
        });
    });
}

function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        const offsetTop = section.offsetTop - 100; // Account for fixed navbar
        window.scrollTo({
            top: offsetTop,
            behavior: 'smooth'
        });
    }
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas ${type === 'success' ? 'fa-check-circle' : type === 'error' ? 'fa-exclamation-circle' : 'fa-info-circle'}"></i>
            <span>${message}</span>
        </div>
    `;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 10000;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        color: white;
        font-weight: 600;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
        transform: translateX(100%);
        transition: transform 0.3s ease;
        max-width: 400px;
        ${type === 'success' ? 'background: #10b981;' : type === 'error' ? 'background: #ef4444;' : 'background: #667eea;'}
    `;
    
    // Add to document
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

// Utility function to format JSON
function formatJSON(json) {
    try {
        const parsed = JSON.parse(json);
        return JSON.stringify(parsed, null, 2);
    } catch (error) {
        return json;
    }
}

// Utility function to copy text to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showNotification('Copied to clipboard!', 'success');
    }).catch(() => {
        showNotification('Failed to copy to clipboard', 'error');
    });
}

// Add copy functionality to code blocks
document.addEventListener('DOMContentLoaded', function() {
    const codeBlocks = document.querySelectorAll('pre code');
    codeBlocks.forEach(block => {
        const pre = block.parentElement;
        const copyButton = document.createElement('button');
        copyButton.className = 'copy-button';
        copyButton.innerHTML = '<i class="fas fa-copy"></i>';
        copyButton.title = 'Copy code';
        copyButton.style.cssText = `
            position: absolute;
            top: 10px;
            right: 10px;
            background: rgba(255, 255, 255, 0.2);
            border: none;
            color: white;
            padding: 0.5rem;
            border-radius: 6px;
            cursor: pointer;
            transition: background 0.3s ease;
        `;
        
        copyButton.addEventListener('click', () => {
            copyToClipboard(block.textContent);
        });
        
        copyButton.addEventListener('mouseenter', () => {
            copyButton.style.background = 'rgba(255, 255, 255, 0.3)';
        });
        
        copyButton.addEventListener('mouseleave', () => {
            copyButton.style.background = 'rgba(255, 255, 255, 0.2)';
        });
        
        pre.style.position = 'relative';
        pre.appendChild(copyButton);
    });
});

// Add keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + K to focus on search (if implemented)
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        // Focus on search input if it exists
        const searchInput = document.querySelector('input[type="search"]');
        if (searchInput) {
            searchInput.focus();
        }
    }
    
    // Escape key to close modals or clear focus
    if (e.key === 'Escape') {
        document.activeElement.blur();
    }
});

// Add scroll spy functionality for navigation
window.addEventListener('scroll', function() {
    const sections = document.querySelectorAll('.section[id]');
    const scrollPos = window.scrollY + 150; // Account for navbar
    
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.offsetHeight;
        const sectionId = section.getAttribute('id');
        
        if (scrollPos >= sectionTop && scrollPos < sectionTop + sectionHeight) {
            // Update active nav link
            navLinks.forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === `#${sectionId}`) {
                    link.classList.add('active');
                }
            });
        }
    });
});

// Add loading animation for images
document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        img.addEventListener('load', function() {
            this.style.opacity = '1';
        });
    });
});

// Console welcome message
console.log(`
🚀 ML Feature Engineering API Documentation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔧 API Server: ${API_BASE_URL}
📝 Documentation: http://localhost:5002/docs
🎯 Interactive Tester: Available on this page
⚡ Features: Real-time testing, code examples, comprehensive docs

Need help? Check the documentation sections above or test the API directly!
`);

// Export functions for global access
window.MLFeatureAPIDocs = {
    checkServerStatus,
    sendTestRequest,
    switchTab,
    scrollToSection,
    showNotification,
    copyToClipboard,
    formatJSON
}; 