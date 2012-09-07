import cgi
import datetime
import json
import os
import urllib
import webapp2

from google.appengine.ext import db

import datastore


class UsersHandler(webapp2.RequestHandler):

  # Return list of users
  def get(self):
    users = datastore.User.all()
    output = {'users': [datastore.to_dict(user) for user in users]}
    self.response.out.write(output)

  # Create new user
  def post(self):
    user = datastore.User()
    user.put()
    self.response.out.write(datastore.to_dict(user))


class UserHandler(webapp2.RequestHandler):

  # Return user
  def get(self, user_id):
    user = db.get(db.Key.from_path('User', int(user_id)))
    self.response.out.write(datastore.to_dict(user))


class UserGamesHandler(webapp2.RequestHandler):

  # Return list of user's games
  def get(self, user_id):
    user = db.get(db.Key.from_path('User', int(user_id)))
    if self.request.get('only_keys'):
      output = {'games': [datastore.to_dict(game) for game in user.game_keys]}
    else:
      output = {'games': [datastore.to_dict(game) for game in user.games]}
    self.response.out.write(output)



app = webapp2.WSGIApplication([ (r'/users/(.*)/games', UserGamesHandler),
                                (r'/users/(.*)', UserHandler),
                                (r'/users', UsersHandler),
                              ],
                              debug=True)