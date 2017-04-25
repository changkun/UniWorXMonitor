var express = require('express');
var MongoClient = require('mongodb').MongoClient;
var assert = require('assert');

var fs = require('fs')
var path = require('path')
var router = express.Router();
var url = 'mongodb://localhost:27017/uniworx';

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

// url: /uniworx/logs
// params: 
//   - date: ISODate format
// response:
//   - array of records, reversed order by time
router.post('/logs', function(req, res, next) {
	var date = req.body.date.split('T')[0]
	var queryDate = new Date(date+'T00:00:00.000Z')
	var tomorrow = new Date(queryDate)
	tomorrow.setDate(queryDate.getDate()+1)
	MongoClient.connect(url, function(err, db) {
		assert.equal(null, err);
		var logs = db.collection('logs')
		logs.find({
			'time': {
				'$gt': queryDate,
				'$lt': tomorrow
			}
		}, {
			'_id': 0
		}).sort({'time': -1}).toArray(function(err, items) {
			assert.equal(null, err)
			var results = {
				'time': date,
				'apply': [],
				'not_possible': []
			}
			items.forEach(function(item) {
				item.apply.forEach(function(i) {
					results.apply.push(i)
				})
				item.not_possible.forEach(function(i) {
					results.apply.push(i)
				})
			})
			res.json(results)
		})
		db.close();
	});
});

router.use('/users', function(req, res, next) {
	MongoClient.connect(url, function(err, db) {
		assert.equal(null, err);
		var users = db.collection('users')

		var status = null;
    var info   = null;
		if (req.method === 'POST') {
			console.log('POST: '+req.body.email)
			if (validate(req.body.email)) {
				users.findOne({'email': req.body.email}, function(err, document) {
					if (document) {
						status = 'Fail';
						info   = 'You already subscribed!';
					} else {
						users.insert({
							'email': req.body.email
						});
						status = 'Success';
						info   = 'You has become our user!';
					}
					res.send({
						'status': status,
						'info': info
					});return;
				})
			} else {
				status = 'Fail';
	      info   = 'Your email is not valid!'
				res.send({
					'status': status,
					'info': info
				});
				return;
			}
		} else if (req.method == 'DELETE') {
			if (validate(req.body.email)) {
				users.findOne({'email': req.body.email}, function(err, document) {
					if (document) {
						users.deleteMany({
							'email': req.body.email
						});
						status = 'Success';
						info   = 'You have unsubscribed mail notification.';
						res.send({
							'status': status,
							'info': info
						});
						return;
					} else {
						status = 'Fail';
						info   = 'You are not subscribed yet.';
						res.send({
							'status': status,
							'info': info
						});
						return;
					}
				})
			} else {
				status = 'Fail';
				info   = 'Your email is not valid!'
				res.send({
					'status': status,
					'info': info
				});
			}
			
		} else if (req.method == 'GET') {
			
			var mails = []
			users.find({}, {'_id':0}).toArray(function(err, items) {
				if (items.length !== 0) {
					items.forEach(function(user) {
						var secreatUser = '';
						for(index in user.email) {
							if (index > 2) {
								secreatUser += '*';
							} else {
								secreatUser += user.email[index];
							}
						}
						mails.push(secreatUser);
					})
				}
				res.send({
					'users': mails
				})
				return;
			});
		} else {
			res.send({'error': 'method error: '+err})
			return;
		}
	})
})

router.post('/courses', function(req, res, next) {
	var semester = req.body.semester

	MongoClient.connect(url, function(err, db) {
		assert.equal(null, err);
		var logs = db.collection('logs')
		logs.find({
			'time': {
				'$gt': queryDate,
				'$lt': tomorrow
			}
		}, {
			'_id': 0
		}).sort({'time': -1}).toArray(function(err, items) {
			assert.equal(null, err)
			res.json(items)
		})
		db.close();
	});
})

module.exports = router;