import datetime

from app import db

friendship_table = db.Table('friendship',
db.Column('friend_from', db.Integer, db.ForeignKey('user.id'),
primary_key=True),
db.Column('friend_to', db.Integer, db.ForeignKey('user.id'),
primary_key=True))

class User(db.Model):
	__tablename__ = 'user'

	# start your code after this line
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), unique=True, nullable=False)
	contact_number = db.Column(db.Integer, unique=True, nullable=False)
	
	#one-to-many model
	temperatures = db.relationship('Temperature', back_populates='user', uselist= True, cascade='all,delete-orphan', lazy=True)

	# many-to-many model to the same class
	friends = db.relationship('User', secondary=friendship_table,
	primaryjoin=id == friendship_table.c.friend_to,
	secondaryjoin=id==friendship_table.c.friend_from)
	# end your code before this line

	def __init__(self, name, contact_number,temperatures=None):
		# start your code after this line
		self.name = name
		self.contact_number = contact_number
		self.temperatures = [] if temperatures is None else temperatures
		# end your code before this line

	def __repr__(self):
		return '{} was created with id {}'.format(self.name, self.id) 
		
	
	def serialize(self):
		# start your code after this line
		#querying all the temp records of a particular user
		user_temp_data = Temperature.query.filter_by(user_id = self.id).all()

		return {
			'contact_number': self.contact_number,
			'id':self.id,
			'name': self.name, 
			'temp_logs':[] if self.temperatures == [] else [{"temp":temp_entry.temp_value,"timestamp":temp_entry.timestamp} for temp_entry in user_temp_data]		
		}
		# end your code before this line

class Temperature(db.Model):
	__tablename__ = 'temperature'

	# start your code after this line
	id = db.Column(db.Integer, primary_key=True)
	timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
	temp_value = db.Column(db.Float, unique=False, nullable=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	
	#one-to-many model
	user = db.relationship('User', back_populates='temperatures')
	# end your code before this line

	def __init__(self, temp_value, user_id):
		# start your code after this line
		self.temp_value = temp_value
		self.user_id = user_id
		# end your code before this line

	def __repr__(self):
		return '{}'.format(self.temp_value) 
		
	def serialize(self):
		# start your code after this line
		return {
			'id':self.id,
			'user_id': self.user_id, 
			'temp_value': self.temp_value,
			'timestamp': self.timestamp,
			'user_name':User.query.filter_by(id=self.user_id).first().name
		}
		# end your code before this line


