// var socket = require('socket.io-client')('http://localhost:5500');

$(document).ready(function() {

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
			$('<p class="sugg-options">Who should I stop following?</p>').appendTo('.suggestion-row');

			suggestionRowHeight = $('.suggestion-row').height();
      resultDivHeight = $(window).height() - (215 + suggestionRowHeight);

			$('#result_div').css("height", resultDivHeight);
      $('#result_div').scrollTop($('#result_div')[0].scrollHeight);
    }, 4500);
	}

	appendInitialBotMessages();

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

	// // console log when socket connects to port 5500
	// socket.on('connect', function() {
	// 	console.log('connection established...')
	// });

	// socket.emit('user_uttered', {'message': 'hey', 'sender': 'rasa'});

  	// event when bot utters message
	function process_response (data) {
    data = data[0];
		console.log(data);

		appendBotMessage(data);

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

  function addSuggestion(suggestions) {
    setTimeout(function () {
      $('<div class="row suggestion-row"></div>').appendTo('#result_div');
      // Loop through suggestions
      for (i = 0; i < suggestions.length; i++) {
        $('<p class="sugg-options">' + suggestions[i].title + '</p>').appendTo('.suggestion-row');
      }

      suggestionRowHeight = $('.suggestion-row').height();
      resultDivHeight = $(window).height() - (215 + suggestionRowHeight);

			$('#result_div').css("height", resultDivHeight);
      $('#result_div').scrollTop($('#result_div')[0].scrollHeight);
    }, 500);
  }

  // $('.sugg-options').click(function(event) {
  //   var suggestionText = $(event.target).text();
  //   console.log('suggestiontext = ' + suggestionText);
  //
  //   sendMessage(suggestionText);
  // });

	var sendMessage = function(message) {
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

});
