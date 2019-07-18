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
    if (e.keyCode === 13) {
			sendMessage();
    }
	});



	// event when bot utters message
	socket.on('bot_uttered', function(data){
		console.log(data);

		setTimeout(function() {appendBotMessage(data);}, 500);

		$("#portfolios").load(location.href+" #portfolios>*","", function() {
			if ($('#followed-portfolio-wrapper').length) {
				$('#empty-followed-tag').hide();
			} else {
				$('#empty-followed-tag').show();
			}

			if ($('#not-followed-portfolio-wrapper').length) {
				$('#empty-not-followed-tag').hide();
			} else {
				$('#empty-not-followed-tag').show();
			}
		});
		// $("#row-followed").load(location.href+" #row-followed>*","");
		// $("#row-not-followed").load(location.href+" #row-not-followed>*","");

		// $("empty-followed-tag").hide();

		console.log('portfolios html refreshed');

		$.ajax({
				type: "GET",
				url: server_url + '/updatebalances/',
				success: function (response) {
						console.log(response);

						$('#available-balance-amount').html(response.available_balance_amount);
						$('#invested-balance-amount').html(response.invested_balance_amount);

				}
		});
	});

	// do something when connection closes
	socket.on('disconnect', function(){});

});
