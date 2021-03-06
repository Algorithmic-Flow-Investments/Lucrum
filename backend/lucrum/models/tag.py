from typing import Dict

from ..database import db
from .base import BaseModel
from .target import Target


class Tag(BaseModel):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), nullable=False)
	targets = db.relationship('Target', secondary='target_tags')
	category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return '<Tag "' + self.name + '">'

	def data_basic(self) -> Dict:
		return {
			'name': self.name,
			'id': self.id,
			'category_id': self.category_id,
			'uses': len(self.targets)  # TODO: get number of transactions
		}

	def data_extra(self):
		return dict(self.data_basic(), **{})


target_tags = db.Table('target_tags', db.Column('tag_id', db.Integer, db.ForeignKey(Tag.id)),
						db.Column('target_id', db.Integer, db.ForeignKey(Target.id)))

transaction_tags = db.Table('transaction_tags', db.Column('tag_id', db.Integer, db.ForeignKey(Tag.id)),
							db.Column('transaction_id', db.Integer, db.ForeignKey('transaction_manual.id')))
