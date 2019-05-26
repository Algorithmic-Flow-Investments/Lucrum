from flask import Blueprint, jsonify, request
from database import db
from models.account import Account
from models.scheduled import ScheduledTransaction
from models.transaction import Transaction, Target, TargetString, Method, MethodString
from dateutil.parser import parse
from api import transactions

api = Blueprint('api', __name__)


@api.route('/api/accounts')
def accounts_basic():
	accounts = Account.query.all()
	return jsonify([account.data_basic() for account in accounts])


@api.route('/api/scheduled')
def scheduled_basic():
	scheduled = ScheduledTransaction.query.all()
	return jsonify([transaction.data_basic() for transaction in scheduled])


@api.route('/api/transactions/list')
def transactions_list():
	minDate = parse(request.args.get('min', '1970-01-01'))
	maxDate = parse(request.args.get('max', '2100-01-01'))
	return jsonify(transactions.show_list(minDate, maxDate))


@api.route('/api/transactions/stats')
def transactions_stats():
	minDate = parse(request.args.get('min', '1970-01-01'))
	maxDate = parse(request.args.get('max', '2100-01-01'))
	return jsonify(transactions.stats(minDate, maxDate))


@api.route('/api/transactions/graph')
def transaction_graph():
	minDate = parse(request.args.get('min', '1970-01-01'))
	maxDate = parse(request.args.get('max', '2100-01-01'))
	return jsonify(transactions.graph(minDate, maxDate))


@api.route('/api/transaction/<id>', methods=['GET', 'POST'])
def transaction_advanced(id):
	if request.method == 'GET':
		transaction = Transaction.query.filter_by(id=id).first()
		return jsonify(transaction.data())
	elif request.method == 'POST':
		data = request.json
		transaction = Transaction.query.filter_by(id=id).first()
		print(transaction)
		print(data)
		for key, value in data.items():
			if key == 'target':
				transaction.target_id = value

			if key == 'method':
				transaction.method_id = value

			if key == 'parent':
				transaction.parent_transaction_id = value
		db.session.commit()
		return jsonify(transaction.data())


@api.route('/api/targets')
def targets_basic():
	targets = Target.query.all()
	return jsonify([target.data_basic() for target in targets])


@api.route('/api/methods')
def methods_basic():
	methods = Method.query.all()
	return jsonify([method.data_basic() for method in methods])


@api.route('/api/target/<id>', methods=['GET', 'POST', 'DELETE'])
def target_advanced(id):
	if request.method == 'GET':
		target = Target.query.filter_by(id=id).first()
		if target is None:
			target = Target('')
		return jsonify(target.data_advanced())
	elif request.method == 'POST':
		data = request.json
		target = Target.query.filter_by(id=id).first()
		if target is None:
			target = Target('')
			db.session.add(target)
			if Target.query.filter_by(name=data['name']).first() is not None:
				return "EXISTS"
		target.name = data['name']
		for string in data['strings']:
			target_string = target.substrings.filter_by(id=string['id']).first()
			if target_string is None:
				target_string = TargetString(target, string['string'])
				db.session.add(target_string)
			else:
				target_string.string = string['string']
		for transaction in Transaction.query.all():
			transaction.process()
		db.session.commit()
		return jsonify({'id': target.id})
	elif request.method == 'DELETE':
		target = Target.query.filter_by(id=id).delete()
		db.session.commit()
		return ""


@api.route('/api/method/<id>', methods=['GET', 'POST', 'DELETE'])
def method_advanced(id):
	if request.method == 'GET':
		method = Method.query.filter_by(id=id).first()
		if method is None:
			method = Method('')
		return jsonify(method.data_advanced())
	elif request.method == 'POST':
		data = request.json
		method = Method.query.filter_by(id=id).first()
		if method is None:
			method = Method('')
			db.session.add(method)
			if Method.query.filter_by(name=data['name']).first() is not None:
				return "EXISTS"
		method.name = data['name']
		for string in data['strings']:
			method_string = method.substrings.filter_by(id=string['id']).first()
			if method_string is None:
				method_string = MethodString(method, string['string'])
				db.session.add(method_string)
			else:
				method_string.string = string['string']
		db.session.commit()
		return jsonify({'id': method.id})
	elif request.method == 'DELETE':
		Method.query.filter_by(id=id).delete()
		db.session.commit()
		return ""



"""@api.route('/api/target/<id>/string/<sid>', methods=['GET', 'POST'])
def target_string(id, sid):
	target = Target.query.filter_by(id=id).first()
	if target is None:
		target = Target('')
		db.session.add(target)
	target_string = target.substrings.filter_by(id=sid).first()
	if request.method == 'POST':
		if target_string is None:
			target_string = TargetString(target, request.json['string'])
			db.session.add(target_string)
		else:
			target_string.string = request.json['string']

	db.session.commit()"""
