jQuery ->

	class Save extends Backbone.Model
		localStorage: new Store("Save")

	save = new Save 
		id:777

	save.fetch()
	if save.has 'userid'
		console.log('Welcome!  Fetching your information.... ')
		console.log save.get 'userid'
	else
		save.save({userid: '12'})
		console.log('saving somewhere')

	class Game extends Backbone.Model

	class Games extends Backbone.Collection
		model: Game

	class GameView extends Backbone.View
		tagname: 'li'
		@model.bind 'change', @render

		render: =>
			$(@el).html """
					<span>#{@model.get 'part1'} #{@model.get 'part2'}!</span>
					<span class='view'>view</span>
						"""
			@

	class MainView extends Backbone.View
		el: $ 'body'

		initialize: ->
			_.bindAll @
			@collection = new Games
			@collection.bind ''
			@render()

		render: ->
			$(@el).append ('<ul><li>Welcome!  Fetching your information.... </li></ul>')