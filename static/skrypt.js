function funkcja(){
	var message = document.getElementById("message").value;
	var key = document.getElementById("key").value;
	if(key.length < message.length && !messageAdded){
		var alert_message = document.createElement("p");
		alert_message.innerText = "Key is shorter than the message. This negatively impects the security of the hash!!!";
		const encryption_form = document.getElementById("encryption_form");
		const article = encryption_form.parentElement;
		article.insertBefore(alert_message, encryption_form);
		messageAdded = true;
	}
	else if(key.length >= message.length && messageAdded){
		
	}
}

var message = document.getElementById("message");
var key = document.getElementById("key");
var messageAdded = false;
message.addEventListener("input", funkcja);
key.addEventListener("input", funkcja);
