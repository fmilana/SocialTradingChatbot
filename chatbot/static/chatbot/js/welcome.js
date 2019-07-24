$(function () {

  $('input#consentCheck').click(function () {
    $('button#startButton').prop('disabled', function(i, v) { return !v; });

  });

  // $('button#startButton').click(function () {
  //   window.location.href = "/chatbot";
  // });

  $('button#startButton').click(function () {
    // var username = $('#usernameInput').val();

    searchParams = new URLSearchParams(window.location.search);
    username = searchParams.get('PROLIFIC_PID');
    console.log('username:', username);
    $.ajax({
      type: "POST",
      url: server_url + '/participants/',
      data: {'username': username},
      success: function () {
        console.log('username:', username);
        // window.location.href = server_url + "/tasks/";
        window.location.href = server_url + "/chatbot";
      },
      error: function (data, msg, reason) {
        console.log('error arguments', data.responseJSON);
        if (data.responseJSON.username.length > 0) {
          if (data.responseJSON.username[0].code === 'duplicate') {
            var message = `It looks like you already took part in this study once. Unfortunately, you can only take part in the study once.`;
            bootbox.alert(message);
          }
        }
      }
    });
  });

});
