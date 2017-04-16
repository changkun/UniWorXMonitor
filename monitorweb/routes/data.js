var express = require('express');
var fs = require('fs')
var path = require('path')
var router = express.Router();

router.get('/', function(req, res, next) {
  res.send('Hello world! Are you looking for <a href="/uniworx">UniworX Monitor</a>?');
});

router.get('/courses', function(req, res, next) {
	fs.readFile(path.join(__dirname, '../data/courses.json'), function(err, data) {
    if (err) {
			throw err;
			res.send('server side error');
			return;
		}
    var data = JSON.parse(data)
    res.send(data)
  });
});

router.get('/log', function(req, res, next) {
	fs.readFile(path.join(__dirname, '../data/log.json'), function(err, data) {
    if (err) {
			throw err;
			res.send('server side error');
			return;
		}
    var data = JSON.parse(data)
    res.send(data)
  });
});

module.exports = router;