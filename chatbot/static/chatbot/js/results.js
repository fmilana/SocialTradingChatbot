$(function () {
  var load_final_result = function () {
    $.ajax({
      type: "GET",
      url: server_url + '/shop/calculate_result/',
      success: function (participant_data) {
        // console.log(participant_data);
        $('.loading').hide();
        render_final_results(participant_data);
      }
    });
  };

  var load_results = function () {
    $.ajax({
      type: "GET",
      url: server_url + '/study/participant/',
      success: function (participant_data) {
        // console.log(participant_data);
        $('.loading').hide();
        render_results(participant_data);
      }
    });
  };

  var render_results = function (participant_data) {
    $('.results .tasks_completed').replaceWith('<span class="tasks_completed">' + participant_data.tasks_completed + '</span>');
    $('.results .initial_budget').replaceWith('<span class="initial_budget">' + participant_data.initial_budget.toFixed(2) + '</span>');
    $('.results .budget').replaceWith('<span class="budget">' + participant_data.budget.toFixed(2) + '</span>');
    $('.results .earned').replaceWith('<span class="earned">' + participant_data.earned.toFixed(2) + '</span>');
    $('.results .spent').replaceWith('<span class="spent">' + participant_data.spent.toFixed(2) + '</span>');
  };

  var render_final_results = function (participant_data) {
    $('.results .penalty').replaceWith('<span class="penalty">' + participant_data.penalty.toFixed(2) + '</span>');
    $('.results .final_bonus').replaceWith('<span class="final_bonus">' + participant_data.final_bonus.toFixed(2) + '</span>');
  };

  load_final_result();
  load_results();
});
