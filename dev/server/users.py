import cgi
import datetime
import json
import os
import urllib
import webapp2

from google.appengine.ext import db

import datastore


class UsersHandler(webapp2.RequestHandler):

  # Return list of entities
  def get(self):
    page = self.request.get('page', 0)
    pageSize = self.request.get('pageSize', 50)
    entities = datastore.User.all().run(offset=page*pageSize, limit=pageSize)
    output = {'entities': [datastore.to_dict(entity) for entity in entities]}

    self.response.out.write(output)

  # Create new user
  def post(self):
    entity = datastore.User()
    entity.alias = self.request.get('alias')
    entity.loginDate = datetime.date.today()
    entity.put()

    self.response.out.write(datastore.to_dict(entity))


class UserHandler(webapp2.RequestHandler):

  # Return entitiy
  def get(self, entity_id):
    entity = datastore.User.get_by_id(int(entity_id))

    self.response.out.write(datastore.to_dict(entity))

  # Update entitiy
  def put(self, entity_id):
    entity = datastore.User.get_by_id(int(entity_id))
    for entity in entity.fields():
      if self.request.get(field):
        datastore.User.__setattr__(entity, field, self.request.get(field))
    entity.put()

    self.response.out.write(datastore.to_dict(entity))


class UserMatchesHandler(webapp2.RequestHandler):

  # Return list of user's matches
  def get(self, entity_id):
    entity = datastore.User.get_by_id(int(entity_id))
    if self.request.get('only_keys'):
      output = {'entities': [key.id() for key in entity.match_keys]}
    else:
      output = {'entities': [datastore.to_dict(match) for match in entity.matches]}

    self.response.out.write(output)



app = webapp2.WSGIApplication([ (r'/users/(.*)/matches',  UserMatchesHandler),
                                (r'/users/(.*)',          UserHandler),
                                (r'/users',               UsersHandler),
                              ],
                              debug=True)