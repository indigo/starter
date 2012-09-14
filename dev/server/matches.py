import cgi
import datetime
import json
import os
import urllib
import webapp2

from google.appengine.ext import db

import datastore


class MatchHandler(webapp2.RequestHandler):

  # Return list of matches
  def get(self):
    page = self.request.get('page', 0)
    pageSize = self.request.get('pageSize', 50)

    matches = datastore.Match.all().run(offset=page*pageSize, limit=pageSize)
    output = {'matches': [datastore.to_dict(match) for match in matches]}
    self.response.out.write(output)

  # Create new match
  def post(self):
    typeId = 

    match = datastore.Match()
    match.typeId(self.request.get('typeId', 1))
    match.isOpen = False
    match.users.insert(0, user.key())



    user.alias = self.request.get('alias')
    user.put()
    self.response.out.write(datastore.to_dict(user))


class MatchHandler(webapp2.RequestHandler):

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


class MatchUsersHandler(webapp2.RequestHandler):

  # Return list of user's matches
  def get(self, user_id):
    user = db.get(db.Key.from_path('User', int(user_id)))
    if self.request.get('only_keys'):
      output = {'matches': [key.id() for key in user.match_keys]}
    else:
      output = {'matches': [datastore.to_dict(match) for match in user.matches]}
    self.response.out.write(output)



app = webapp2.WSGIApplication([ (r'/matches/(.*)/users',  MatchUsersHandler),
                                (r'/matches/(.*)/moves',  MatchMovesHandler),
                                (r'/matches/(.*)',        MatchHandler),
                                (r'/matches',             MatchHandler),
                              ],
                              debug=True)