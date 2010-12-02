(function () {
        var Middlewares, _k, _len, _ref2, _result, ware;
        Middlewares = ["functions",null,null];
        _result = []; _ref2 = Middlewares;
        for (_k = 0, _len = _ref2.length; _k < _len; _k++) {
          ware = _ref2[_k];
          _result.push((function() {
            if (ware) {
              return $.getScript("/js/middlewares/" + (ware) + ".js");
            }
          })());
        }
        return _result;
      }).call(this);