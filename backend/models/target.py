from database import db


class Target(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), nullable=False)

	internal_account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=True)
	internal_account = db.relationship('Account', foreign_keys=[internal_account_id])

	substrings = db.relationship('TargetString', backref='parent', lazy='dynamic', passive_deletes=True)

	tags = db.relationship('Tag', secondary='target_tags')

	def __init__(self, name, internal_account=None):
		self.name = name
		"""if internal_account:
			self.internal_account_id = internal_account.id
		else:
			from models.account import Account
			acc = Account.query.filter_by(name=self.name).first()
			if acc is not None:
				self.internal_account = acc"""

	def __repr__(self):
		if self.internal_account is not None:
			return '<Target ' + str(self.internal_account) + '>'
		return '<Target "' + self.name + '">'

	def data_basic(self):
		return {
			'name': self.name,
			'id': self.id,
			'is_internal': self.internal_account is not None,
			'tag_ids': [tag.id for tag in self.tags],
			'usages': len(self.transactions)
		}

	def data_extra(self):
		return dict(self.data_basic(), **{
			'strings': [string.data() for string in self.substrings],
		})


class TargetString(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	string = db.Column(db.Text, nullable=False)

	parent_id = db.Column(db.Integer, db.ForeignKey(Target.id, ondelete='CASCADE'), nullable=True)

	def __init__(self, parent, string):
		parent.substrings.append(self)
		self.string = str(string).lower()

	def data(self):
		return {'string': self.string, 'id': self.id}
