jQuery ->
	@app = window.app ? {}
	@app.Users = new @app.Users()
	usersView = new @app.UsersView
		collection: @app.Users
		el: $('#content')	
	console.log @app.Users
