// var socket = require('socket.io-client')('http://localhost:5500');

$(document).ready(function() {

	function appendBotMessage(data) {
		var message = data['text'];

		$('#result_div #typing-gif').remove();

		$("#result_div").append("<p id='bot-message'>" + message + "</p><br>");

		buttons = data['buttons'];

		if (typeof buttons !== 'undefined') {
			addSuggestion(buttons);
		}

		$('#result_div').scrollTop($('#result_div')[0].scrollHeight);
	}

	// console log when socket connects to port 5500
	// socket.on('connect', function() {
	// 	console.log('connection established...')
	// });

	// socket.emit('user_uttered', {'message': 'hey', 'sender': 'rasa'});



	// event when bot utters message
	function process_response(data) {
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
	}
	// socket.on('bot_uttered',process_response);

	function addSuggestion(suggestions) {
    setTimeout(function () {
      $('<div class="row suggestion-row"></div>').appendTo('#result_div');
      // Loop through suggestions
      for (i = 0; i < suggestions.length; i++) {
        $('<p class="sugg-options">' + suggestions[i].title + '</p>').appendTo('.suggestion-row');
      }

			suggestionRowHeight = $('.suggestion-row').height();
      resultDivHeight = $(window).height() - (205 + suggestionRowHeight);

			$('#result_div').css("height", resultDivHeight);
      $('#result_div').scrollTop($('#result_div')[0].scrollHeight);
    }, 500);
  }

	// on click of suggestions get value and send to API.AI
  $(document).on("click", ".sugg-options", function () {
    sendMessage(this.text());
  });

	var sendMessage = function(message) {
		console.log(message);
		if (message) {
			// TODO: change this to use $.post -- or even better fetch
			// TODO: use the user ID from django

			var url = server_url + '/chatbot/';
			var post_data = {'message': message, 'sender': username};
			fetch(post_url, {
				method: 'POST',
				body: JSON.stringify(post_data),
				credentials: 'include',
				headers: {'Content-Type': 'application/json'}
			}).then(res => res.json()).then(response => {
				console.log('POST response:', response);
				// window.location.replace(server_url + "/tasks/?order=" + next_task_order);
				//window.location = server_url + "/tasks/?order=" + next_task_order;
				process_response(response);
			}).catch(error => {
				console.log('POST error:', error);
			});

			$("#result_div").append("<p id='user-message'> " + message + "</p><br>");
			$('#result_div').scrollTop($('#result_div')[0].scrollHeight);
			setTimeout(function(){
				$('#result_div').append('<img id="typing-gif" src="' + staticUrl + 'chatbot/images/typing.svg">')
				$('#result_div').scrollTop($('#result_div')[0].scrollHeight);
			}, 500);
			$("#chat-input").val('');
			$('.suggestion-row').remove();
			$('#result_div').css("height", "calc(100vh - 220px)");
		}
	};

	$(document).on("click", ".sugg-options", function(event) {
    sendMessage($(event.target).text());
  });

	$("#send-button").click(function() {
    sendMessage($("#chat-input").val());
  });

	$('#chat-input').keyup(function (e) {
    if (e.keyCode === 13) {
			sendMessage($("#chat-input").val());
    }
	});

	// do something when connection closes
	// socket.on('disconnect', function(){});

});
