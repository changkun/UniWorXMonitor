var express = require('express');
var fs = require('fs')
var path = require('path')
var router = express.Router();

router.get('/', function(req, res, next) {
  res.send('Hello world! Are you looking for <a href="/uniworx">UniworX Monitor</a>?');
});

module.exports = router;
