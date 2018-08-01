// debugger
function debug(str){ $("#debug").append("<p>"+str+"</p>"); };

try {
    ws = new WebSocket("ws://192.168.1.65:8888/echo");
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


// screen
screen = document.getElementById('screen');
ws.onmessage = function (event) {
    if (event.data) {
        data = JSON.parse(event.data)
        screen.innerHTML = data.html
    }
}

// other handlers
ws.onopen = function() {
    // debug("connected...");
    ws.send("hello server");
};

ws.onclose = function(event) {
    // console.log(event);
    // debug("socket closed " + JSON.stringify(event.code));
};

ws.onerror =  function(event) {
    console.log(event)
    // debug("socket error observed");
};
