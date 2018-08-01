var messageSocket = new WebSocket("ws://192.168.1.65:8080");
var doc = document.getElementById('doc');

// doc.contentEditable = true;
// doc.focus();

// function sendText() {
//     var msg = {
//         html : doc.innerHTML,
//     }
//     console.log("sending message: ", msg)
//     messageSocket.send(JSON.stringify(msg));
// }
//
// TODO edit handler
// doc.addEventListener("input", sendText);

messageSocket.onmessage = function (event) {
    if (event.data) {
        data = JSON.parse(event.data)
        console.log(data.html);
        doc.innerHTML = data.html
    }
}
