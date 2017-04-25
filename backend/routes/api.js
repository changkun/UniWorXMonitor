var express = require('express');
var MongoClient = require('mongodb').MongoClient;
var assert = require('assert');

var fs = require('fs')
var path = require('path')
var router = express.Router();

var utils = require('../tools/utils')

const url = 'mongodb://localhost:27017/uniworx';

// url: /api/v1/logs
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

// url: /api/v1/users
// - GET:
// 	+ response: return all encrypted user email
// - POST:
//  + body: 	{ 'email': 'user_email' }
//  + response: return post results: {'status': 'Fail/Success', 'info': 'reason'}
// - DELETE:
//  + body: 	{ 'email': 'user_email' }
//  + response: return delete results as same as POST
router.use('/users', function(req, res, next) {
	MongoClient.connect(url, function(err, db) {
		assert.equal(null, err);
		var users = db.collection('users')

		var status = null;
    var info   = null;
		if (req.method === 'POST') {
			console.log('POST: '+req.body.email)
			if (utils.validate(req.body.email)) {
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
		} else if (req.method === 'DELETE') {
			if (utils.validate(req.body.email)) {
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
		} else if (req.method === 'GET') {
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

// url: /api/v1/courses
// - GET:
// - POST:
router.post('/courses', function(req, res, next) {
	MongoClient.connect(url, function(err, db) {
		assert.equal(null, err);
		
		// TODO: fix me

		db.close();
	});
})

module.exports = router;