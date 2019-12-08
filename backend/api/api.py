from logging import debug

from dateutil.parser import parse
from flask import Blueprint, jsonify, request

from api import transactions
from api import accounts
from database import db
from models import Tag, Category, Budget
from models.account import Account
from models.scheduled import ScheduledTransaction
from models.transaction import Transaction, Target, TargetString, Method, MethodString
from server_data import new_database, populate_database

api = Blueprint('api', __name__)


@api.route('/api/accounts/list')
def accounts_basic():
	accounts = Account.query.all()
	return jsonify([account.data_basic() for account in accounts])


@api.route('/api/accounts/list/advanced')
def accounts_advanced():
	return jsonify(accounts.show_list())


@api.route('/api/scheduled')
def scheduled_basic():
	scheduled = ScheduledTransaction.query.all()
	return jsonify([transaction.data_basic() for transaction in scheduled])


@api.route('/api/transactions/list')
def transactions_list():
	minDate = parse(request.args.get('min', '1970-01-01'))
	maxDate = parse(request.args.get('max', '2100-01-01'))
	targetID = request.args.get('target_id', None, type=int)
	idOnly = request.args.get('id_only', False) == 'true'
	return jsonify(transactions.show_list(minDate, maxDate, targetID, idOnly))


@api.route('/api/transactions/stats')
def transactions_stats():
	minDate = parse(request.args.get('min', '1970-01-01'))
	maxDate = parse(request.args.get('max', '2100-01-01'))
	budget = request.args.get('budget', 1)
	return jsonify(transactions.stats(minDate, maxDate, budget))


@api.route('/api/transactions/graph')
def transaction_graph():
	minDate = parse(request.args.get('min', '1970-01-01'))
	maxDate = parse(request.args.get('max', '2100-01-01'))
	budget = request.args.get('budget', 1)
	return jsonify(transactions.graph(minDate, maxDate, budget))


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


@api.route('/api/targets/list')
def targets_basic():
	targets = Target.query.all()
	return jsonify([target.data_basic() for target in targets])


@api.route('/api/methods')
def methods_basic():
	methods = Method.query.all()
	return jsonify([method.data_basic() for method in methods])


@api.route('/api/target/<id>', methods=['GET'])
def target_advanced(id):
	target = Target.query.filter_by(id=id).first()
	if target is None:
		target = Target('')
	return jsonify(target.data_advanced())


@api.route('/api/target/<id>/edit', methods=['POST'])
def target_edit(id):
	data = request.json
	target = Target.query.filter_by(id=id).first()
	if target is None:
		target = Target('')
		db.session.add(target)
		if Target.query.filter_by(name=data['name']).first() is not None:
			return 'EXISTS', 409
	target.name = data['name']
	updated = []
	if 'strings' in data:
		for string in data['strings']:
			target_string = target.substrings.filter_by(id=string['id']).first()
			if target_string is None:
				target_string = TargetString(target, string['string'])
				db.session.add(target_string)
			else:
				target_string.string = string['string']
		for string in target.substrings:
			if string.string not in [s['string'] for s in data['strings']]:
				db.session.delete(string)

		db.session.flush()

		updated = [transaction.id for transaction in Transaction.query.filter(Transaction.target_id == target.id).all()]
		for transaction in Transaction.query.all():
			changed = transaction.process()
			if changed:
				updated.append(transaction.id)

	if 'tags' in data:
		for tag in data['tags']:
			target.tags.append(Tag.query.filter_by(id=tag['id']).first())

	db.session.commit()

	return jsonify({'target': target.data_advanced(), 'updated': updated})


@api.route('/api/target/<id>/delete', methods=['DELETE'])
def target_delete(id):
	updated = [transaction.id for transaction in Transaction.query.filter(Transaction.target_id == id).all()]
	Target.query.filter_by(id=id).delete()
	db.session.commit()
	return jsonify(updated)


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
				return 'EXISTS'
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
		return ''


@api.route('/api/tags/list')
def list_tags():
	return jsonify([tag.data_basic() for tag in Tag.query.all()])


@api.route('/api/tag/<id>/edit', methods=['POST'])
def edit_tag(id):
	data = request.json
	tag = Tag.query.filter_by(id=id).first()
	if data['category'] is not None:
		tag.category_id = data['category']['id']

	db.session.commit()
	return ""


@api.route('/api/categories/list')
def list_categories():
	return jsonify([category.data_basic() for category in Category.query.all()])


@api.route('/api/budgets/list')
def list_budgets():
	return jsonify([budget.data_basic() for budget in Budget.query.all()])


@api.route('/api/meta/stats')
def meta_stats():
	return jsonify({
		'transactions': Transaction.query.count(),
		'latest': Transaction.query.order_by(Transaction.date.desc()).first().date
	})


@api.route('/api/meta/rebuild', methods=['POST'])
def rebuild():
	new_database()
	populate_database(False, latest=False)
	return ""


@api.route('/api/meta/populate', methods=['POST'])
def populate():
	populate_database(True)
	return ""
