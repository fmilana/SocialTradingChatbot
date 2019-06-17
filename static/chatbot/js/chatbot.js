var newspostCounter = 0;

var newsposts = JSON.parse(newsposts_list.replace(/&quot;/g, '"'));
var profiles = JSON.parse(profiles_list.replace(/&quot;/g, '"'));

var updateNewsposts = setInterval(function() {

  if (newspostCounter > 8) {
    clearInterval(updateNewsposts);
  }

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
        <div class="head"> \
            <p>' + text + '</p> \
        </div> \
      </div> \
    </div> \
  </div>';

  $('.scrollable-newsposts').append(div);

  $('.scrollable-newsposts').scrollTop($('.scrollable-newsposts')[0].scrollHeight);

  newspostCounter++;
}, 1000);
