from typing import Dict

from ..database import db
from .base import BaseModel


class Category(BaseModel):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), nullable=False)
	tags = db.relationship('Tag', backref='category')
	budgets = db.relationship('Budget', secondary='budget_categories')

	def __init__(self, name):
		self.name = name

	def data_basic(self) -> Dict:
		return {'id': self.id, 'name': self.name}
