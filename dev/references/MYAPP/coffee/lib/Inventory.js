(function() {
  var Action, Inventory, Log, Ressource, _ref,
    __hasProp = Object.prototype.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor; child.__super__ = parent.prototype; return child; };

  this.app = (_ref = window.app) != null ? _ref : {};

  Ressource = (function(_super) {

    __extends(Ressource, _super);

    function Ressource() {
      Ressource.__super__.constructor.apply(this, arguments);
    }

    return Ressource;

  })(Backbone.Model);

  Inventory = (function(_super) {

    __extends(Inventory, _super);

    function Inventory() {
      Inventory.__super__.constructor.apply(this, arguments);
    }

    Inventory.prototype.model = Ressource;

    Inventory.prototype.localStorage = new Store("Inventory");

    Inventory.prototype.getRessource = function(name) {
      var i, _i, _len, _ref2;
      _ref2 = this.models;
      for (_i = 0, _len = _ref2.length; _i < _len; _i++) {
        i = _ref2[_i];
        if (name === i.get('title')) return i;
      }
    };

    Inventory.prototype.getValue = function(name) {
      var _ref2;
      return (_ref2 = this.getRessource(name)) != null ? _ref2.get('value') : void 0;
    };

    Inventory.prototype.atLeast = function(name, value) {
      return this.getValue(name) >= value;
    };

    Inventory.prototype.has = function(name) {
      var i, _i, _len, _ref2;
      _ref2 = this.models;
      for (_i = 0, _len = _ref2.length; _i < _len; _i++) {
        i = _ref2[_i];
        if (name === i.get('title')) return true;
      }
      return false;
    };

    Inventory.prototype.updateValue = function(name, value) {
      if (!this.has(name)) {
        return this.create({
          title: name,
          value: value
        });
      } else {
        return this.updateExistingValue(name, value);
      }
    };

    Inventory.prototype.updateExistingValue = function(name, value) {
      var rsc, updatedrsc, _i, _len, _ref2;
      _ref2 = this.models;
      for (_i = 0, _len = _ref2.length; _i < _len; _i++) {
        rsc = _ref2[_i];
        if (rsc.get('title') === name) {
          updatedrsc = rsc.set({
            value: rsc.get('value') + value
          });
        }
      }
      if (updatedrsc) updatedrsc.save();
      return updatedrsc;
    };

    return Inventory;

  })(Backbone.Collection);

  Action = (function(_super) {

    __extends(Action, _super);

    function Action() {
      Action.__super__.constructor.apply(this, arguments);
    }

    return Action;

  })(Backbone.Model);

  Log = (function(_super) {

    __extends(Log, _super);

    function Log() {
      Log.__super__.constructor.apply(this, arguments);
    }

    Log.prototype.model = Action;

    Log.prototype.localStorage = new Store("Log");

    Log.prototype.initialize = function(options) {
      this.level = options.ld;
      return this.level.loadLD(this);
    };

    Log.prototype.getLDByActionID = function(actionID) {
      return this.level.getBar(actionID);
    };

    Log.prototype.start = function(actionID) {
      var timeleft;
      console.log("Start action " + actionID + ", saved to the localstore");
      this.getLDByActionID(actionID).cost();
      this.create({
        time: new Date().getTime(),
        actionID: actionID
      });
      timeleft = this.getLDByActionID(actionID).duration() * 1000;
      return this.stepAction(timeleft, actionID);
    };

    Log.prototype.setFinish = function(actionID) {
      var l, m, _i, _len, _results;
      m = _.clone(this.models);
      this.getLDByActionID(actionID).finish();
      _results = [];
      for (_i = 0, _len = m.length; _i < _len; _i++) {
        l = m[_i];
        if (l.get('actionID') === ("" + actionID)) _results.push(this.eraseLog(l));
      }
      return _results;
    };

    Log.prototype.getByActionID = function(actionID) {
      var l, m;
      m = _.clone(this.models);
      return ((function() {
        var _i, _len, _results;
        _results = [];
        for (_i = 0, _len = m.length; _i < _len; _i++) {
          l = m[_i];
          if (l.get('actionID') === ("" + actionID)) _results.push(l);
        }
        return _results;
      })())[0];
    };

    Log.prototype.eraseLog = function(action) {
      console.log('destroy', action);
      return action.destroy();
    };

    Log.prototype.reloadActions = function() {
      var actionID, t, timeleft, _i, _len, _ref2, _results;
      _ref2 = this.running();
      _results = [];
      for (_i = 0, _len = _ref2.length; _i < _len; _i++) {
        actionID = _ref2[_i];
        console.log("reloadActions :) " + actionID);
        t = this.getByActionID(actionID);
        timeleft = t.get('time') + this.getLDByActionID(actionID).duration() * 1000 - new Date().getTime();
        _results.push(this.stepAction(timeleft, actionID));
      }
      return _results;
    };

    Log.prototype.running = function() {
      var m, _i, _len, _ref2, _results;
      _ref2 = this.models;
      _results = [];
      for (_i = 0, _len = _ref2.length; _i < _len; _i++) {
        m = _ref2[_i];
        _results.push(m.get('actionID'));
      }
      return _results;
    };

    Log.prototype.stepAction = function(timeleft, actionID) {
      var _this = this;
      this.trigger('tick', actionID, timeleft);
      if (timeleft < 1000) {
        this.timeleft = 1;
        return setTimeout((function() {
          return _this.setFinish(actionID);
        }), 500);
      } else {
        this.timeleft = timeleft - 1000;
        return setTimeout((function() {
          return _this.stepAction(_this.timeleft, actionID);
        }), 1000);
      }
    };

    return Log;

  })(Backbone.Collection);

  this.app.Action = Action;

  this.app.Inventory = new Inventory();

  this.app.Log = Log;

}).call(this);
