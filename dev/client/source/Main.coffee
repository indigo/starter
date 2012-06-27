# A minimalist main

jQuery ->
	window.fbAsyncInit = () ->
		FB.init
			appId      : '463528243676331',                             # App ID
			channelUrl : 'http://zoe-nicole.appspot.com//channel.html', # Channel File
			status     : true,                                          # check login status
			cookie     : true,                                          # enable cookies to allow the server to access the session
			xfbml      : true                                           # parse XFBML

	window.getFriends = () ->
		FB.api '/me/friends', { limit: 10 }, (response) ->
			alert r for r in response

	do
		->
			$('#facebook-jssdk').attr
				'src':'http://connect.facebook.net/en_US/all.js'
				'async':'async'

	$("#fblogin").click () ->
		FB.login (response) ->
			if (response.authResponse)
				console.log('Welcome!  Fetching your information.... ')
				FB.api '/me', (response) ->
					console.log('Good to see you, ' + response.name + '.')
			else 
				console.log('User cancelled login or did not fully authorize.')

	$("#fblogout").click () ->
		FB.logout () ->
			console.log 'logged out'
