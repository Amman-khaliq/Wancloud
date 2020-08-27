from flask import Flask,request,jsonify, abort, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_httpauth import HTTPBasicAuth
import models

#Setting up the connection
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost/wancloudDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Connection to the mysql DB
db = SQLAlchemy(app)

#FOr schemas
ma = Marshmallow(app)

#Used for signup/login
auth = HTTPBasicAuth()

#to check whether someone is logged in or not
login_check = False



#This creates tables in DB if they are already not created
db.create_all()



item_schema = models.ItemSchema()
items_schema = models.ItemSchema(many=True)
user_schema = models.UserSchema()


#This signs up a new user
@app.route('/signup', methods=['POST'])
def new_user():
    username = request.json.get('username')
    name = request.json.get('name')
    password = request.json.get('password_hash')
    number = request.json.get('number')
    if username is None or password is None:
        abort(400)    # missing arguments
    if models.User.query.filter_by(username=username).first() is not None:
        abort(400)
        # existing user
    user = models.User(username, name, password, number)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return (jsonify({'username': user.username}), 201,
            {'Location': url_for('new_user', _external=True)})


#This logs in a user
@app.route('/login', methods=['POST'])
def login_user():
    username = request.json.get('username')
    password = request.json.get('password_hash')
    userr = models.User.query.get(username)
    if userr.verify_password(password):
        login_check = True
        return("logged in")
    else:
        return("Try Again with correct email and password")


#This adds a new item into the lost and found

@app.route('/items',methods = ['POST'])
def create_item():
    name = request.json['name']
    location = request.json['location_item']
    description = request.json['description']
    date = request.json['datee']
    nItem = models.Item(name,location,description,date)
    db.session.add(nItem)
    db.session.commit()
    return items_schema.jsonify(nItem)


#To get all items in the lost and found
@app.route('/items',methods = ['GET'])
def get_item():
    allitems = models.Item.query.all()
    result = items_schema.dump(allitems)
    return jsonify(result)

#Get specific item
@app.route('/items/<id>',methods = ['GET'])
def get_item1(id):
    item = models.Item.query.get(id)
    return item_schema.jsonify(item)

#to update an item
@app.route('/items/<id>',methods = ['PUT'])
def update_item(id):
    item = models.Item.query.get(id)
    name = request.json['name']
    location = request.json['location_item']
    description = request.json['description']
    date = request.json['datee']
    item.title = name
    item.location_item = location
    item.description = description
    item.datee = date

    db.session.commit()
    return item_schema.jsonify(item)

#To delete an item
@app.route('/items/<id>',methods = ['DELETE'])
def delete_item(id):
    item = models.Item.query.get(id)
    db.session.delete(item)
    db.session.commit()
    return item_schema.jsonify(item)

if __name__ == "__main__":
    app.run(debug = True)

