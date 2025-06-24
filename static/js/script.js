document.addEventListener('DOMContentLoaded', function() {
    const themeSwitch = document.getElementById('theme-switch');
    const chatMessages = document.getElementById('chat-messages');
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');

    // Theme switching
    if (themeSwitch) {
        themeSwitch.addEventListener('click', () => {
            document.body.dataset.theme = document.body.dataset.theme === 'dark' ? 'light' : 'dark';
            localStorage.setItem('theme', document.body.dataset.theme);
        });

        // Load saved theme
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme) {
            document.body.dataset.theme = savedTheme;
        }
    }

    // Chat functionality
    if (sendButton && messageInput) {
        sendButton.addEventListener('click', sendMessage);
        messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }

    function sendMessage() {
        const message = messageInput.value.trim();
        if (!message) return;

        // Add user message to chat
        addMessageToChat('user', message);
        messageInput.value = '';

        // Send message to server
        fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            addMessageToChat('bot', data.response);
        })
        .catch(error => {
            console.error('Error:', error);
            addMessageToChat('bot', 'Sorry, there was an error processing your message.');
        });
    }

    function addMessageToChat(type, message) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}-message`;
        messageDiv.textContent = message;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});
