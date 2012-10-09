# Views
@app = window.app ? {}

class GameView extends Backbone.View
	tagname: 'li'

class UserView extends Backbone.View
	tagname: 'li'	
	render: ->
		content = @model.get('alias')
		$(@el).html(content)
		@el

class UsersView extends Backbone.View
	initialize: ->
		@input = @$('#new-user')
		@collection.bind 'add', @addOne
		@collection.bind 'refresh', @addAll
		@collection.bind 'reset', @addAll
		@collection.fetch()
	addOne: (user) =>
		console.log user
		view = new UserView(model: user)
		@$('#user-list').append(view.render())
	addAll: =>
		@collection.each @addOne

class  MatchView extends Backbone.View

class MainView extends Backbone.View
	el: $ 'body'

	initialize: ->
		_.bindAll @
		@collection = new Games
		@collection.bind ''
		@render()

	render: ->
		$(@el).append ('<ul><li>Welcome!  Fetching your information.... </li></ul>')

@app.UsersView = UsersView