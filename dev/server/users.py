import json
import webapp2

import datastore


class UsersHandler(webapp2.RequestHandler):

  # Return list of entities
  def get(self):
    page = self.request.get('page', 0)
    pageSize = self.request.get('pageSize', 50)
    entities = datastore.User.all().run(offset=page*pageSize, limit=pageSize)
    output = {'entities': [datastore.to_dict(entity) for entity in entities]}

    self.response.out.write(output)

  # Create new entitiy
  def post(self):
    data = json.loads(self.request.body)

    entity = datastore.User()
    for field in entity.fields():
      if field in data:
        datastore.Game.__setattr__(entity, field, data[field])
    entity.put()

    self.response.out.write(datastore.to_dict(entity))


class UserHandler(webapp2.RequestHandler):

  # Return entitiy
  def get(self, entity_key):
    entity = datastore.User.get(entity_key)

    self.response.out.write(datastore.to_dict(entity))

  # Update entitiy
  def put(self, entity_key):
    data = json.loads(self.request.body)

    entity = datastore.User.get(entity_key)
    for field in entity.fields():
      if field in data:
        datastore.Game.__setattr__(entity, field, data[field])
    entity.put()

    self.response.out.write(datastore.to_dict(entity))


class UserMatchesHandler(webapp2.RequestHandler):

  # Return list of user's matches
  def get(self, entity_key):
    entity = datastore.User.get(entity_key)
    output = {'entities': [datastore.to_dict(match) for match in entity.matches]}

    self.response.out.write(output)



app = webapp2.WSGIApplication([ (r'/users/(.*)/matches',  UserMatchesHandler),
                                (r'/users/(.*)',          UserHandler),
                                (r'/users',               UsersHandler),
                              ],
                              debug=True)