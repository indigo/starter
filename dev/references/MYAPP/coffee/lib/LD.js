(function() {
  var LD, inventory, _ref;

  LD = (function() {

    function LD() {
      this.allBar = {};
    }

    LD.prototype.addBar = function(metadata) {
      return this.allBar[metadata.id] = metadata;
    };

    LD.prototype.getAllBars = function() {
      return this.allBar;
    };

    LD.prototype.getBar = function(id) {
      return this.allBar[id];
    };

    LD.prototype.checkInventory = function(title, qty) {
      if (!inventory.atLeast('Root', 1)) {
        return 'Possible';
      } else {
        return 'Impossible';
      }
    };

    LD.prototype.loadLD = function(log) {
      var _this = this;
      this.addBar({
        id: 0,
        title: 'Start here and be faster than me',
        check: function() {
          return _this.checkInventory('Root', 1);
        },
        cost: function() {
          inventory.updateValue('Root', 1);
          inventory.updateValue('Credits', 50);
          return inventory.updateValue('Game Over', 0);
        },
        duration: function() {
          return 1000;
        },
        finish: function() {
          return inventory.updateValue('Game Over', 1);
        }
      });
      this.addBar({
        id: 2,
        title: 'Collect',
        check: function() {
          if (inventory.atLeast('Credits', 5)) {
            return 'Possible';
          } else {
            return 'Impossible';
          }
        },
        cost: function() {
          return inventory.updateValue('Credits', -5);
        },
        duration: function() {
          return 2;
        },
        finish: function() {
          inventory.updateValue('Credits', inventory.getValue('MCV') * 5);
          return "Miam Miam";
        }
      });
      this.addBar({
        id: 3,
        title: 'Build a MCV',
        check: function() {
          if (inventory.atLeast('Credits', 50)) {
            return 'Possible';
          } else {
            return 'Impossible';
          }
        },
        cost: function() {
          return inventory.updateValue('Credits', -50);
        },
        duration: function() {
          return 1;
        },
        finish: function() {
          inventory.updateValue('MCV', 1);
          return log.start('4');
        }
      });
      this.addBar({
        id: 4,
        title: 'Build a Barrack',
        check: function() {
          if (inventory.atLeast('Credits', 100)) {
            return 'Possible';
          } else {
            return 'Impossible';
          }
        },
        cost: function() {
          return inventory.updateValue('Credits', -100);
        },
        duration: function() {
          return 5;
        },
        finish: function() {
          return inventory.updateValue('Barrack', 1);
        }
      });
      return this.addBar({
        id: 5,
        title: 'Train a Marine',
        check: function() {
          if (inventory.atLeast('Credits', 75) && inventory.has('Barrack')) {
            return 'Possible';
          } else {
            return 'Impossible';
          }
        },
        cost: function() {
          return inventory.updateValue('Credits', -75);
        },
        duration: function() {
          return 5;
        },
        finish: function() {
          return inventory.updateValue('Marine', 1);
        }
      });
    };

    return LD;

  })();

  this.app = (_ref = window.app) != null ? _ref : {};

  this.app.LD = LD;

  inventory = this.app.Inventory;

}).call(this);
