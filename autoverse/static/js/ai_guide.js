let chatHistory = [];

function toggleChat() {
    const win = document.getElementById('ai-chat-window');
    win.style.display = win.style.display === 'flex' ? 'none' : 'flex';
    if(win.style.display === 'flex') {
        document.getElementById('ai-chat-input').focus();
        if(chatHistory.length === 0) {
            addMessage("Hello! I am your AutoVerse Virtual Guide. I can help you understand F1 aerodynamics, engine mechanics, or any car-related technology. How can I assist you?", "ai");
        }
    }
}

function addMessage(text, sender) {
    const messagesDiv = document.getElementById('chat-messages');
    const msg = document.createElement('div');
    msg.className = `chat-msg msg-${sender}`;
    msg.textContent = text;
    messagesDiv.appendChild(msg);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

async function sendChatMessage() {
    const input = document.getElementById('ai-chat-input');
    const text = input.value.trim();
    if(!text) return;
    
    input.value = '';
    addMessage(text, 'user');
    
    document.getElementById('typing-indicator').style.display = 'block';
    
    try {
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                message: text,
                history: chatHistory
            })
        });
        
        const data = await response.json();
        document.getElementById('typing-indicator').style.display = 'none';
        
        if(data.reply) {
            addMessage(data.reply, 'ai');
            chatHistory.push({"role": "user", "content": text});
            chatHistory.push({"role": "assistant", "content": data.reply});
        } else {
            addMessage("I am currently experiencing connection issues. Please try again.", "ai");
        }
        
    } catch(err) {
        console.error(err);
        document.getElementById('typing-indicator').style.display = 'none';
        addMessage("Communication disrupted. Link offline.", "ai");
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('ai-chat-input');
    if(input) {
        input.addEventListener('keypress', function(e) {
            if(e.key === 'Enter') {
                sendChatMessage();
            }
        });
    }
});
