jQuery ->
	@app = window.app ? {}
	users = new @app.Users()
	users.bind 'add', -> console.log 'test'
	users.fetch()
	console.log users
	@app.users = users