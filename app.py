# Step 01: import necessary libraries/modules
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# your code begins here 

# Step 02: initialize flask app here 
app = Flask(__name__)
app.debug = True

# Step 03: add database configurations here
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://asm02_user:password@localhost:5432/asm02'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Step 04: import models
from models import User, Temperature

# Step 05: add routes and their binded functions here
@app.route('/user/', methods=['POST']) 
def create_user():
	print('create_user')

	# start your code after this line
	if 'name' and 'contact' in request.json:
		name = request.json['name'] 
		contact_number = request.json['contact'] 
	else:
		return "Please ensure you have written the field names correctly"

	if isinstance(name,str)==False:
		return "Please ensure your name is in the string format"

	if name=="":
		return "Please ensure your name is filled up"

	if isinstance(contact_number,int)==False:
		return "Please ensure your contact is in integer"

	try:
		new_user = User(name=name, contact_number=contact_number)
		db.session.add(new_user)
		db.session.commit() # this must be done before adding reviews
		if len(str(contact_number))==8:
			return jsonify('new user {}'.format(new_user))
		else:
			return "Please type an 8 digit number"
		
	except Exception as e:
		return (str(e))

	# end your code before this line

@app.route('/temp/', methods=['POST']) 
def create_temp():
	print('create_temp')

	# start your code after this line
	if 'name' and 'temp' in request.json:
		name = request.json['name']
		temp_value = request.json['temp']
	else:
		return "Please ensure you have written the field names correctly"
	
	if isinstance(name,str)==False or isinstance(temp_value,float)==False :
		return "Please make sure your input data types are correct. Check if your name is in string and temp is in float."
	
	if name=="":
		return "Please ensure your friend's name is filled up."

	try:
		searched_user = User.query.filter_by(name=name).first()
		if searched_user != None:
			searched_user_id = searched_user.id		
			new_temp = Temperature(temp_value=temp_value, user_id=searched_user_id)
			db.session.add(new_temp)
			db.session.commit()
			return jsonify('new temp record {} was created for user {}'.format(new_temp,name))
		else:
			return "Are you sure {} is your friend?".format(name)

		
	except Exception as e:
		return (str(e))
	# end your code before this line

@app.route('/friend/', methods=['PUT']) 
def update_friend():
	print('update_friend')

	# start your code after this line

	# start your code after this line
	user = request.json['user']
	mutual_friends = request.json['friends'] 
	# user = User.query.filter_by(name=user).first()

	try:
		mutual_friend_list = []
		for name in mutual_friends:
			# check_friend = User.query.filter_by(name=friend).first()
			check_friend = User.query.filter_by(name=name).first()
			# print(check_friend)
			contact_number = User.query.filter_by(contact_number=contact_number).first()
			print(User(name,contact_number).serialize())

			if check_friend is None:
				return ('There is a person in the friend list who is actually not our mutual friend')
			else:
				mutual_friend_list.append(name)

		if len(mutual_friend_list) ==0:
			return []
				
		print(mutual_friend_list)
		User.friends = mutual_friend_list
		db.session.commit()
		print(User(name,contact_number).serialize())
		return jsonify(User(name,contact_number).serialize())
		
	except Exception as e:
		return (str(e))

	# end your code before this line

@app.route('/user/', methods=['GET']) 
def get_user():
	print('get_user')

	# start your code after this line
	user = User.query.all()
	return jsonify([u.serialize() for u in user])
	# end your code before this line

@app.route('/temp/', methods=['GET']) 
def get_temp():
	print('get_temp')

	# start your code after this line
	if 'name' in request.args: #if want to search by description. 
		name = request.args.get('name') #what does this mean
		User_ = User.query.filter_by(name=name).first() #to check if it is the same as database #get the first item
		temp = Temperature.query.filter_by(user_id=User_.id) #gets all the reviews with the menu_id
		return jsonify([t.serialize() for t in temp])
	else:
		temp = Temperature.query.all()
		return jsonify([t.serialize() for t in temp])	
	# end your code before this line

# your code ends here 

if __name__ == '__main__':
	app.run(debug=True)


		# this must be done before adding reviews
	# except Exception as e:
	# 	return (str(e))

# 	# end your code before this line

