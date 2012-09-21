import json
import webapp2

import datastore


class GamesHandler(webapp2.RequestHandler):

  # Return list of entities
  def get(self):
    entities = datastore.Game.all().run()
    output = {'entities': [datastore.to_dict(entity) for entity in entities]}

    self.response.out.write(output)

  # Create new entitiy
  def post(self):
    data = json.loads(self.request.body)

    entity = datastore.Game()
    for field in entity.fields():
      if field in data:
        datastore.Game.__setattr__(entity, field, data[field])
    entity.put()

    self.response.out.write(datastore.to_dict(entity))


class GameHandler(webapp2.RequestHandler):

  # Return entitiy
  def get(self, entity_key):
    entity = datastore.Game.get(entity_key)

    self.response.out.write(datastore.to_dict(entity))

  # Update entitiy
  def put(self, entity_key):
    data = json.loads(self.request.body)

    entity = datastore.Game.get(entity_key)
    for field in entity.fields():
      if field in data:
        datastore.Game.__setattr__(entity, field, data[field])
    entity.put()

    self.response.out.write(datastore.to_dict(entity))



app = webapp2.WSGIApplication([ (r'/games/(.*)', GameHandler),
                                (r'/games',      GamesHandler),
                              ],
                              debug=True)