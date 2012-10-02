import webapp2
from google.appengine.ext import db

import datastore
from rest import RestHandler



class UserMatchHandler(RestHandler):

  def get(self, user_key):
    RestHandler.get(self)

  # Join/Create new match
  def post(self, user_key):
    user = db.Key(user_key)

    # Get next active game
    match = datastore.Matches.gql("WHERE state = 1 AND users = :1", user).get()

    # Join open game
    if not match:
      for m in datastore.Matches.gql("WHERE state = 0"):
        if user not in m.users:
          match = m
          match.state = 1
          match.users.insert(0, user)
          match.put()
          break

    # Create new game
    if not match:
      match = datastore.Matches(state=0, users=[user])
      match.put()

    self.response.out.write(datastore.to_dict(match))



app = webapp2.WSGIApplication([ (r'/users/(.*)/matches', UserMatchHandler),
                                (r'/.*', RestHandler),
                              ], debug=True)
