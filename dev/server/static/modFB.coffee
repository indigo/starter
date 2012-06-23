      

      window.fbAsyncInit = function() {
        FB.init({
          appId      : '463528243676331', // App ID
          channelUrl : 'http://zoe-nicole.appspot.com//channel.html', // Channel File
          status     : true, // check login status
          cookie     : true, // enable cookies to allow the server to access the session
          xfbml      : true  // parse XFBML
        });

        // Additional initialization code here
      };

      window.getFriends = function() {
        FB.api('/me/friends', { limit: 10 }, function(response) {
          for (var i=0, l=response.length; i<l; i++) {
            var post = response[i];
            if (post.name) {
              alert('Message: ' + post.name);
            } else if (post.attachment && post.attachment.name) {
              alert('Attachment: ' + post.attachment.name);
            }
          }
        });
      };

      // Load the SDK Asynchronously
      (function(d){
         var js, id = 'facebook-jssdk', ref = d.getElementsByTagName('script')[0];
         if (d.getElementById(id)) {return;}
         js = d.createElement('script'); js.id = id; js.async = true;
         js.src = "//connect.facebook.net/en_US/all.js";
         ref.parentNode.insertBefore(js, ref);
       }(document));

       onLogin = function() {
         FB.login(function(response) {
           if (response.authResponse) {
             console.log('Welcome!  Fetching your information.... ');
             FB.api('/me', function(response) {
               console.log('Good to see you, ' + response.name + '.');
             });
           } else {
             console.log('User cancelled login or did not fully authorize.');
           }
         });
       };

       onLogout = function() {
        FB.logout(function(response) {
          // user is now logged out
        });
       };