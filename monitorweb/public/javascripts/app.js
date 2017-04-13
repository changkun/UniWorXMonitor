function getUsers() {
  $('.users ul').empty();
  $('input').val('');
  $.get('/users', function(data) {
    data.users.forEach(function(user) {
      $('.users ul').append('<li>'+user+'</li>');
    });
  });
}
function setResponse(res) {
  $('.response .status').text(res.status);
  $('.response .info').text(res.info);
}
function subscribe() {
  $('#sub').on('click', function() {
    $.post('/users/add', {
      'email': $('#email').val()
    }, function(data) {
      getUsers();
      setResponse(data);
    });
  });
}
function unsubscribe() {
  $('#unsub').on('click', function() {
    $.post('/users/del', {
      'email': $('#email').val()
    }, function(data) {
      getUsers();
      setResponse(data);
    });
  });
}
function setup() {
  getUsers();
  subscribe();
  unsubscribe();
}
setup();