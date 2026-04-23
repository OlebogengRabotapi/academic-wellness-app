/**
 * StudyMind JavaScript functionality
 */

// Study Session Tracking
class StudySessionTracker {
    constructor() {
        this.currentSessionId = null;
        this.startTime = null;
        this.timerInterval = null;
        this.init();
    }

    init() {
        this.bindEvents();
        this.checkExistingSession();
    }

    bindEvents() {
        const startBtn = document.getElementById('start-session-btn');
        const endBtn = document.getElementById('end-session-btn');

        if (startBtn) {
            startBtn.addEventListener('click', () => this.startSession());
        }

        if (endBtn) {
            endBtn.addEventListener('click', () => this.endSession());
        }
    }

    async startSession() {
        const materialId = document.getElementById('start-session-btn').dataset.materialId;
        const activityType = 'reading'; // Default activity type

        try {
            const response = await fetch(`/session/start/${materialId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken(),
                },
                body: JSON.stringify({ activity_type: activityType }),
            });

            const data = await response.json();

            if (data.session_id) {
                this.currentSessionId = data.session_id;
                this.startTime = new Date();
                this.showTimer();
                this.updateButtons(true);
                this.startTimer();
                this.showMessage('Study session started!', 'success');
            }
        } catch (error) {
            console.error('Error starting session:', error);
            this.showMessage('Error starting session', 'danger');
        }
    }

    async endSession() {
        if (!this.currentSessionId) return;

        try {
            const response = await fetch('/session/end/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken(),
                },
            });

            const data = await response.json();

            if (data.success) {
                this.stopTimer();
                this.hideTimer();
                this.updateButtons(false);
                this.showMessage('Study session ended!', 'success');
                this.currentSessionId = null;
                this.startTime = null;

                // Refresh the page to update stats
                setTimeout(() => location.reload(), 1000);
            }
        } catch (error) {
            console.error('Error ending session:', error);
            this.showMessage('Error ending session', 'danger');
        }
    }

    startTimer() {
        this.timerInterval = setInterval(() => {
            if (this.startTime) {
                const elapsed = new Date() - this.startTime;
                const hours = Math.floor(elapsed / 3600000);
                const minutes = Math.floor((elapsed % 3600000) / 60000);
                const seconds = Math.floor((elapsed % 60000) / 1000);

                document.getElementById('timer-display').textContent =
                    `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
            }
        }, 1000);
    }

    stopTimer() {
        if (this.timerInterval) {
            clearInterval(this.timerInterval);
            this.timerInterval = null;
        }
    }

    showTimer() {
        document.getElementById('session-timer').style.display = 'block';
    }

    hideTimer() {
        document.getElementById('session-timer').style.display = 'none';
    }

    updateButtons(sessionActive) {
        const startBtn = document.getElementById('start-session-btn');
        const endBtn = document.getElementById('end-session-btn');

        if (sessionActive) {
            startBtn.style.display = 'none';
            endBtn.style.display = 'block';
        } else {
            startBtn.style.display = 'block';
            endBtn.style.display = 'none';
        }
    }

    checkExistingSession() {
        // Check if there's an existing session in sessionStorage
        const sessionData = sessionStorage.getItem('studymind_session');
        if (sessionData) {
            const data = JSON.parse(sessionData);
            this.currentSessionId = data.session_id;
            this.startTime = new Date(data.start_time);
            this.showTimer();
            this.updateButtons(true);
            this.startTimer();
        }
    }

    getCSRFToken() {
        return window.CSRF_TOKEN || document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
    }

    showMessage(message, type) {
        // Create a simple alert message
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        document.body.appendChild(alertDiv);

        // Auto remove after 3 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 3000);
    }
}

// Chat Functionality
class ChatManager {
    constructor() {
        this.materialId = null;
        this.init();
    }

    init() {
        const chatForm = document.getElementById('chat-form');
        if (chatForm) {
            this.materialId = chatForm.action.split('/').slice(-2)[0]; // Extract material ID from URL
            chatForm.addEventListener('submit', (e) => this.handleChatSubmit(e));
            this.loadRecentMessages();
        }
    }

    async handleChatSubmit(event) {
        event.preventDefault();
        
        const form = event.target;
        const formData = new FormData(form);
        const message = formData.get('message');
        
        if (!message.trim()) return;
        
        // Disable form while processing
        const submitBtn = form.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Thinking...';
        
        try {
            const response = await fetch(form.action, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': this.getCSRFToken(),
                },
                body: formData,
            });
            
            if (response.ok) {
                // Clear the form
                form.querySelector('textarea').value = '';
                // Reload messages
                await this.loadRecentMessages();
                this.showMessage('Question answered by AI tutor!', 'success');
            } else {
                this.showMessage('Error sending message', 'danger');
            }
        } catch (error) {
            console.error('Error sending chat message:', error);
            this.showMessage('Error sending message', 'danger');
        } finally {
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;
        }
    }

    async loadRecentMessages() {
        const messagesContainer = document.getElementById('chat-messages');
        if (!messagesContainer || !this.materialId) return;
        
        try {
            const response = await fetch(`/api/material/${this.materialId}/summary/`);
            const data = await response.json();
            
            // For now, just show that chat is available
            // In a full implementation, you'd have an API endpoint for recent chat messages
            messagesContainer.innerHTML = `
                <div class="text-center text-muted">
                    <small>Chat with AI tutor about this material</small>
                </div>
            `;
        } catch (error) {
            console.error('Error loading messages:', error);
        }
    }

    getCSRFToken() {
        return window.CSRF_TOKEN || document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
    }

    showMessage(message, type) {
        // Create a simple alert message
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(alertDiv);
        
        // Auto remove after 3 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 3000);
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    new StudySessionTracker();
    new ChatManager();
});