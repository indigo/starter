import json
import webapp2

import datastore


class RestHandler(webapp2.RequestHandler):

  def get(self):
    self.pre_process()

    # Return list of entities
    if not self.entity:

      if not self.ancestor:
        entities = self.Entity.all()
      else:
        entities = self.Entity.gql("WHERE %s = :1" % self.ancestor_type, self.ancestor)

      output = {'entities': [datastore.to_dict(entity) for entity in entities]}
      self.response.out.write(output)

    # Return entitiy
    else:
      self.response.out.write(datastore.to_dict(self.entity))

  # Create new entitiy
  def post(self):
    self.pre_process()
    self.entity = self.Entity()
    self.update_entity()

  # Update entitiy
  def put(self):
    self.pre_process()
    self.update_entity()


  # Pre-process request
  def pre_process(self):
    self.ancestor_type = None
    self.Ancestor = None
    self.ancestor = None
    path_list = self.request.path[1:].split('/')

    # Global function
    if len(path_list) & 1:
      self.Entity = eval("datastore.%s" % path_list[-1].capitalize())
      self.entity = None

      if len(path_list) > 1:
        self.ancestor_type = "datastore.%s" % path_list[-3]
        self.Ancestor = eval("datastore.%s" % path_list[-3].capitalize())
        self.ancestor = self.Ancestor.get(path_list[-2])

    # Entity specific function
    elif len(path_list) > 0:
      self.Entity = eval("datastore.%s" % path_list[-2].capitalize())
      self.entity = self.Entity.get(path_list[-1])
    else:
      raise Exception

  # Update entity
  def update_entity(self):
    data = json.loads(self.request.body)

    for field in self.entity.fields():
      if field in data:
        self.Entity.__setattr__(self.entity, field, data[field])
    self.entity.put()

    self.response.out.write(datastore.to_dict(self.entity))



app = webapp2.WSGIApplication([ (r'/.*', RestHandler),
                              ],
                              debug=True)