# ModelsAndCollections
@app = window.app ? {}

class Game extends Backbone.Model

class Games extends Backbone.Collection
	model: Game

# "alias": "Indigo", "loginDate": "2012-10-07", "parent": "None", "key": "ahNkZXZ..."
class User extends Backbone.Model

class Users extends Backbone.Collection
	model: User
	url: "/users"

class Match extends Backbone.Model

class Matches extends Backbone.Collection
	model: Match

@app.Game = Game
@app.Games = Games
@app.User = User
@app.Users = Users
@app.Match = Match
@app.Matches = Matches