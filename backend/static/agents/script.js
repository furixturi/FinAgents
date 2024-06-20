let ws;
const userId = document.getElementById("userIdInput").value;

function connectWebSocket() {
    if(!ws) {
        console.log(`!ws ${!ws}. Connecting to WebSocket with user ID: ${userId}`);
        ws = new WebSocket(`ws://localhost:8000//agents-chat/${userId}`);

        ws.onmessage = function (event) {
            console.log('Received message: ', event.data)
            const messages = document.getElementById('chat');
            const messageData = JSON.parse(event.data);
            const message = document.createElement('div');
            const content = document.createTextNode(`${messageData.agent_type} - ${messageData.name}: ${messageData.message} [Timestamp: ${messageData.sent_at}]`);
            message.appendChild(content);
            messages.appendChild(message);
        };
    }
}

function sendMessage() {
    const input = document.getElementById("messageInput");
    const message = {
        userId: userId,
        agent_type: "UserProxyAgent",
        message: input.value
    };

    console.log('Sending message: ', message);
    ws.send(JSON.stringify(message));
    input.value = '';
}