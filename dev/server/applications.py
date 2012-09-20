import cgi
import datetime
import json
import os
import urllib
import webapp2

from google.appengine.ext import db

import datastore


class ApplicationsHandler(webapp2.RequestHandler):

  # Return list of entities
  def get(self):
    entities = datastore.Application.all().run()
    output = {'entities': [datastore.to_dict(entity) for entity in entities]}

    self.response.out.write(output)

  # Create new entitiy
  def post(self):
    entity = datastore.Application()
    entity.name = self.request.get('name')
    entity.gamesCount = 0
    entity.usersCount = 0
    entity.put()

    self.response.out.write(datastore.to_dict(entity))


class ApplicationHandler(webapp2.RequestHandler):

  # Return entitiy
  def get(self, entity_id):
    entity = datastore.Application.get_by_id(int(entity_id))

    self.response.out.write(datastore.to_dict(entity))

  # Update entitiy
  def put(self, entity_id):
    entity = datastore.Application.get_by_id(int(entity_id))
    for entity in entity.fields():
      if self.request.get(field):
        datastore.Application.__setattr__(entity, field, self.request.get(field))
    entity.put()

    self.response.out.write(datastore.to_dict(entity))


class GamesHandler(webapp2.RequestHandler):

  # Return list of entities
  def get(self, ancestor_key):
    entities = datastore.Game.all().ancestor(ancestor_key)
    output = {'entities': [datastore.to_dict(entity) for entity in entities]}

    self.response.out.write(output)

  # Create new entitiy
  def post(self, ancestor_key):
    entity = datastore.Game(parent=ancestor_key)
    entity.name = self.request.get('name')
    entity.minMatchUsers = self.request.get('minMatchUsers')
    entity.maxMatchUsers = self.request.get('maxMatchUsers')
    entity.matchesCount = 0
    entity.put()

    self.response.out.write(datastore.to_dict(entity))


class GameHandler(webapp2.RequestHandler):

  # Return entitiy
  def get(self, ancestor_id, entity_id):
    entity = datastore.Game.get_by_id(int(entity_id))

    self.response.out.write(datastore.to_dict(entity))

  # Update entitiy
  def put(self, ancestor_id, entity_id):
    entity = datastore.Application.get_by_id(int(entity_id))
    for entity in entity.fields():
      if self.request.get(field):
        datastore.Application.__setattr__(entity, field, self.request.get(field))
    entity.put()

    self.response.out.write(datastore.to_dict(entity))


app = webapp2.WSGIApplication([ (r'/applications/(.*)/games/(.*)', GameHandler),
                                (r'/applications/(.*)/games',      GamesHandler),
                                (r'/applications/(.*)',            ApplicationHandler),
                                (r'/applications',                 ApplicationsHandler),
                              ],
                              debug=True)