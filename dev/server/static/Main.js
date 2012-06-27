(function() {

  jQuery(function() {
    window.fbAsyncInit = function() {
      return FB.init({
        appId: '463528243676331',
        channelUrl: 'http://zoe-nicole.appspot.com//channel.html',
        status: true,
        cookie: true,
        xfbml: true
      });
    };
    window.getFriends = function() {
      return FB.api('/me/friends', {
        limit: 10
      }, function(response) {
        var r, _i, _len, _results;
        _results = [];
        for (_i = 0, _len = response.length; _i < _len; _i++) {
          r = response[_i];
          _results.push(alert(r));
        }
        return _results;
      });
    };
    (function() {
      return $('#facebook-jssdk').attr({
        'src': 'http://connect.facebook.net/en_US/all.js',
        'async': 'async'
      });
    })();
    $("#fblogin").click(function() {
      return FB.login(function(response) {
        if (response.authResponse) {
          console.log('Welcome!  Fetching your information.... ');
          return FB.api('/me', function(response) {
            return console.log('Good to see you, ' + response.name + '.');
          });
        } else {
          return console.log('User cancelled login or did not fully authorize.');
        }
      });
    });
    return $("#fblogout").click(function() {
      return FB.logout(function() {
        return console.log('logged out');
      });
    });
  });

}).call(this);
