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
    page = self.request.get('page', 0)
    pageSize = self.request.get('pageSize', 50)

    users = datastore.User.all().run(offset=page*pageSize, limit=pageSize)
    output = {'users': [datastore.to_dict(user) for user in users]}
    self.response.out.write(output)

  # Create new user
  def post(self):
    user = datastore.User()
    user.alias = self.request.get('alias')
    user.joinDate = datetime.date.today()
    user.loginDate = datetime.date.today()
    user.put()
    self.response.out.write(datastore.to_dict(user))


class UserHandler(webapp2.RequestHandler):

  # Return user
  def get(self, user_id):
    user = datastore.User.get_by_id(int(user_id)) #db.get(db.Key.from_path('User', int(user_id)))
    self.response.out.write(datastore.to_dict(user))

  # Update user
  def put(self, user_id):
    user = db.get(db.Key.from_path('User', int(user_id)))
    data = json.loads(self.request.body)

    for field in user.fields():
      if data[field]:
        datastore.User.__setattr__(user, field, data[field])

    user.put()
    self.response.out.write(datastore.to_dict(user))


class UserMatchesHandler(webapp2.RequestHandler):

  # Return list of user's matches
  def get(self, user_id):
    user = db.get(db.Key.from_path('User', int(user_id)))
    if self.request.get('only_keys'):
      output = {'matches': [key.id() for key in user.match_keys]}
    else:
      output = {'matches': [datastore.to_dict(match) for match in user.matches]}
    self.response.out.write(output)



app = webapp2.WSGIApplication([ (r'/users/(.*)/matches',  UserMatchesHandler),
                                (r'/users/(.*)',          UserHandler),
                                (r'/users',               UsersHandler),
                              ],
                              debug=True)