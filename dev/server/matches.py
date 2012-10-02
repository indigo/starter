import json
import webapp2
from google.appengine.ext import db

import datastore
import rest


class MatchHandler(rest.RestHandler):

  def get(self):
    self.pre_process()

    # Return entitiy
    if self.entity:
      self.response.out.write(datastore.to_dict(self.entity))

    # Return list of entities
    else:
      if not self.ancestor:
        entities = self.Entity.all()
      else:
        entities = eval("self.ancestor.%s" % self.entity_type)

      output = {'entities': [datastore.to_dict(entity) for entity in entities]}
      self.response.out.write(output)

  # Create new entitiy
  def post(self):
    self.pre_process()
    self.entity = self.Entity(parent=self.ancestor)
    self.update_entity()



app = webapp2.WSGIApplication([ (r'/matches/.*', MatchHandler),
                              ],
                              debug=True)