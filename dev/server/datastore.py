import datetime
import json
from google.appengine.ext import db



class Games(db.Model):
  name = db.StringProperty()
  minUsers = db.IntegerProperty()
  maxUsers = db.IntegerProperty()


class Users(db.Model):
  alias = db.StringProperty()
  loginDate = db.DateProperty(auto_now=True)


class Matches(db.Model):
  state = db.IntegerProperty()
  nbUsers = db.IntegerProperty()
  users = db.ListProperty(db.Key, default=None)


class Plays(db.Model):
  user = db.ReferenceProperty(Users)
  data = db.ListProperty(int)


def to_dict(model):
  SIMPLE_TYPES = (int, long, float, bool, dict, basestring)
  output = {'key': str(model.key())}

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
