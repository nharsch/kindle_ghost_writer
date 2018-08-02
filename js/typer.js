websocket_address = "ws://" + server_address + ":" + port + "/typer_socket"

// debugger
function debug(str){ $("#debug").append("<p>"+str+"</p>"); };

try {
    ws = new WebSocket(websocket_address);
}
catch(err) {
    debug("error" + err.message)
}


// keyboard
keyboard = document.getElementById('keyboard');
keyboard.contentEditable = true;
function sendText() {
    var msg = {
        html : keyboard.innerHTML,
    }
    console.log("sending message: ", msg)
    ws.send(JSON.stringify(msg));
}
keyboard.addEventListener("input", sendText);


// other handlers
ws.onopen = function() { ws.send("hello server"); };

ws.onclose = function(event) { console.log(event); };

ws.onerror =  function(event) { console.log(event) };
