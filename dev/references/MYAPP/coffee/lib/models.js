(function() {
  var Ressource, _ref,
    __hasProp = Object.prototype.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor; child.__super__ = parent.prototype; return child; };

  Ressource = (function(_super) {

    __extends(Ressource, _super);

    function Ressource() {
      Ressource.__super__.constructor.apply(this, arguments);
    }

    return Ressource;

  })(Backbone.Model);

  this.app = (_ref = window.app) != null ? _ref : {};

  this.app.Ressource = Ressource;

}).call(this);
