(function() {
  var __hasProp = Object.prototype.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor; child.__super__ = parent.prototype; return child; },
    __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
    __indexOf = Array.prototype.indexOf || function(item) { for (var i = 0, l = this.length; i < l; i++) { if (i in this && this[i] === item) return i; } return -1; };

  jQuery(function() {
    var ActionPanelView, ActionView, MainView, SimpleRessourceView, _ref;
    this.app = (_ref = window.app) != null ? _ref : {};
    MainView = (function(_super) {

      __extends(MainView, _super);

      function MainView() {
        MainView.__super__.constructor.apply(this, arguments);
      }

      MainView.prototype.el = '#content';

      MainView.prototype.initialize = function(options) {
        this.collection.bind('reset', this.render, this);
        this.collection.bind('add', this.render, this);
        return this.collection.bind('change', this.render, this);
      };

      MainView.prototype.render = function() {
        var rsc, simpleRessourceView, _i, _len, _ref2;
        $(this.el).empty();
        _ref2 = this.collection.models;
        for (_i = 0, _len = _ref2.length; _i < _len; _i++) {
          rsc = _ref2[_i];
          simpleRessourceView = new SimpleRessourceView({
            model: rsc
          });
          $(this.el).append(simpleRessourceView.render().el);
        }
        return this;
      };

      MainView.prototype.createNew = function(attributes) {
        return this.collection.create(attributes);
      };

      MainView.prototype.addValue = function(name, value) {
        var rsc, updatedrsc, _i, _len, _ref2;
        _ref2 = this.collection.models;
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

      return MainView;

    })(Backbone.View);
    SimpleRessourceView = (function(_super) {

      __extends(SimpleRessourceView, _super);

      function SimpleRessourceView() {
        SimpleRessourceView.__super__.constructor.apply(this, arguments);
      }

      SimpleRessourceView.prototype.className = 'SimpleRessourceView';

      SimpleRessourceView.prototype.tagName = 'li';

      SimpleRessourceView.prototype.template = _.template($('#simple-ressource-template').html());

      SimpleRessourceView.prototype.render = function() {
        $(this.el).html(this.template(this.model.toJSON()));
        return this;
      };

      return SimpleRessourceView;

    })(Backbone.View);
    ActionPanelView = (function(_super) {

      __extends(ActionPanelView, _super);

      function ActionPanelView() {
        this.render = __bind(this.render, this);
        ActionPanelView.__super__.constructor.apply(this, arguments);
      }

      ActionPanelView.prototype.el = '#panel';

      ActionPanelView.prototype.tagName = 'li';

      ActionPanelView.prototype.initialize = function(options) {
        var a, k;
        this.inventory = options.inventory;
        this.level = options.bars;
        this.inventory.bind('change', this.render, this);
        this.inventory.bind('add', this.render, this);
        this.inventory.bind('reset', this.render, this);
        this.collection.bind('change', this.onAdd, this);
        this.collection.bind('add', this.onAdd, this);
        this.collection.bind('destroy', this.render, this);
        this.collection.bind('tick', this.render, this);
        this.collection.bind('reset', this.reloadActions, this);
        return this.actionViews = (function() {
          var _ref2, _results;
          _ref2 = this.level.getAllBars();
          _results = [];
          for (k in _ref2) {
            a = _ref2[k];
            _results.push(new ActionView({
              collection: this.collection,
              level: this.level,
              actionID: k
            }));
          }
          return _results;
        }).call(this);
      };

      ActionPanelView.prototype.render = function(options) {
        var actionView, _i, _len, _ref2;
        $(this.el).empty();
        _ref2 = this.actionViews;
        for (_i = 0, _len = _ref2.length; _i < _len; _i++) {
          actionView = _ref2[_i];
          $(this.el).append(actionView.render().el);
        }
        return this;
      };

      ActionPanelView.prototype.onAdd = function(e) {
        console.log("onAdd", e);
        return this.render();
      };

      ActionPanelView.prototype.renderAction = function(a, k) {
        var actionView;
        actionView = new ActionView({
          collection: this.collection,
          level: this.level,
          actionID: k
        });
        return $(this.el).append(actionView.render().el);
      };

      ActionPanelView.prototype.reloadActions = function() {
        return this.collection.reloadActions();
      };

      return ActionPanelView;

    })(Backbone.View);
    ActionView = (function(_super) {

      __extends(ActionView, _super);

      function ActionView() {
        this.render = __bind(this.render, this);
        ActionView.__super__.constructor.apply(this, arguments);
      }

      ActionView.prototype.className = 'ActionView';

      ActionView.prototype.tagName = 'li';

      ActionView.prototype.template = {
        template_Possible: _.template($('#ActionView-template').html()),
        template_Impossible: _.template($('#ActionView-template-impossible').html())
      };

      ActionView.prototype.template_running = _.template($('#ActionView-template-running').html());

      ActionView.prototype.events = {
        'click .clickable': 'startAction'
      };

      ActionView.prototype.initialize = function(options) {
        this.collection.bind('tick', this.timeleftUpdate, this);
        this.level = options.level;
        this.actionID = options.actionID;
        return this.action = this.level.getBar(this.actionID);
      };

      ActionView.prototype.timeleftUpdate = function(actionID, timeleft) {
        if (this.actionID === actionID) {
          this.timeleft = timeleft;
          console.log("" + actionID + " " + timeleft + " ");
        }
        return this.render();
      };

      ActionView.prototype.render = function() {
        var _ref2;
        if (this.timeleft != null) {
          this.mergedAttributes = _.extend(_.clone(this.action), {
            timeleft: Math.round(this.timeleft / 1000)
          });
        } else {
          this.mergedAttributes = _.extend(_.clone(this.action), {
            timeleft: 1
          });
        }
        if (_ref2 = this.actionID, __indexOf.call(this.collection.running(), _ref2) >= 0) {
          $(this.el).html(this.template_running(this.mergedAttributes));
        } else {
          this.mergedAttributes.duration = Math.round(this.mergedAttributes.duration());
          $(this.el).html(this.template["template_" + (this.action.check())](this.mergedAttributes));
          $(this.el).attr('action-id', this.action.id);
        }
        this.delegateEvents();
        return this;
      };

      ActionView.prototype.startAction = function(e) {
        this.timeleft = this.action.duration() * 1000;
        this.collection.start(this.actionID);
        return this.render();
      };

      return ActionView;

    })(Backbone.View);
    this.app.MainView = MainView;
    return this.app.ActionPanelView = ActionPanelView;
  });

}).call(this);
