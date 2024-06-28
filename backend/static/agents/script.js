var socket;

async function createDummyGroup() {
    const user_id = document.getElementById('user_id').value;
    if(user_id){
        const response = await fetch(`http://localhost:8000/agents/users/${user_id}/groupchat/create-dummy-group`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ user_id: user_id }),
        });

        if(!response.ok){
            console.log(`Failed to create dummy group because of an error: ${response.status} ${response.statusText}`);
            return;
        }
        const data = await response.json();
        console.log(data);
        document.getElementById('group_id').textContent = data.group_id;
    
    }
}

function connect() {
    var user_id = document.getElementById('user_id').value;
    var group_id = document.getElementById('group_id').value;
    socket = new WebSocket("ws://localhost:8000/agents/users/" + user_id + "/groupchat/" + group_id);

    socket.onmessage = function (event) {
        var messages = document.getElementById('messages');
        messages.textContent += '\n' + event.data;
    };

    socket.onclose = function (event) {
        console.log("WebSocket closed: ", event);
    };

    socket.onerror = function (error) {
        console.log("WebSocket Error: ", error);
    };
}

function sendMessage() {
    var message = document.getElementById('message').value;
    socket.send(message);
}