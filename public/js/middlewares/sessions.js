(function () {
    return (this.Session = {
      "id": Cookie.read('_sessid')
    });
  }).call(this);