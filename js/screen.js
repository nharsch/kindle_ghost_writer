// debugger
function debug(str){ $("#debug").append("<p>"+str+"</p>"); };

try {
    ws = new WebSocket("ws://192.168.1.65:8888/screen_socket");
}
catch(err) {
    debug("error" + err.message)
}


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
    console.log("opened connection");
    ws.send("hello server");
};

ws.onclose = function(event) {
    console.log(event);
};

ws.onerror =  function(event) {
    console.log(event)
};
