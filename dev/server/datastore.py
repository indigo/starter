import datetime
import json
from google.appengine.ext import db



class Games(db.Model):
  name = db.StringProperty()


class Users(db.Model):
  alias = db.StringProperty()
  loginDate = db.DateProperty(auto_now=True)

  @property
  def matches(self):
    return Matches.gql("WHERE users = :1", self.key())

  @property
  def nextMatch(self):
    match = None

    # Get next active game
    matches = Matches.gql("WHERE state = 1 AND users = :1", self.key())
    for m in matches:
      if m.users[0] == self:
        match = m
        break

    # Join open game
    if not match:
      matches = Matches.gql("WHERE state = 0")
      for m in matches:
        if self.key() not in m.users:
          match = m
          match.state = 1
          match.users.insert(0, self.key())
          match.put()
          break

    # Create new game
    if not match:
      match = Matches(state=0, users=[self.key()])
      match.put()

    return to_dict(match)


class Matches(db.Model):
  users = db.ListProperty(db.Key, default=None)
  state = db.IntegerProperty()
  data = db.ListProperty(int)

  @property
  def plays(self):
    return Plays.gql("WHERE ANCESTOR IS :1", self.key())


class Plays(db.Model):
  user = db.ReferenceProperty(Users)
  data = db.ListProperty(int)


def to_dict(model):
  if not isinstance(model, db.Model):
    return str(model)

  SIMPLE_TYPES = (int, long, float, bool, dict, basestring)
  output = {'key': str(model.key()), 'parent':str(model.parent_key())}

  for key, prop in model.properties().iteritems():
    value = getattr(model, key)

    if value is None or isinstance(value, SIMPLE_TYPES):
      output[key] = value
    elif isinstance(value, list):
      if len(value) > 0 and isinstance(value[0], db.Key):
        output[key] = [int(item.id()) for item in value]
      else:
        output[key] = value
    elif isinstance(value, datetime.date):
      output[key] = str(value)
    elif isinstance(value, db.GeoPt):
      output[key] = {'lat': value.lat, 'lon': value.lon}
    elif isinstance(value, db.Model):
      output[key] = to_dict(value)
    else:
      raise ValueError('cannot encode ' + repr(prop))

  return output
