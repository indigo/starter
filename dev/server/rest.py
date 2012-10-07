import json
import webapp2
from google.appengine.ext import db

import datastore



class RestHandler(webapp2.RequestHandler):

  def get(self):
    self.pre_process()

    # Return entitiy
    if self.entity:
      attr = self.request.get('property')
      if attr:
        self.response.out.write(eval("self.entity.%s" % attr))
      else:
        self.response.out.write(datastore.to_dict(self.entity))

    # Return list of entities
    else:
      page = int(self.request.get('page', 0))
      pageSize = int(self.request.get('pageSize', 50))

      if not self.ancestor:
        entities = self.Entity.all()
      else:
        entities = eval("self.ancestor.%s" % self.entity_type)

      output = [datastore.to_dict(entity) for entity in entities.run(offset=page*pageSize, limit=pageSize)]
      self.response.out.write(json.dumps(output))


  # Create new entitiy
  def post(self):
    self.pre_process()
    self.entity = self.Entity(parent=self.ancestor)
    self.update_entity()


  # Update entitiy
  def put(self):
    self.pre_process()
    self.update_entity()


  # Pre-process request
  def pre_process(self):
    self.Ancestor = None
    self.ancestor = None
    path_list = self.request.path[1:].split('/')

    # Global function
    if len(path_list) & 1:
      self.Entity = eval("datastore.%s" % path_list[-1].capitalize())
      self.entity = None
      self.entity_type = path_list[-1]

      if len(path_list) > 1:
        self.Ancestor = eval("datastore.%s" % path_list[-3].capitalize())
        self.ancestor = self.Ancestor.get(path_list[-2])

    # Entity specific function
    elif len(path_list) > 0:
      self.Entity = eval("datastore.%s" % path_list[-2].capitalize())
      self.entity = self.Entity.get(path_list[-1])
      self.entity_type = path_list[-2]

    else:
      raise Exception


  # Update entity
  def update_entity(self):
    data = json.loads(self.request.body)

    for key, value in data.items():
      if isinstance(value, list) and len(value) > 0 and isinstance(value[0], basestring) and value[0][:4] == "key=":
        self.Entity.__setattr__(self.entity, key, [db.Key(k[4:]) for k in value])
      elif isinstance(value, basestring) and value[:4] == "key=":
        self.Entity.__setattr__(self.entity, key, db.Key(value[4:]))
      else:
        self.Entity.__setattr__(self.entity, key, value)
    self.entity.put()

    self.response.out.write(datastore.to_dict(self.entity))



app = webapp2.WSGIApplication([ (r'/.*', RestHandler),
                              ], debug=True)
