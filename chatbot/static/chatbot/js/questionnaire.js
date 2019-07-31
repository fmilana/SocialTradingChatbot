d3.select(window).on("load", function () {

    var log = {};

    var min_text_length = 10;

    // console.log('data:', data);
    data.reverse();
    data.forEach( (item, item_no) => {
        //
        item_no = data.length - item_no - 1;
        var row = d3.select('form')
                    // .append('div')
                    .insert("div",":first-child")
                    // .insert("div",":last-child")
                    .attr('class', 'form-row');
        var col = row.append('div')
                     .attr('class', 'col-12');
        
        if ('label' in item) {
            col.append('span')
               .html(item['label']);
        } else if ('question' in item) {
            var div = col.append('div')
                         .attr('class' , 'form-group');
            
            div.append('label')
            //    .attr('for', ``)
                .html(item['question'])

            if ('choices' in item) {
                // multiple choice question
                item['choices'].forEach( (choice, i) => {
                    var html = `
                    <input class="form-check-input item${item_no}-radios form-control" 
                           type="radio" 
                           name="item${item_no}-radios" 
                           id="item${item_no}-radio${i}" 
                           value="option${i}" 
                           required>
                       <label class="form-check-label" 
                              for="item${item_no}-radio${i}">${choice}</label>`;
                    var item_div = div.append('div')
                       .attr('class', 'form-check')
                       .html(html);
                    if (i === (item.choices.length - 1)) {
                        item_div.append('div')
                                .attr('class', "invalid-feedback")
                                .html('Please select an answer.');
                    }
                });
            } else {
                // open question
                div.append('textarea')
                   .attr('class', 'form-control')
                   .attr('id', `item${item_no}-textarea`)
                   .attr('rows', 3)
                   .attr('required', '');
                div.append('div')
                   .attr('id', `item${item_no}-feedback`)  
                   .attr('class', "invalid-feedback")
                   .html(`Please provide an answer, using at least ${min_text_length} characters.`);
            }
        }
    });

    data.reverse();

    // make the checkboxes valid as soon as one item is selected
    d3.selectAll('.form-check-input')
        .on('click', function (d) {
            // get item_no
            var item = d3.select(this).attr('id').split('-')[0];
            d3.selectAll(`.${item}-radios`).classed('is-invalid', false);
      });
    // 
    // make the textarea valid as soon as min_text_length characters are entered
    d3.selectAll('textarea')
        .on('keyup', function (d) {
            var selected = d3.select(this);
            var text = selected.node().value;
            if (text.trim().length >= min_text_length) {
                selected.classed('is-invalid', false);
            }
      });
    // 

    d3.select('#submit-btn').on('click', function () {
        // calculate task completion time
        var end = performance.now();
        var task_completion_time = end - start;

        console.log('task_completion_time:', task_completion_time);

        // get the form data
        var results = [];
        var errors = false;
        data.forEach( (item, item_no) => {
            if ('label' in item) {
                results.push('');
            } else if ('question' in item) {
                if ('choices' in item) {
                    // multiple choice question
                    var selected = d3.select(`input[name="item${item_no}-radios"]:checked`);
                    if (selected.node() === null) {
                        answer = '';
                        mising_data = true;
                        d3.selectAll(`.item${item_no}-radios`).classed('is-invalid', true);
                        errors = true;
                    } else {
                        var q = 'label[for="' + selected.node().id + '"]';
                        answer = d3.select(q).text();
                    }
                    results.push({
                        question: item.question,
                        answer: answer
                    });
                } else {
                    // open question
                    var selected = d3.select(`#item${item_no}-textarea`);
                    var text = selected.node().value
                    console.log('text:', text);
                    results.push({
                        question: item.question,
                        answer: text
                    });
                    if ( text.length < min_text_length ) {
                        selected.classed('is-invalid', true);
                        errors = true;
                        d3.select(`item${item_no}-feedback`)
                            .style('display', 'block');
                    } else {
                        d3.select(`.item${item_no}-feedback`)
                            .style('display', 'hidden');
                    }
                }
            }
            // d3.selectAll('form')
            //   .classed('was-validated', true);
            console.log(results);
        });

        console.log('errors:', errors);

        event.preventDefault();
        event.stopPropagation();

        if (errors === false) {
            // post data to the server
            var post_url = server_url + "/questionnaire/";
            var post_data = {
                groups: results,
                task_completion_time: task_completion_time,
                log: log
            };
            fetch(post_url, {
                method: 'POST',
                body: JSON.stringify(post_data),
                credentials: 'include',
                headers: {'Content-Type': 'application/json'}
            }).then(res => res.json()).then(response => {
                console.log('POST response:', response);
                console.log('POST response.headers:', response.headers);
                // window.location.replace(server_url + "/tasks/?order=" + next_task_order);
                // window.location = server_url + "/tasks/?order=" + next_task_order;
                window.location = response.completion_url;
            }).catch(err => {
                console.log('POST error:', err);
            });
        }
    });

    var start = performance.now();
        

});


