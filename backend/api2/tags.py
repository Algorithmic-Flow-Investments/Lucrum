from typing import Dict

from werkzeug.datastructures import MultiDict

from database import db
from models import Tag


def tags_list(query: MultiDict):
	tags = Tag.query
	return [tag.data_basic() for tag in tags.all()]


def update(tag_id: int, data: Dict):
	tag = Tag.query.filter(Tag.id == tag_id).first()
	if data['category_id'] is not None:
		tag.category_id = data['category_id']

	db.session.commit()
	return tag.data_extra()
