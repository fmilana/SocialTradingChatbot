$(function() {
  if (window.location.pathname == "/") {
    $('.navbar').hide();
  }
});


$(function() {
  $("#imagetagging-button").click(function () {
      $("#investment-button").removeClass('active');
      $(this).addClass('active');
      $(".content-container").hide();
      $('#image-tagging-area').css('display', 'inline-block');
  });

  $("#investment-button").click(function () {
      $("#imagetagging-button").removeClass('active');
      $(this).addClass('active');
      $("#image-tagging-area").hide();
      $(".content-container").show();
  });
});
