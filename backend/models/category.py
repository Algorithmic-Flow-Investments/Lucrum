from database import db


class Category(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), nullable=False)
	tags = db.relationship('Tag', backref='category')
	budgets = db.relationship('Budget', secondary='budget_categories')

	def __init__(self, name):
		self.name = name

	def data_basic(self):
		return {'id': self.id, 'name': self.name}
