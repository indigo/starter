# MODELS
# title, value
@app = window.app ? {}

class Ressource extends Backbone.Model

class Inventory extends Backbone.Collection
	model: Ressource
	localStorage: new Store("Inventory")
	getRessource: (name) ->
		for i in @models
			if name is i.get('title')
				return i
	getValue: (name) ->
		@getRessource(name)?.get('value')
	atLeast: (name, value) ->
		@getValue(name) >= value
	has: (name) ->
		for i in @models
			if name is i.get('title')
				return true
		false

	updateValue: (name, value) ->
		if not @has name
			@create
				title: name
				value: value
		else
			@updateExistingValue(name, value)

	updateExistingValue: (name, value) ->
			updatedrsc = rsc.set({value: rsc.get('value') + value}) for rsc in @models when rsc.get('title') is name
			if updatedrsc then updatedrsc.save()
			updatedrsc

# actionID title time
class Action extends Backbone.Model

class Log extends Backbone.Collection
	model: Action
	localStorage: new Store("Log")
	
	initialize: (options) ->
		@level = options.ld
		@level.loadLD @
	
	getLDByActionID: (actionID) ->
		@level.getBar(actionID)

	start: (actionID) ->
		console.log "Start action #{actionID}, saved to the localstore"
		#LEVEL DESIGN COST
		@getLDByActionID(actionID).cost()
		@create
			time: new Date().getTime()
			actionID: actionID
		timeleft =  @getLDByActionID(actionID).duration() * 1000
		@stepAction timeleft, actionID
	
	setFinish: (actionID) ->
		m = _.clone(@models)
		@getLDByActionID(actionID).finish()
		# could do better here using getByActionID
		@eraseLog l for l in m when l.get('actionID') is "#{actionID}"

	getByActionID: (actionID) ->
		m = _.clone(@models)
		# do i have to do that for all the list ? why only 0 ?
		(l for l in m when l.get('actionID') is "#{actionID}")[0]

	eraseLog: (action) ->
		console.log 'destroy' , action
		action.destroy()

	reloadActions: () ->
		for actionID in @running()
			console.log "reloadActions :) #{actionID}"
			t = @getByActionID(actionID)
			timeleft =  t.get('time') + @getLDByActionID(actionID).duration() * 1000 - new Date().getTime()
			@stepAction(timeleft, actionID)


	running: () ->
		(m.get('actionID') for m in @models)

	stepAction: (timeleft, actionID) ->
		@trigger 'tick', actionID, timeleft
		if timeleft < 1000
			@timeleft = 1
			setTimeout((=> @setFinish(actionID)), 500)
		else
			@timeleft = timeleft - 1000
			setTimeout((=> @stepAction @timeleft, actionID), 1000)

@app.Action = Action
@app.Inventory = new Inventory()
@app.Log = Log