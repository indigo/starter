class LD
	constructor: ->
		@allBar = {}
	addBar: (metadata) ->
		@allBar[metadata.id] = metadata
	getAllBars: ->
		@allBar
	getBar: (id) ->
		@allBar[id]

	checkInventory: (title, qty) ->
		if not inventory.atLeast('Root',1)
			'Possible'
		else
			'Impossible'

	loadLD: (log)->
		@addBar
			id:0
			title: 'Start here and be faster than me'
			check: =>
				@checkInventory('Root',1)
			cost: ->
				inventory.updateValue('Root', 1)
				inventory.updateValue('Credits', 50)
				inventory.updateValue('Game Over', 0)
			duration: -> 1000
			finish: ->
				inventory.updateValue('Game Over', 1)

		@addBar
			id:2
			title: 'Collect'
			check: ->
				if inventory.atLeast('Credits',5) then 'Possible' else 'Impossible'
				#inventory.atLeast('Credits', 5)
			cost: ->
				inventory.updateValue('Credits', -5)
			duration: -> 2
			finish: ->
				inventory.updateValue('Credits', inventory.getValue('MCV') * 5)
				"Miam Miam"

		@addBar
			id:3
			title: 'Build a MCV'
			check: ->
				if inventory.atLeast('Credits',50) then 'Possible' else 'Impossible'
			cost: ->
				inventory.updateValue('Credits', -50)
			duration: -> 1
			finish: ->
				inventory.updateValue('MCV', 1)
				log.start '4'

		@addBar
			id:4
			title: 'Build a Barrack'
			check: ->
				if inventory.atLeast('Credits',100) then 'Possible' else 'Impossible'
			cost: ->
				inventory.updateValue('Credits', -100)
			duration: -> 5
			finish: ->
				inventory.updateValue('Barrack', 1)


		@addBar
			id:5
			title: 'Train a Marine'
			check: ->
				if inventory.atLeast('Credits',75) and inventory.has('Barrack')
					'Possible'
				else
					'Impossible'
			cost: ->
				inventory.updateValue('Credits', -75)
			duration: -> 5
			finish: ->
				inventory.updateValue('Marine', 1)


@app = window.app ? {}
@app.LD = LD
inventory = @app.Inventory

