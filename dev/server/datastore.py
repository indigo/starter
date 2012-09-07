import datetime
import time
import json

from google.appengine.ext import db



def to_dict(model):
  SIMPLE_TYPES = (int, long, float, bool, dict, basestring, list)
  output = {}

  for key, prop in model.properties().iteritems():
    value = getattr(model, key)

    if value is None or isinstance(value, SIMPLE_TYPES):
      output[key] = value
    elif isinstance(value, datetime.date):
      # Convert date/datetime to ms-since-epoch ("new Date()").
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


def get_fields_by_id(entity_kind, entity_id, fields):

    result = {}

    # Get entity
    entity = db.get(db.Key.from_path(entity_kind, int(entity_id)))

    # Get all fields
    if fields == '*':
      fields = entity.fields()

    # Write fields in dict
    result = {'id': entity.key().id(), 'key': entity.key()}

    for field in fields:
      result[field] = eval('entity.%s' % field)

    return json.dumps(result)


def get_games_by_user_id(user_id):

    result = {}

    # Get user
    user = db.get(db.Key.from_path('User', int(user_id)))

    # Get games
    for game in user.game_keys:
      result[game.key().id()] = str(game.key())

    return json.dumps(result)


class User(db.Model):
  alias = db.StringProperty()

  @property
  def games(self):
      return Game.gql("WHERE users = :1", self.key())

  @property
  def game_keys(self):
      return Game.gql("WHERE users = :1", self.key(), keys_only=True)


class Game(db.Model):
  type = db.IntegerProperty()
  open = db.BooleanProperty()
  users = db.ListProperty(db.Key, default=None)


class Move(db.Model):
  user = db.ReferenceProperty(User)
  data = db.ListProperty(int)

