$(function () {

  $('input#consentCheck').click(function () {
    $('button#startButton').prop('disabled', function(i, v) { return !v; });

  });

  $('button#startButton').click(function () {
    window.location.href = "/chatbot";
  });
});
