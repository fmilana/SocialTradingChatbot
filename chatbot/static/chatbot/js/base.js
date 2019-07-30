$(document).ready(function() {
  if (window.location.pathname == "/" || window.location.pathname == "/information/" || window.location.pathname == "/consent/" || window.location.pathname == "/results/") {
    $('.navbar').hide();
  }
});

var contentHeight = $(".content-container").height();

$(function() {
  $("#imagetagging-button").click(function () {
      $("#investment-button").removeClass('active');
      $(this).addClass('active');
      // $(".content-container").hide();
      $(".content-container").css('opacity', '0');
      $(".content-container").css('height', '0');
      $('#image-tagging-area').css('display', 'inline-block');
      // $('.notification').css('display', 'inline-block');
  });

  $("#investment-button").click(function () {
      $("#imagetagging-button").removeClass('active');
      $(this).addClass('active');
      $("#image-tagging-area").hide();
      $('.notification').hide();
      // $(".content-container").show();
      $(".content-container").css('opacity', '100');
      $(".content-container").css('height', contentHeight);
  });
});
