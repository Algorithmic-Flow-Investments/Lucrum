from typing import Dict

from sqlalchemy import select
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property

from lucrum.database import db
from .base import BaseModel


class Target(BaseModel):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), nullable=False)

	# internal_account = db.relationship("Account", uselist=False)
	internal_account = db.relationship("Account", back_populates="target", uselist=False)
	internal_account_id = association_proxy('internal_account', 'id')

	substrings = db.relationship('TargetString', backref='parent', lazy='dynamic', passive_deletes=True)

	tags = db.relationship('Tag', secondary='target_tags')

	def __init__(self, name):
		self.name = name

	def __repr__(self):
		if self.internal_account is not None:
			return '<Target ' + str(self.internal_account) + '>'
		return '<Target "' + self.name + '">'

	def data_basic(self) -> Dict:
		return {
			'name': self.name,
			'id': self.id,
			'is_internal': self.internal_account is not None,
			'tag_ids': [tag.id for tag in self.tags],
			'usages': len(self.transactions)
		}

	def data_extra(self) -> Dict:
		return dict(self.data_basic(), **{
			'strings': [string.data() for string in self.substrings],
		})

	@property
	def transactions(self):
		transaction = next(table for table in BaseModel.__subclasses__() if table.__name__ == 'Transaction')
		return db.session.query(transaction).filter_by(target_id=self.id).all()

	@hybrid_property
	def is_internal(self):
		return self.internal_account is not None

	@is_internal.expression
	def is_internal(self):
		return self.internal_account_id != None

	# @hybrid_property
	# def internal_account_id(self):
	# 	return self.internal_account.id
	#
	# @internal_account_id.expression
	# def internal_account_id(cls):
	# 	from .account import Account
	# 	return select([Account.name]).where(cls.id == Account.target_id).as_scalar()


class TargetString(BaseModel):
	id = db.Column(db.Integer, primary_key=True)
	string = db.Column(db.Text, nullable=False)

	parent_id = db.Column(db.Integer, db.ForeignKey(Target.id, ondelete='CASCADE'), nullable=True)

	def __init__(self, parent, string):
		parent.substrings.append(self)
		self.string = str(string).lower()

	def data(self) -> Dict:
		return {'string': self.string, 'id': self.id}
