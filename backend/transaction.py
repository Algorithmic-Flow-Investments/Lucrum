from database import db


class Transaction(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	amount = db.Column(db.Float, nullable=False)
	date = db.Column(db.DateTime, nullable=False)
	raw_info = db.Column(db.Text, nullable=True)

	tags = db.relationship('Tag', secondary='transaction_tags')

	target_id = db.Column(db.Integer, db.ForeignKey('target.id'), nullable=True)
	target = db.relationship('Target', backref=db.backref('transactions', lazy=True), foreign_keys=[target_id])

	method_id = db.Column(db.Integer, db.ForeignKey('method.id'), nullable=True)
	method = db.relationship('Method', backref=db.backref('transactions', lazy=True), foreign_keys=[method_id])

	account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
	account = db.relationship('Account', backref=db.backref('transactions', lazy=True), foreign_keys=[account_id])

	def __init__(self, account, amount, date, tags=[], target=None, method=None, info=None):
		self.account = account
		self.raw_info = info  # type: str
		self.amount = float(amount)
		self.date = date

		for tag in tags:
			if type(tag) == str:
				tag = Tag.query.filter_by(name=tag).first()
			if type(tag) == tuple:
				proportion = tag[1]
				if type(tag[0]) == str:
					tag = Tag.query.filter_by(name=tag[0]).first()
				else:
					tag = tag[0]
				with db.session.no_autoflush:
					link = TransactionTags(self, tag, proportion)
					db.session.add(link)

			if tag is not None:
				self.tags.append(tag)

		if type(target) == str:
			target = Target.query.filter_by(name=target).first()

		if target is not None:
			self.target = target

		if type(method) == str:
			method = Method.query.filter_by(name=method).first()

		if method is not None:
			self.target = method

		self.process()

	def process_type(self, dataString, one=True):
		raw = self.raw_info.lower()
		for datStr in dataString.query.all():
			if raw.find(datStr.string) != -1:
				datStr.parent.transactions.append(self)
				if one: return

	def process(self):
		if self.raw_info is not None:
			self.process_type(TagString, False)
			self.process_type(TargetString)
			self.process_type(MethodString)

			"""print(self.raw_info , '==>')
			print(self.tags)
			print(self.method)
			print(self.target)"""

	def __repr__(self):
		return "<Transaction {} at {} using {} tags: {}>".format(self.amount, self.target, self.method, self.tags)

	def data_basic(self):
		return {'amount': self.amount, 'id': self.id, 'date': self.date,
				'target': self.target.data_basic() if self.target is not None else {'name': self.raw_info, 'internal': False, 'exists': False, 'id': -1},
				'tags': [tag.data_basic() for tag in self.tags]}

	def data_advanced(self):
		return {'amount': self.amount, 'id': self.id, 'date': self.id,
				'target': self.target.data_advanced() if self.target is not None else {'name': self.raw_info, 'internal': False, 'exists': False, 'id': -1},
				'tags': [tag.data_advanced(self) for tag in self.tags],
				'raw': self.raw_info,
				'method': self.method.data_basic() if self.method is not None else None}


class Tag(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), nullable=False)
	transactions = db.relationship('Transaction', secondary='transaction_tags')

	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return '<Tag "' + self.name + '">'

	def proportion(self, transaction):
		return TransactionTags.query.filter_by(tag_id=self.id, transaction_id=transaction.id).first().proportion

	def data_basic(self):
		return {'name': self.name, 'id': self.id}

	def data_advanced(self, transaction):
		return {'name': self.name, 'id': self.id, 'proportion': self.proportion(transaction)}


class TagString(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	string = db.Column(db.Text, nullable=False)

	parent_id = db.Column(db.Integer, db.ForeignKey(Tag.id), nullable=True)
	parent = db.relationship(Tag, backref=db.backref('substrings', lazy=True), foreign_keys=[parent_id])

	def __init__(self, parent, string):
		parent.substrings.append(self)
		self.string = str(string).lower()


class TransactionTags(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))
	transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'))
	proportion = db.Column(db.Float, nullable=True)

	def __init__(self, transaction, tag, proportion=None):
		self.transaction_id = transaction.id
		self.tag_id = tag.id
		self.proportion = proportion


"""
transaction_tags = db.Table('transaction_tags',
	db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
	db.Column('transaction_id', db.Integer, db.ForeignKey('transaction.id'), primary_key=True)
)"""

scheduled_tags = db.Table('scheduled_tags',
							db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
							db.Column('scheduled_transaction_id', db.Integer, db.ForeignKey('scheduled_transaction.id'),
								primary_key=True)
							)


class Target(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), nullable=False)

	internal_account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=True)
	internal_account = db.relationship('Account', backref=db.backref('internal_transactions', lazy=True),
										foreign_keys=[internal_account_id])

	def __init__(self, name):
		self.name = name
		from account import Account
		acc = Account.query.filter_by(name=self.name).first()
		if acc is not None:
			self.internal_account = acc

	def __repr__(self):
		if self.internal_account is not None:
			return '<Target ' + str(self.internal_account) + '>'
		return '<Target "' + self.name + '">'

	def data_basic(self):
		return {'name': self.name, 'id': self.id, 'internal': self.internal_account is not None, 'exists': True}

	def data_advanced(self):
		return {'name': self.name, 'id': self.id, 'internal': self.internal_account is not None, 'exists': True,
		        'strings': [string.data_basic() for string in self.substrings]}


class TargetString(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	string = db.Column(db.Text, nullable=False)

	parent_id = db.Column(db.Integer, db.ForeignKey(Target.id), nullable=True)
	parent = db.relationship(Target, backref=db.backref('substrings', lazy='dynamic'), foreign_keys=[parent_id])

	def __init__(self, parent, string):
		parent.substrings.append(self)
		self.string = str(string).lower()

	def data(self):
		return {'string': self.string, 'id': self.id}


class Method(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), nullable=False)

	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return '<Method "' + self.name + '">'

	def data_basic(self):
		return {'name': self.name, 'id': self.id}

	def data_advanced(self):
		return {'name': self.name, 'id': self.id, 'strings': [string.data_basic() for string in self.substrings]}


class MethodString(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	string = db.Column(db.Text, nullable=False)

	parent_id = db.Column(db.Integer, db.ForeignKey(Method.id), nullable=True)
	parent = db.relationship(Method, backref=db.backref('substrings', lazy='dynamic'), foreign_keys=[parent_id])

	def __init__(self, parent, string):
		parent.substrings.append(self)
		self.string = str(string).lower()

	def data(self):
		return {'string': self.string, 'id': self.id}
