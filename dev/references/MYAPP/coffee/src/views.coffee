# Views
jQuery ->
	@app = window.app ? {}

	class MainView extends Backbone.View
		el: '#content'

		initialize: (options) ->
			@collection.bind 'reset', @render, @
			@collection.bind 'add', @render, @
			@collection.bind 'change', @render, @

		render: ->
			$(@el).empty()
			for rsc in @collection.models
				simpleRessourceView = new SimpleRessourceView model: rsc
				$(@el).append simpleRessourceView.render().el
			@

		createNew: (attributes)->
			@collection.create attributes

		addValue: (name, value)->
			updatedrsc = rsc.set({value: rsc.get('value') + value}) for rsc in @collection.models when rsc.get('title') is name
			if updatedrsc then updatedrsc.save()
			updatedrsc

	class SimpleRessourceView extends Backbone.View
		className: 'SimpleRessourceView'
		tagName: 'li'
		template: _.template($('#simple-ressource-template').html())
		render: ->
			$(@el).html @template(@model.toJSON())
			@

	class ActionPanelView extends Backbone.View
		el: '#panel'
		tagName: 'li'
		#template: _.template( $('#Action-Template').html())

		initialize: (options) ->
			@inventory = options.inventory
			@level = options.bars
			@inventory.bind 'change', @render, @
			@inventory.bind 'add', @render, @
			@inventory.bind 'reset', @render, @
			@collection.bind 'change', @onAdd, @
			@collection.bind 'add', @onAdd, @
			@collection.bind 'destroy', @render, @
			@collection.bind 'tick', @render, @
			@collection.bind 'reset', @reloadActions, @
			#@renderAction(a, actionID) for actionID, a of @level.getAllBars()
			#actionView = new ActionView collection: @collection, level: @level, actionID: k
			@actionViews = (new ActionView collection: @collection, level: @level, actionID: k for k, a of @level.getAllBars())
		
		render: (options) =>
			$(@el).empty()
			#@renderAction(a, actionID) for actionID, a of @level.getAllBars()
			$(@el).append actionView.render().el for actionView in @actionViews
			@

		onAdd: (e) ->
			console.log "onAdd", e

			@render()

		renderAction: (a, k) ->
			#$(@el).append @template action
			actionView = new ActionView collection: @collection, level: @level, actionID: k
			$(@el).append actionView.render().el

		reloadActions: () ->
			@collection.reloadActions()

	class ActionView extends Backbone.View
		className: 'ActionView'
		tagName: 'li'
		template:
			template_Possible: _.template($('#ActionView-template').html())
			template_Impossible: _.template($('#ActionView-template-impossible').html())
		template_running: _.template($('#ActionView-template-running').html())
		events:
			'click .clickable': 'startAction'

		initialize: (options) ->
			@collection.bind 'tick', @timeleftUpdate, @
			@level = options.level
			@actionID = options.actionID
			@action = @level.getBar @actionID

		timeleftUpdate: (actionID, timeleft) ->
			if @actionID is actionID
				@timeleft = timeleft
				console.log "#{actionID} #{timeleft} "
			@render()

		render: () =>
			if @timeleft?
				@mergedAttributes = _.extend(_.clone(@action), { timeleft: Math.round( @timeleft/1000 ) })
			else
				@mergedAttributes = _.extend(_.clone(@action), { timeleft: 1})
			#running = (m.attributes.actionID for m in @collection.models)
			if @actionID in @collection.running()
				#console.log "template_running #{@actionID}"
				$(@el).html @template_running(@mergedAttributes)
			else
				#console.log "template_#{@action.check()} #{@actionID}"
				@mergedAttributes.duration = Math.round(@mergedAttributes.duration())
				$(@el).html @template["template_#{@action.check()}"](@mergedAttributes)
				$(@el).attr('action-id', @action.id)
			@delegateEvents()
			@

		startAction: (e) ->
			@timeleft = @action.duration() * 1000
			@collection.start @actionID
			@render()

	@app.MainView = MainView
	@app.ActionPanelView = ActionPanelView
