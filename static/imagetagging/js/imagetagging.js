$(function () {

    var _task

    var render_tagging_task = function () {
        // var image_url = server_url + '/imagetagging/static/' + _task.image_url;
        var image_url = server_url + '/static/' + _task.image_url;

        console.log(image_url);
        $('.tagging img').attr("src", image_url);
        $('.found-tags-list').empty();
        _task.tags.forEach(element => {
            $('.found-tags-list').append(element + '; ');
        });
        if (_task.tags.length === 0) {
            $('.found-tags-list').append('none so far.');
        }
        if (_task.tags.length === 3) {
            // disable button
            $('.btn-check-tag').prop('disabled', true);
            $('.input-tag').prop('disabled', true);
            $('.found-tags-list').append('all tags found!');
            $('.input-tag').attr('placeholder', 'all tags already found!');
            // load_results();
        } else {
            $('.btn-check-tag').prop('disabled', false);
            $('.input-tag').prop('disabled', false);
            $('.input-tag').attr('placeholder', 'please enter a tag');
        }
        $('.loading').hide();
    };

    var load_tagging_task = function (task_id) {
        console.log('load_tagging_task');
        var url = server_url + '/imagetagging/image-task/';

        if (task_id) {
            url = url + task_id + '/';
        }

        console.log('url:', url);

        $.ajax({
            type: "GET",
            url: url,
            success: function (task_data) {
                console.log(task_data);
                _task = task_data;
                render_tagging_task();
            }
        });

    };

    $('.btn-check-tag').click(function () {
        // check the tag for this task
        var tag_text = $('.input-tag').val(),
            url = server_url + '/imagetagging/tags/',
            post_data = {
                'image_task': _task.id,
                'label': tag_text,
                'csrfmiddlewaretoken': getCookie('csrftoken')
            };
        $.ajax({
            type: "POST",
            url: url,
            data: post_data,
            success: function (response) {
                console.log(response);
                if (response.correct) {
                    _task.tags.push(tag_text);
                    render_tagging_task();
                    $('.input-tag').val('');
                } else {
                    // TODO: blink incorrect
                    $('.input-tag').popover('show');
                }
                if (response.complete) {
                    // load_results();
                }
            }
        });
    });

    $('.input-tag').keypress(function() {
        $('.input-tag').popover('hide');
    });

    $('.btn-next-image').click(function () {
        console.log('clicked');
        load_tagging_task(_task.next_task);
    });




    // function to retrieve cookie (from django)
    var getCookie = function(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    };

    load_tagging_task();
});
