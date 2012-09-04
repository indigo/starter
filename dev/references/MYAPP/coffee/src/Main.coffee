# main, objectif ici, faire le moins possible
# c'est le lancement, donc principalement du loading, de la définition de start
# lancement de la mainView

jQuery ->
	@app = window.app ? {}
	levelDesign = new @app.LD()
	gameScene = new @app.Log ld: levelDesign

	@app.mainView = new @app.MainView collection: @app.Inventory
	@app.actionPanelView = new @app.ActionPanelView
		collection: gameScene
		inventory: @app.Inventory
		bars: levelDesign

	gameScene.fetch()
	@app.Inventory.fetch()
