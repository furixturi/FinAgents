let ws;

function connectWebSocket() {
    const userId = document.getElementById("userIdInput").value;
    if(!ws) {
        console.log(`!ws ${!ws}. Connecting to WebSocket with user ID: ${userId}`);
        ws = new WebSocket(`ws://localhost:8000/chat/${userId}`);

        ws.onmessage = function (event) {
            const messages = document.getElementById('chat');
            const messageData = JSON.parse(event.data);
            const message = document.createElement('div');
            const content = document.createTextNode(`[User ID: ${messageData.user_id}] [Username: ${messageData.username}] ${messageData.message} [Timestamp: ${messageData.timestamp}]`);
            message.appendChild(content);
            messages.appendChild(message);
        };
    }
}

function sendMessage() {
    const input = document.getElementById("messageInput");
    const recipientId = document.getElementById("recipientIdInput").value;
    const message = {
        message: input.value
    };
    if (recipientId) {
        message.recipient_id = recipientId;
    }
    ws.send(JSON.stringify(message));
    input.value = '';
}