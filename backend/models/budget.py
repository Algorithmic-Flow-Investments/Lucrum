import enum
from datetime import date

from sqlalchemy import func

from database import db
from models.base import BaseModel
from models import Category, Transaction, Tag


class Budget(BaseModel):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), nullable=False)
	total = db.Column(db.Float, nullable=True)

	class Period(enum.Enum):
		WEEK = 1
		MONTH = 2

	period = db.Column(db.Enum(Period), nullable=True)
	startDate = db.Column(db.Date, nullable=True)
	endDate = db.Column(db.Date, nullable=True)
	categories = db.relationship('Category', secondary='budget_categories')

	def __init__(self, name, total=None, start=None, end=date.max, period=None):
		self.name = name
		self.total = total
		self.period = period
		self.startDate = start
		self.endDate = end

	def data_basic(self):
		return {'id': self.id, 'name': self.name, 'categories': [cat.id for cat in self.categories]}

	@property
	def start(self):
		if self.startDate:
			return self.startDate
		return self.transactions.order_by(Transaction.date).first().date

	@property
	def transactions(self):
		start = self.startDate
		if start is None:
			start = date.min
		return Transaction.query \
                                 .join(Transaction.tags, isouter=True) \
                                 .join(Tag.category, isouter=True) \
                                 .join(Category.budgets, isouter=True) \
                                 .filter(Budget.id == self.id) \
                                 .filter(Transaction.date >= start, Transaction.date <= self.endDate)

	@property
	def per_day(self):
		if self.total is None:
			return None
		return self.per_week / 7

	@property
	def per_week(self):
		if self.total is None:
			return None
		if self.period == Budget.Period.WEEK:
			return self.total
		if self.period == Budget.Period.MONTH:
			return self.total * 12 / 52

	@property
	def per_month(self):
		if self.total is None:
			return None
		if self.period == Budget.Period.WEEK:
			return self.total * 52 / 12
		if self.period == Budget.Period.MONTH:
			return self.total

	@property
	def current_budget(self):
		if self.total is None:
			return None
		return (date.today() - self.start).days * self.per_day

	def stats(self):
		return {
			'total': self.transactions.with_entities(func.sum(Transaction.amount)).scalar(),
			'weekly_budget': self.per_week,
			'monthly_budget': self.per_month,
			'current_budget': self.current_budget
		}


budget_categories = db.Table('budget_categories', db.Column('category_id', db.Integer, db.ForeignKey(Category.id)),
								db.Column('budget_id', db.Integer, db.ForeignKey(Budget.id)))
