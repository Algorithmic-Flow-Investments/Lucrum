from typing import Dict

from werkzeug.datastructures import MultiDict
from werkzeug.exceptions import abort

from database import db
from models import Target, TargetString, Transaction, Tag
from processing import process_transactions
from processing.task_queue import EventManager


def targets_list(query: MultiDict):
	targets = Target.query
	return [target.data_basic() for target in targets.all()]


def get(target_id: int):
	return Target.query.filter(Target.id == target_id).first().data_extra()


def add(data: Dict):
	print("Adding", data)
	if Target.query.filter(Target.name == data['name']).first() is not None:
		return abort(409)
	target = Target(data['name'])
	db.session.add(target)

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
	EventManager.putTargetsUpdatedEvent([target])
	db.session.commit()
	process_transactions.update_all()
	return target.data_extra()


def delete(target_id: int):
	updated = [transaction for transaction in Transaction.query.filter(Transaction.target_id == target_id).all()]
	Target.query.filter_by(id=target_id).delete()
	EventManager.putTransactionsUpdatedEvent(updated)
	db.session.commit()
	return "SUCCESS"


def update(target_id: int, data: Dict):
	do_update = False
	target = Target.query.filter_by(id=target_id).one()
	print("Updating target", target.data_extra(), data)
	target.name = data['name']
	for string in data['strings']:
		target_string = target.substrings.filter_by(id=string['id']).first()
		if target_string is None:
			target_string = TargetString(target, string['string'])
			db.session.add(target_string)
			do_update = True
		else:
			target_string.string = string['string']
	for string in target.substrings:
		if string.string not in [s['string'] for s in data['strings']]:
			db.session.delete(string)
			do_update = True

	if 'tag_ids' in data:
		for tag_id in data['tag_ids']:
			target.tags.append(Tag.query.filter_by(id=tag_id).first())
		for tag in target.tags:
			if tag.id not in data['tag_ids']:
				print("del", tag)
				target.tags.remove(tag)
	print("Done updating target", target.data_extra())
	# if 'tags' in data:
	# 	for tag in data['tags']:
	# 		target.tags.append(Tag.query.filter_by(id=tag['id']).first())
	EventManager.putTargetsUpdatedEvent([target])
	db.session.commit()
	if do_update:
		process_transactions.update_all()
	target = Target.query.filter_by(id=target_id).one()
	return target.data_extra()
