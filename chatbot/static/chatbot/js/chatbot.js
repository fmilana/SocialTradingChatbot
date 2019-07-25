$(document).ready(function() {
  $('#parentheses').hide()

  var isPaused = false;

  var _seconds_left = 300;

  var newspostTimeout;

  var update_timer = function() {
    if (!isPaused) {
      var seconds,
          minutes,
          html;
      _seconds_left -= 1;
      if (_seconds_left < 1) {
          _seconds_left = 300;

          old_invested_amount = parseFloat($('#invested-balance-amount').text());

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

                    $('#result_div').append('<row><p id="month-chat">Month: ' + response.month + '/5</p></row>')
                    $('#result_div').scrollTop($('#result_div')[0].scrollHeight);

                  } else {
                    $('#result_div').append('<row><p id="month-chat">Month: ' + response.month + '/5</p></row>')
                    $('#result_div').scrollTop($('#result_div')[0].scrollHeight);
                  }

                  $('.last-change').show();
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

                  $('#invested-balance-amount').html((Math.round(response.invested_balance_amount * 100) / 100).toFixed(2));

                  new_invested_amount = parseFloat($('#invested-balance-amount').text());
                  new_invested_amount = parseFloat(Math.round(new_invested_amount * 100) / 100).toFixed(2);

                  span = $('#invested-balance-change');

                  string = '';

                  if (old_invested_amount == 0) {
                    string = '+0.00%';
                    span.removeClass('positive-change');
                    span.removeClass('negative-change');
                    span.addClass('no-change');

                  } else {
                    invested_balance_change = 100 * (new_invested_amount - old_invested_amount) / old_invested_amount;
                    invested_balance_change = parseFloat(Math.round(invested_balance_change * 100) / 100).toFixed(2);

                    console.log('invested balance change = ' + invested_balance_change);

                    if (invested_balance_change > 0) {
                      string = '+' + invested_balance_change + '%';
                      span.removeClass('negative-change');
                      span.removeClass('no-change');
                      span.addClass('positive-change');
                    } else if (invested_balance_change == 0) {
                      string = '+0.00%';
                      span.removeClass('positive-change');
                      span.removeClass('negative-change');
                      span.addClass('no-change');
                    } else {
                      string = invested_balance_change + '%';
                      span.removeClass('positive-change');
                      span.removeClass('no-change');
                      span.addClass('negative-change');
                    }
                  }

                  console.log('invested balance change string = ' + string);

                  span.text(string);
                  $('#parentheses').show();
              }
          });

          $('.scrollable-newsposts').empty();
          newspostCounter = 0;

          $('#ok-button').unbind().on('click', function() {
            isPaused = false;

            setNewspostTimer();
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

  newsposts = shuffle(JSON.parse(newsposts_list.replace(/&quot;/g, '"')));
  profiles = JSON.parse(profiles_list.replace(/&quot;/g, '"'));

  newspostCounter = 0;

  function updateNewsposts() {

    if (newspostCounter < 10) {
      if (newspostCounter > 8) {
        clearTimeout(newspostTimeout);
      }

      $('#loading-gif').remove();

      newspost = newsposts[newspostCounter];
      profile = profiles[newspost.fields.profile - 1];
      name = profile.fields.name;

      $.ajax({
          type: "GET",
          url: server_url + '/getnextchanges/',
          success: function (response) {

            // chatbot_change = (Math.round(response[profile.fields.name + '-chatbot-change'] * 100) / 100).toFixed(2)
            newspost_change = (Math.round(response[profile.fields.name + '-newspost-change'] * 100) / 100).toFixed(2)

            text = '';

            // var change_to_consider;
            //
            // if (newspost_accurate) {
            //   change_to_consider = next_change;
            // } else {
            //   change_to_consider = fake_change;
            // }

            newspost_change = Math.abs(Math.round(newspost_change))

            // newspost text based on change value and accuracy
            if (newspost_change > 0) {
              text = name + '\'s portfolio to increase by ~' + newspost_change + '%.';
            } else if (newspost_change == 0) {
              text = name + '\'s portfolio to stay the same.';
            } else {
              text = name + '\'s portfolio to decrease by ~' + newspost_change + '%.';
            }

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



            if (newspostCounter < 9) {
              setNewspostTimer();
            }

            newspostCounter++;
          }
      });
    }
  };


  function setNewspostTimer() {
    var min = 10;
    var max = 20;

    var rand = Math.floor(Math.random() * (max - min + 1) + min);

    clearTimeout(newspostTimeout);
    newspostTimeout = setTimeout(updateNewsposts, rand * 1000);

    console.log('NEXT NEWSPOST TIMEOUT SET AS ' + rand);
  }

  var mybot = '<div class="chatCont" id="chatCont">'+
								'<div id="result_div" class="resultDiv"></div>'+
								'<div class="chatForm input-group" id="chat-div">'+
									'<input type="text" class="col-10 form-control input-sm" id="chat-input" autocomplete="off" placeholder="Type something..."'+ 'class="form-control bot-txt"/>'+
									'<button id="send-button" class="col-2 btn btn-dark btn-sm">Send</button>' +
								'</div>'+
							'</div>';

	$("mybot").html(mybot);


  setNewspostTimer();
  console.log('timout SET!');


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

function gauss(stdev) {
  var r = 0;
  for (var i = 10; i > 0; i --){
      r += Math.random();
  }

  var value = (r / 10) * stdev;

  if (value <= -100) {
    value = -99;
  } else if (value >= 100) {
    value = 99;
  }

  return value;
}
