from flask import Blueprint, jsonify, request, Response, stream_with_context

from api2 import transactions, targets, methods, accounts, budgets, meta, tags, categories
from processing.process_transactions import update_all
from processing.task_queue import EventManager
from server_data import populate_database

api = Blueprint('api2', __name__, url_prefix='/api/v2')

####
# Transactions
####


@api.route('/transactions/list')
def transactions_list() -> Response:
	return jsonify(transactions.transactions_list(request.args))


@api.route('/transactions/stats')
def transactions_stats() -> Response:
	return jsonify(transactions.stats(request.args))


@api.route('/transactions/stats/outgoings_graph')
def transactions_outgoings_graph() -> Response:
	return jsonify(transactions.graph(request.args)) \
 \
 \
   @api.route('/transactions/stats/tags_categories')


def transactions_tags_categories() -> Response:
	return jsonify(transactions.tags_categories(request.args))


@api.route('/transactions/get/<int:transaction_id>')
def transactions_get(transaction_id) -> Response:
	return jsonify(transactions.get(transaction_id))


@api.route('/transactions/update/<int:transaction_id>', methods=['POST'])
def transactions_update(transaction_id) -> Response:
	return jsonify(transactions.update(transaction_id, request.json))


@api.route('/transactions/process', methods=['POST'])
def transactions_process() -> Response:
	return jsonify(transactions.process(request.args))


####
# Targets
####


@api.route('/targets/list')
def targets_list() -> Response:
	return jsonify(targets.targets_list(request.args))


@api.route('/targets/get/<int:target_id>')
def targets_get(target_id) -> Response:
	return jsonify(targets.get(target_id))


@api.route('/targets/add', methods=['POST'])
def targets_add() -> Response:
	return jsonify(targets.add(request.json))


@api.route('/targets/delete/<int:target_id>', methods=['DELETE'])
def targets_delete(target_id) -> Response:
	return jsonify(targets.delete(target_id))


@api.route('/targets/update/<int:target_id>', methods=['POST'])
def targets_update(target_id) -> Response:
	return jsonify(targets.update(target_id, request.json))


####
# Methods
####


@api.route('/methods/list')
def methods_list() -> Response:
	return jsonify(methods.methods_list(request.args))


###
# Accounts
####


@api.route('/accounts/list')
def accounts_list() -> Response:
	return jsonify(accounts.accounts_list(request.args))


@api.route('/accounts/get/<int:account_id>')
def accounts_get(account_id) -> Response:
	return jsonify(accounts.get(account_id))


@api.route('accounts/stats/balance_graph')
def accounts_balance_graph() -> Response:
	return jsonify(accounts.accounts_balance_graph(request.args))


####
# Tags
####


@api.route('/tags/list')
def tags_list() -> Response:
	return jsonify(tags.tags_list(request.args))


@api.route('/tags/update/<int:tag_id>', methods=['POST'])
def tags_update(tag_id) -> Response:
	return jsonify(tags.update(tag_id, request.json))


####
# Categories
####


@api.route('/categories/list')
def categories_list() -> Response:
	return jsonify(categories.categories_list(request.args))


####
# Budgets
####


@api.route('/budgets/list')
def budgets_list() -> Response:
	return jsonify(budgets.budgets_list(request.args))


####
# Meta
####


@api.route('/meta/stats')
def meta_stats() -> Response:
	return jsonify(meta.stats(request.args))


@api.route('/meta/populate', methods=['POST'])
def populate() -> Response:
	populate_database(True, False)
	return jsonify()


@api.route('/meta/update', methods=['POST'])
def update_all_transactions() -> Response:
	update_all(False)
	return jsonify()


####
# Subscribe
####


@api.route('/subscribe')
def subscribe() -> Response:
	con = EventManager.new_connection()
	return Response(stream_with_context(con.get_stream()), mimetype='text/event-stream')
