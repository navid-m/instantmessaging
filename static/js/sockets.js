var socket = io();
var room;

socket.on('connect', function() {
	socket.emit('msg', 'joined. <a hidden id = "status"></a>')
})

socket.on('declarecode', function(serverroom) {
	room = serverroom
})

socket.on('msg', function(msg) {
	if (msg.includes(room)) {
		var toadd = "";
		if (!msg.includes(":")) {
			toadd += "<center>"
		}
		toadd += "<br><span class = 'fmsg'>" + msg + "</span><br><br></center>";
		msdiv = document.getElementById("messages"); 
		msdiv.innerHTML += toadd
		msdiv.scrollTop = msdiv.scrollHeight - msdiv.clientHeight;
	}
})

socket.on('disconnect', function() {
	socket.emit('disc')
})

function sendmsg() {
	if (document.getElementById("message").value.trim() != "") {
		socket.emit('msg', document.getElementById("message").value)	
		document.getElementById("message").value = ""
	}
}

window.addEventListener("keyup", function(event) {
    if (event.key == "Enter") {
    	sendmsg();
    }
});