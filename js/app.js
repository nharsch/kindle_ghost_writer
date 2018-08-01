// window.alert('testing that js works');
ws = new WebSocket("ws://192.168.1.65:8080");
doc = document.getElementById('doc');

function debug(str){ $("#debug").append("<p>"+str+"</p>"); };

ws.onmessage = function (event) {
    if (event.data) {
        data = JSON.parse(event.data)
        doc.innerHTML = data.html
    }
}
ws.onclose = function() { debug("socket closed"); };
ws.onerror =  function(event) { debug("socket error observed"); };
ws.onopen = function() {
    debug("connected...");
    ws.send("hello server");
};
