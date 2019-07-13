$(document).ready(function() {
  var isPaused = false;

  var _seconds_left = 180;

  var update_timer = function () {
    if (!isPaused) {
      var seconds,
          minutes,
          html;
      _seconds_left -= 1;
      if (_seconds_left < 1) {
          _seconds_left = 180;

          isPaused = true;
          clearTimeout(newspostTimeout);

          $('#myModal').modal({
            backdrop: 'static',
            keyboard: false
          });

          $.ajax({
              type: "GET",
              url: server_url + '/updatemonth/',
              success: function (response) {
                  console.log(response);
                  if (response.increased) {

                    $('#month-number').html(response.month);

                  } else {

                  }
              }
          });

          $.ajax({
              type: "GET",
              url: server_url + '/updateportfolios/',
              success: function (response) {
                  console.log(response);

                  if (!$('#loading-gif').length) {
                    $('.scrollable-newsposts').append('<img id="loading-gif" src="' + staticUrl + 'chatbot/images/loading.gif">');
                  }

                  $("#portfolios").load(location.href+" #portfolios>*","");
                  $('#invested-balance-amount').html(response.invested_balance_amount);
              }
          });

          $('.scrollable-newsposts').empty();
          newspostCounter = 0;

          $('#ok-button').on('click', function() {
            isPaused = false;
          });
      }
      minutes = Math.floor(_seconds_left / 60);
      minutes = minutes.toLocaleString('en', {'minimumIntegerDigits': 2});
      seconds = _seconds_left % 60;
      seconds = seconds.toLocaleString('en', {'minimumIntegerDigits': 2});
      text = minutes + ':' + seconds;
      $('#timer').text(text);
    } else {
      console.log("IS PAUSED");
    }
  };

  window.setInterval(update_timer, 1000);
  update_timer();


  function shuffle(array) {
    var currentIndex = array.length, temporaryValue, randomIndex;

    // While there remain elements to shuffle...
    while (0 !== currentIndex) {

      // Pick a remaining element...
      randomIndex = Math.floor(Math.random() * currentIndex);
      currentIndex -= 1;

      // And swap it with the current element.
      temporaryValue = array[currentIndex];
      array[currentIndex] = array[randomIndex];
      array[randomIndex] = temporaryValue;
    }

    return array;
  }

  $('.scrollable-newsposts').append('<img id="loading-gif" src="' + staticUrl + 'chatbot/images/loading.gif">');

  var newsposts = shuffle(JSON.parse(newsposts_list.replace(/&quot;/g, '"')));
  var profiles = JSON.parse(profiles_list.replace(/&quot;/g, '"'));

  var newspostTimeout;
  var newspostCounter = 0;

  function updateNewsposts() {

    if (!isPaused) {
      if (newspostCounter > 8) {
        clearInterval(updateNewsposts);
      }

      $('#loading-gif').remove();

      var newspost = newsposts[newspostCounter];
      var profile = profiles[newspost.fields.profile - 1];
      var name = profile.fields.name;
      var text = newspost.fields.text;

      var div = '<div class="wrapper-newspost"> \
        <div class="container-newspost"> \
          <div class="img-container-newspost"> \
            <img class="card-img" src= "' + staticUrl + 'chatbot/images/profiles/' +  name.replace(' ', '-') + '.jpg" alt="' + name + ' image"> \
          </div> \
          <div class="content-newspost"> \
            <div> \
                <p id="text-newspost"><strong>' + text + '</strong></p> \
            </div> \
          </div> \
        </div> \
      </div>';

      $('.scrollable-newsposts').append(div);

      if (newspostCounter < 9) {
        $('.scrollable-newsposts').append('<img id="loading-gif" src="' + staticUrl + 'chatbot/images/loading.gif">');
      }

      $('.scrollable-newsposts').scrollTop($('.scrollable-newsposts')[0].scrollHeight);

      newspostCounter++;

      var min = 10;
      var max = 20;

      var rand = Math.floor(Math.random() * (max - min + 1) + min);

      newspostTimeout = setTimeout(updateNewsposts, rand * 1000);
    }
  };

  setTimeout(updateNewsposts, 10000);
});



// chat
$(document).ready(function() {

	var mybot = '<div class="chatCont" id="chatCont">'+
								'<div id="result_div" class="resultDiv"></div>'+
								'<div class="chatForm" id="chat-div">'+
									'<input type="text" class="col-10" id="chat-input" autocomplete="off" placeholder="Type something..."'+ 'class="form-control bot-txt"/>'+
									'<button id="send" class="col-2">send</button>' +
								'</div>'+
							'</div>';

	$("mybot").html(mybot);

});
