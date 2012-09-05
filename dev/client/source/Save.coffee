jQuery ->

	class Save extends Backbone.Model
		localStorage: new Store("Save")

	save = new Save 
		id:777
		
	save.fetch()
	if save.has 'userid'
		console.log('Welcome!  Fetching your information.... ')
		console.log save.get userid
	else
		save.save({userid: '12'})
		console.log('saving somewhere')
