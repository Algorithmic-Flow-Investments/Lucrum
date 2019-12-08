from models import Method, MethodString, Target, TargetString, Category, Tag, Budget
from . import METHODS, TARGETS, CATEGORIES, TAGS
from database import db
from logging import warn, info


def load_methods():
	load_data(METHODS, Method, MethodString)
	db.session.commit()


def load_targets():
	load_data(TARGETS, Target, TargetString)
	db.session.commit()


def load_categories():
	for name in CATEGORIES:
		c = Category(name)
		db.session.add(c)
	db.session.commit()


def load_tags():
	for name, data in TAGS.items():
		tag = Tag.query.filter_by(name=name).first()
		if tag is None:
			tag = Tag(name)
			db.session.add(tag)

		category = Category.query.filter_by(name=data[1]).first()
		if category is not None:
			tag.category_id = category.id
		for target_name in data[0]:
			t = Target.query.filter_by(name=target_name).first()
			if t is None:
				warn(f'{t} is not a target')
				continue
			tag.targets.append(t)
	db.session.commit()


def load_data(data, parent_model, string_model):
	for name, strings in data.items():
		parent = parent_model.query.filter_by(name=name).first()
		if parent is None:
			parent = parent_model(name)
			db.session.add(parent)
		db.session.commit()

		for string in strings:
			s = string_model(parent, string)
			db.session.add(s)


def load_default_budget():
	if Budget.query.filter_by(name='Overall').first() is None:
		b = Budget('Overall')
		b.categories = [category for category in Category.query.all()]
		db.session.add(b)
		db.session.commit()


def load_all():
	info('Loading all prebuilt data...')
	load_methods()
	load_targets()
	load_categories()
	load_tags()
	load_default_budget()
