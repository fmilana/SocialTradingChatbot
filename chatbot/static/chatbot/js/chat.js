// var socket = require('socket.io-client')('http://localhost:5500');

$(document).ready(function() {

	var adviceCountdown = 30;

	adviceCountdownInterval = setInterval(function() {
		if (adviceCountdown > 0) {
			adviceCountdown -= 1;
		} else {
			sendMessage("Give me some advice", true);
			adviceCountdown = 30;
		}
	}, 1000);

	function appendInitialBotMessages() {
		setTimeout(function(){
			$('#result_div').append('<img id="typing-gif" src="' + staticUrl + 'chatbot/images/typing.svg">');
		}, 500);

		setTimeout(function() {
			$('#result_div #typing-gif').remove();
			$('#result_div').append("<p id='bot-message'>Hi there!</p><br>");
		}, 1500);

		setTimeout(function() {
			$('#result_div').append('<img id="typing-gif" src="' + staticUrl + 'chatbot/images/typing.svg">');
		}, 2000);

		setTimeout(function() {
			$('#result_div #typing-gif').remove();
			$('#result_div').append("<p id='bot-message'>You can tell me to follow or unfollow portfolios, add or withdraw amounts and ask me things like: \"Should I invest 50 in ralph?\" or \"Who should I unfollow?\". I'm here to give you accurate predictions!</p><br>");
		}, 4000);

		setTimeout(function () {
      $('<div class="row suggestion-row"></div>').appendTo('#result_div');
      $('<p class="sugg-options">Give me some advice</p>').appendTo('.suggestion-row');
			$('<p class="sugg-options">Who should I follow?</p>').appendTo('.suggestion-row');

			suggestionRowHeight = $('.suggestion-row').height();
      resultDivHeight = $(window).height() - (215 + suggestionRowHeight);

			$('#result_div').css("height", resultDivHeight);
      $('#result_div').scrollTop($('#result_div')[0].scrollHeight);
    }, 4500);
	}

	appendInitialBotMessages();

	function appendBotMessage(data, periodicAdvice) {
    var message = data['text'];

		$('#typing-gif').remove();

		console.log('periodicAdvice = ' + periodicAdvice);
		console.log('message = ' + message);

		$('#result_div_notification #typing-gif').remove();

		if (!periodicAdvice || message != "You're doing great! I don't think you should follow or unfollow anyone else this month.") {
			if (periodicAdvice && $('#image-tagging-area').is(':visible')) {
				$('.notification').hide();
				$('#result_div_notification #bot-message').remove();
				$('#result_div_notification #user-message-notification').remove();
				$('#result_div_notification br').remove();
				$('.notification').css('display', 'inline-block');
			}

			$("#result_div").append("<p id='bot-message'>" + message + "</p><br>");
			$("#result_div_notification").append("<p id='bot-message'>" + message + "</p><br>");
			$('#result_div_notification #typing-gif').remove();

	    buttons = data['buttons'];

			if (typeof buttons !== 'undefined') {
				addSuggestion(buttons);
			}

			$('#result_div').scrollTop($('#result_div')[0].scrollHeight);

			$('#result_div_notification').scrollTop($('#result_div')[0].scrollHeight);
		}

		adviceCountdown = 30;
  }

  	// event when bot utters message
	function process_response(data, periodicAdvice) {
    data = data[0];
		console.log(data);

		appendBotMessage(data, periodicAdvice);

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

		$.ajax({
				type: "GET",
				url: server_url + '/updatebalances/',
				success: function (response) {
						console.log(response);

						$('#available-balance-amount').html(response.available_balance_amount);
						$('#invested-balance-amount').html(response.invested_balance_amount);

				}
		});

		adviceCountdown = 30;
	}

  function addSuggestion(suggestions) {
    setTimeout(function () {

			$('.suggestion-row-notification').remove();

			$('<div class="row suggestion-row-notification"></div>').appendTo('#result_div_notification');
    	$('<div class="row suggestion-row"></div>').appendTo('#result_div');

			var addSuggestions = true;

			for (i = 0; i < suggestions.length; i++) {
				if (suggestions[i].title == "Give me some advice") {
					addSuggestions = false;
					setTimeout(function() {
						$('.notification').fadeOut("slow", function() {
							//Stuff to do *after* the animation takes place
						})
					}, 500);
				}
			}

      // Loop through suggestions
      for (i = 0; i < suggestions.length; i++) {
        $('<p class="sugg-options">' + suggestions[i].title + '</p>').appendTo('.suggestion-row');
				if (addSuggestions) {
					console.log('adding notifications');
					$('<p class="sugg-options-notification">' + suggestions[i].title + '</p>').appendTo('.suggestion-row-notification');
				}
			}

			suggestionRowHeight = $('.suggestion-row').height();
    	resultDivHeight = $(window).height() - (215 + suggestionRowHeight);
			$('#result_div').css("height", resultDivHeight);
      $('#result_div').scrollTop($('#result_div')[0].scrollHeight);

			if (addSuggestions) {
				suggestionRowNotificationHeight = $('.suggestion-row-notification').height();
				resultDivNotificationHeight = $('.notification').height() - (90 + suggestionRowNotificationHeight);
				$('#result_div_notification').css("height", resultDivNotificationHeight);
	      $('#result_div_notification').scrollTop($('#result_div')[0].scrollHeight);
			}
    }, 500);
  }

	var sendMessage = function(message, periodicAdvice) {
		console.log(message);
		if (message) {
      //socket.emit('user_uttered', {'message': chatInput, 'sender': 'rasa'});
			var post_url = server_url + '/chatbotproxy/';
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
				process_response(response, periodicAdvice);
			}).catch(error => {
				console.log('POST error:', error);
			});

			if (!periodicAdvice) {
				$("#result_div").append("<p id='user-message'> " + message + "</p><br>");
				$('#result_div').scrollTop($('#result_div')[0].scrollHeight);
				$("#chat-input").val('');

				if ($("#result_div_notification").is(':visible')) {
					$("#result_div_notification").append("<p id='user-message-notification'> " + message + "</p><br>");
					$('#result_div_notification').scrollTop($('#result_div_notification')[0].scrollHeight);
					$("#chat-input-notification").val('');
				}
			}
			setTimeout(function(){
				$('#result_div').append('<img id="typing-gif" src="' + staticUrl + 'chatbot/images/typing.svg">')
				console.log('appending gif........');
				$('#result_div').scrollTop($('#result_div')[0].scrollHeight);

				$('#result_div_notification').append('<img id="typing-gif" src="' + staticUrl + 'chatbot/images/typing.svg">')
				$('#result_div_notification').scrollTop($('#result_div_notification')[0].scrollHeight);
			}, 500);

      $('.suggestion-row').remove();
			$('.suggestion-row-notification').remove();
			$('#typing-gif').remove();

      $('#result_div').css("height", "calc(100vh - 220px)");
			$('#result_div_notification').css("height", "220px");
		}

		adviceCountdown = 30;
	};

  $(document).on("click", ".sugg-options", function(event) {
    sendMessage($(event.target).text(), false);
  });

	$(document).on("click", ".sugg-options-notification", function(event) {
    sendMessage($(event.target).text(), false);
  });

  $("#send-button").click(function() {
    sendMessage($("#chat-input").val(), false);
  });

	$("#send-button-notification").click(function() {
    sendMessage($("#chat-input-notification").val(), false);
  });

	$('#chat-input').keyup(function (e) {
    if (e.keyCode === 13) {
			sendMessage($("#chat-input").val(), false);
    }
	});

	$('#chat-input-notification').keyup(function (e) {
    if (e.keyCode === 13) {
			sendMessage($("#chat-input-notification").val(), false);
    }
	});

	$('#close-button').click(function() {
		$('.notification').hide();
	});
});
