var express = require('express');
var fs = require('fs')
var path = require('path')
var util = require('util');
var spawn = require('child_process').spawn
var router = express.Router();

function validate(email) {
  var tester = /^[-!#$%&'*+\/0-9=?A-Z^_a-z{|}~](\.?[-!#$%&'*+\/0-9=?A-Z^_a-z`{|}~])*@[a-zA-Z0-9](-?\.?[a-zA-Z0-9])*\.[a-zA-Z](-?[a-zA-Z0-9])+$/;
  if (!email) return false;

  if (email.length>254) return false;
  
  var valid = tester.test(email);
  if(!valid) return false;
  
  var parts = email.split('@');
  if(parts[0].length>64) return false;
  
  var domainParts = parts[1].split(".");
	if(domainParts.some(function(part) {return part.length>63; }))
		return false;

	return true;
}

router.get('/', function(req, res, next) {
  fs.readFile(path.join(__dirname, '../data/users.json'), function(err, data) {
    if (err) throw err;
    var data = JSON.parse(data)
    var secreat = {
      'users': []
    }
    data.users.forEach(function(user) {
      var secreatUser = '';
      for(index in user) {
        if (index > 2) {
          secreatUser += '*';
        } else {
          secreatUser += user[index];
        }
      }
      secreat.users.push(secreatUser)
    })
    res.send(secreat)
  });
});

router.post('/add', function(req, res, next) {
  fs.readFile(path.join(__dirname, '../data/users.json'), function(err, data) {
    if (err) throw err;
    var data = JSON.parse(data);
    var status = null;
    var info   = null;
    if(validate(req.body.email)) {
      if(data.users.indexOf(req.body.email) > -1) {
        status = 'Fail';
        info   = 'You already subscribed!';
      } else {
        data.users.push(req.body.email);
        fs.writeFileSync(path.join(__dirname, '../data/users.json'), JSON.stringify(data));
        status = 'Success';
        info   = 'You has become our user!';
        var process = spawn('python3', [path.join(__dirname, '../monitor/sendmail.py'), 'subscribe', req.body.email]);
        process.stdout.on('data', function (data){
          util.log(data.toString())
        });
      }
    } else {
      status = 'Fail';
      info   = 'Your email is not valid!'
    }
    res.send({
      'status': status,
      'info': info
    })
  });
});

router.post('/del', function(req, res, next) {
  fs.readFile(path.join(__dirname, '../data/users.json'), function(err, data) {
    if (err) throw err;
    var data = JSON.parse(data);
    var status = null;
    var info   = null;
    
    if(validate(req.body.email)) {
      if(data.users.indexOf(req.body.email) > -1) {
        data.users.splice(data.users.indexOf(req.body.email), 1)
        fs.writeFileSync(path.join(__dirname, '../data/users.json'), JSON.stringify(data));
        status = 'Success';
        info   = 'You have unsubscribed mail notification.';
        var process = spawn('python3', [path.join(__dirname, '../monitor/sendmail.py'), 'unsubscribe', req.body.email]);        process.stdout.on('data', function (data){
          util.log(data.toString())
        });
      } else {
        status = 'Fail';
        info   = 'You are not subscribed yet.';
      }
    } else {
      status = 'Fail';
      info   = 'Your email is not valid!';
    }
    res.send({
      'status': status,
      'info': info
    })
  })
});

module.exports = router;
