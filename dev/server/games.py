import cgi
import datetime
import jinja2
import json
import os
import urllib
import webapp2

from google.appengine.ext import db

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__ )))


class User(db.Model):
  #games = db.ListProperty(db.Key, default=None)

  @property
  def games(self):
      return Game.gql("WHERE users = :1", self.key())

class Game(db.Model):
  type = db.IntegerProperty()
  open = db.BooleanProperty()
  users = db.ListProperty(db.Key, default=None)

class Move(db.Model):
  user = db.ReferenceProperty(User)
  data = db.ListProperty(int)


class AdminPage(webapp2.RequestHandler):

  def get(self):
    user = user_games = game = game_moves = None

    # Create new user
    if self.request.get('new_user'):
      User().put()

    # Fetch user's games
    if self.request.get('user_key'):
      try:
        user = db.get(self.request.get('user_key'))
        user_games = user.games #db.get(user.games)
      except:
        self.response.out.write("Invalid user_key")
        return

    # Fetch game's moves
    if self.request.get('game_key'):
      try:
        game = db.get(self.request.get('game_key'))
        game_moves = db.Query(Move).ancestor(game.key())
      except:
        self.response.out.write("Invalid game_key")
        return

    # Load page
    template_values = { 'all_users': User.all(), 'user': user, 'user_games': user_games, 'game': game, 'game_moves': game_moves }
    template = jinja_environment.get_template('admin.html')
    self.response.out.write(template.render(template_values))


class UserPage(webapp2.RequestHandler):

  def get(self):

    # Get user from key
    try:
      user = db.get(self.request.get('user_key'))

    # Create new user
    except:
      user = User()
      user.put()

    # Sort games based on turn
    all_games = user.games #db.get(user.games)
    waiting_games = []
    myturn_games = []

    for game in all_games:
      if not game.open and game.users[0] == user.key():
        myturn_games.append(game)
      else:
        waiting_games.append(game)

    # Load page
    template_values = { 'user': user, 'myturn_games': myturn_games, 'waiting_games': waiting_games }
    template = jinja_environment.get_template('user.html')
    self.response.out.write(template.render(template_values))


class GamePage(webapp2.RequestHandler):

  def get(self):

    user = db.get(self.request.get('user_key'))
    game = None

    # Load Game
    if self.request.get('game_key'):
      game = db.get(self.request.get('game_key'))

    else:
      new_game = True

      # Find next active game
      for user_game in user.games:
      #  user_game = db.get(game_key)

        if not user_game.open and user_game.users[0] == user.key():
          game = user_game
          new_game = False
          break

      # Find joinable game
      if not game:
        open_games = Game.gql("WHERE open=True")
        for open_game in open_games:
          if open_game.users[0] != user.key():
            game = open_game
            break

      # Create new game
      if not game:
        game = Game(type = 1)

      # Add game to user
      if new_game:
        game.open = False
        game.users.insert(0, user.key())
        game.put()

    game_moves = db.Query(Move).ancestor(game.key())

    # Load page
    template_values = { 'user': user, 'game': game, 'game_moves': game_moves }
    template = jinja_environment.get_template('game.html')
    self.response.out.write(template.render(template_values))


class PlayPage(webapp2.RequestHandler):

  def get(self):

    user = db.get(self.request.get('user_key'))
    game = db.get(self.request.get('game_key'))
    data = eval(self.request.get('game_data'))

    # Create move
    move = Move(parent=game.key(), user=user.key(), data=data)
    move.put()

    # Set game as open
    if len(game.users) == 1:  # TODO: replace 1 with dynamic value based on game type
      game.open = True

    # Move current user to end of list
    else:
      game.users.append(game.users.pop(0))

    game.put()

    game_moves = db.Query(Move).ancestor(game.key())

    # Load page
    template_values = { 'user': user, 'game': game, 'game_moves': game_moves }
    template = jinja_environment.get_template('game.html')
    self.response.out.write(template.render(template_values))



pages = [
          ('/admin', AdminPage),
          ('/user', UserPage),
          ('/game', GamePage),
          ('/play', PlayPage)
        ]
app = webapp2.WSGIApplication(pages, debug=True)