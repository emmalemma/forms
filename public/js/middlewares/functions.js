(function () {
    var $_call, _i, _len, _ref, _result, routed_functions;
    var __slice = Array.prototype.slice;
    var __hasProp = Object.prototype.hasOwnProperty;
    $_call = function(function_name) {
      var args, kwargs, request;
      args = __slice.call(arguments, 1);
      switch (typeof args[args.length - 1]) {
        case 'object':
          kwargs = args.pop();
          break;
        case 'function':
          kwargs = {
            callback: args.pop()
          };
          break;
      }
      request = new Request.JSON({
        url: '/$/' + function_name,
        onSuccess: (function() {
          if (kwargs) {
            return kwargs.callback;
          }
        })()
      });
      if (kwargs) {
        delete kwargs.callback;
      }
      if (args.length) {
        kwargs = (typeof kwargs !== "undefined" && kwargs !== null) ? kwargs : {};
        kwargs._fargs = args;
      }
      if (kwargs) {
        return request.send(JSON.stringify(kwargs));
      } else {
        return request.get();
      }
    };
    routed_functions = [];
    _result = []; _ref = routed_functions;
    for (_i = 0, _len = _ref.length; _i < _len; _i++) {
      (function() {
        var f = _ref[_i];
        return _result.push(window[f] = function() {
          var args;
          args = __slice.call(arguments, 0);
          return $_call.apply(this, [("" + (f))].concat(args));
        });
      })();
    }
    return _result;
  }).call(this);