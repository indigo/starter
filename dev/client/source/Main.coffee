jQuery ->
	@app = window.app ? {}
	users = new @app.Users()
	users.fetch()