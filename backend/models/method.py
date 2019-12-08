from database import db


class Method(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), nullable=False)

	substrings = db.relationship('MethodString',
	                             backref='parent',
	                             lazy='dynamic',
	                             cascade='delete',
	                             passive_deletes=True)

	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return '<Method "' + self.name + '">'

	def data_basic(self):
		return {'name': self.name, 'id': self.id}

	def data_advanced(self):
		return {
		    'name': self.name,
		    'id': self.id,
		    'strings': [string.data() for string in self.substrings]
		}


class MethodString(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	string = db.Column(db.Text, nullable=False)

	parent_id = db.Column(db.Integer,
	                      db.ForeignKey(Method.id, ondelete='CASCADE'))

	def __init__(self, parent, string):
		parent.substrings.append(self)
		self.string = str(string).lower()

	def data(self):
		return {'string': self.string, 'id': self.id}
