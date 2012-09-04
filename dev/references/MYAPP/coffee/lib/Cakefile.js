(function() {
  var build, fs, print, spawn;

  fs = require('fs');

  print = require('util').print;

  spawn = require('child_process').spawn;

  build = function(callback) {
    var coffee;
    coffee = spawn('coffee', ['-c', '-o', 'lib', 'src']);
    coffee.stderr.on('data', function(data) {
      return process.stderr.write(data.toString());
    });
    coffee.stdout.on('data', function(data) {
      return print(data.toString());
    });
    return coffee.on('exit', function(code) {
      if (code === 0) return typeof callback === "function" ? callback() : void 0;
    });
  };

  task('build', 'Build lib/ from src/', function() {
    return build();
  });

}).call(this);
