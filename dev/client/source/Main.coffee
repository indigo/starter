jQuery ->
	@app = window.app ? {}
	users = new @app.Users()
	users.fetch()
	console.log users.toJSON()
	@app.users = users