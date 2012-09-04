(function() {

  jQuery(function() {
    var gameScene, levelDesign, _ref;
    this.app = (_ref = window.app) != null ? _ref : {};
    levelDesign = new this.app.LD();
    gameScene = new this.app.Log({
      ld: levelDesign
    });
    this.app.mainView = new this.app.MainView({
      collection: this.app.Inventory
    });
    this.app.actionPanelView = new this.app.ActionPanelView({
      collection: gameScene,
      inventory: this.app.Inventory,
      bars: levelDesign
    });
    gameScene.fetch();
    return this.app.Inventory.fetch();
  });

}).call(this);
