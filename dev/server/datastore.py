import datetime
import time
import json

from google.appengine.ext import db



def to_dict(model):
  SIMPLE_TYPES = (int, long, float, bool, dict, basestring)
  output = {}

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
      ms = time.mktime(value.utctimetuple())
      ms += getattr(value, 'microseconds', 0) / 1000
      output[key] = int(ms)
    elif isinstance(value, db.GeoPt):
      output[key] = {'lat': value.lat, 'lon': value.lon}
    elif isinstance(value, db.Model):
      output[key] = to_dict(value)
    else:
      raise ValueError('cannot encode ' + repr(prop))

  return json.dumps(output)


class User(db.Model):
  alias = db.StringProperty()
  joinDate = db.DateProperty()
  loginDate = db.DateProperty()

  @property
  def matches(self):
      return Game.gql("WHERE users = :1", self.key())

  @property
  def match_keys(self):
      return Game.gql("WHERE users = :1", self.key()).run(keys_only=True)


class Match(db.Model):
  typeId = db.IntegerProperty()
  isOpen = db.BooleanProperty()
  users = db.ListProperty(db.Key, default=None)


class Play(db.Model):
  user = db.ReferenceProperty(User)
  data = db.ListProperty(int)

