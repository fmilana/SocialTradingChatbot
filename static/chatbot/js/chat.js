var socket = require('socket.io-client')('http://localhost:5500');

$(document).ready(function() {

	function appendBotMessage(data) {
		var message = data['text'];

		$("#result_div").append("<p id='bot-message'>" + message + "</p><br>");
		$('#result_div').scrollTop($('#result_div')[0].scrollHeight);
	}

	// console log when socket connects to port 5500
	socket.on('connect', function() {
		console.log('connection established...')
	});

	// socket.emit('user_uttered', {'message': 'hey', 'sender': 'rasa'});

	var sendMessage = function() {
		const chatInput = $("#chat-input").val();
		console.log(chatInput);
		if (chatInput) {
			socket.emit('user_uttered', {'message': chatInput, 'sender': 'rasa'});
			$("#result_div").append("<p id='user-message'> " + chatInput + "</p><br>");
			$('#result_div').scrollTop($('#result_div')[0].scrollHeight);
			$("#chat-input").val('');
		}
	};

	$("#send").click(sendMessage);

	$('#chat-input').keyup(function (e) {
		console.log(e.keyCode);
    if (e.keyCode === 13) {
			sendMessage();
    }
	});



	// event when bot utters message
	socket.on('bot_uttered', function(data){
		console.log(data);

		setTimeout(function() {appendBotMessage(data);}, 500);

		$("#portfolios").load(location.href+" #portfolios>*","");
	});

	// do something when connection closes
	socket.on('disconnect', function(){});

});
