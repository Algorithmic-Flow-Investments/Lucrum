from database import db
from models.tag import Tag
from models.target import Target


class ScheduledTransaction(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), nullable=False)
	amount = db.Column(db.Float, nullable=False)
	date = db.Column(db.DateTime, nullable=False)

	monthly = db.Column(db.Boolean, nullable=False)
	weekly = db.Column(db.Boolean, nullable=False)
	endDate = db.Column(db.DateTime, nullable=True)

	tags = db.relationship('Tag',
	                       secondary='scheduled_tags',
	                       lazy='subquery',
	                       backref=db.backref('scheduled', lazy=True))

	target_id = db.Column(db.Integer,
	                      db.ForeignKey('target.id'),
	                      nullable=True)
	target = db.relationship('Target',
	                         backref=db.backref('scheduled', lazy=True),
	                         foreign_keys=[target_id])

	def __init__(self,
	             name,
	             amount,
	             date,
	             tags=[],
	             target=None,
	             monthly=False,
	             weekly=False,
	             end_date=None):
		self.name = name
		self.amount = amount
		self.date = date
		self.monthly = monthly
		self.weekly = weekly
		self.endDate = end_date

		for tag in tags:
			if type(tag) == str:
				tag = Tag.query.filter_by(name=tag).first()

			if tag != None:
				self.tags.append(tag)

		if type(target) == str:
			target = Target.query.filter_by(name=target).first()

		if target != None:
			self.target = target

	# target.scheduled.append(self)

	def data_basic(self):
		return {
		    'name': self.name,
		    'amount': self.amount,
		    'id': self.id,
		    'date': self.date,
		    'internal': self.target.internal_account is not None
		}


scheduled_tags = db.Table(
    'scheduled_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('scheduled_transaction_id',
              db.Integer,
              db.ForeignKey('scheduled_transaction.id'),
              primary_key=True))
