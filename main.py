from flask import Flask,request,jsonify, abort, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash


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


#User Class for signing up of new user
class User(db.Model):
    __tablename__ = 'users'
    #id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), primary_key=True, unique=True, index=True)
    password_hash = db.Column(db.String(120))

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)



#Item Class for lost and found items
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    location_item = db.Column(db.String(100))
    description = db.Column(db.String(100))
    datee = db.Column(db.String(50))

    def __init__(self, name,loc, description,date):
        self.name = name
        self.location_item = loc
        self.description = description
        self.datee = date


#This creates tables in DB if they are already not created
db.create_all()


#Schemas to help us when we make HTTP request
class ItemSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'location_item', 'description','datee')


class UserSchema(ma.Schema):
    class Meta:
        fields = ('username', 'password_hash')


item_schema = ItemSchema()
items_schema = ItemSchema(many=True)
user_schema = UserSchema()


#This signs up a new user
@app.route('/signup', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password_hash')
    print('hhhhh',password)
    if username is None or password is None:
        abort(400)    # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        abort(400)
        # existing user
    user = User(username=username)
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
    userr = User.query.get(username)
    if userr.verify_password(password):
        return("logged in")
    else:
        return("Wrong password")


#This adds a new item into the lost and found
@app.route('/items',methods = ['POST'])
def create_item():
    name = request.json['name']
    location = request.json['location_item']
    description = request.json['description']
    date = request.json['datee']
    nItem = Item(name,location,description,date)
    db.session.add(nItem)
    db.session.commit()
    return items_schema.jsonify(nItem)


#To get all items in the lost and found
@app.route('/items',methods = ['GET'])
def get_item():
    allitems = Item.query.all()
    result = items_schema.dump(allitems)
    return jsonify(result)

#Get specific item
@app.route('/items/<id>',methods = ['GET'])
def get_item1(id):
    item = Item.query.get(id)
    return item_schema.jsonify(item)

#to update an item
@app.route('/items/<id>',methods = ['PUT'])
def update_item(id):
    item = Item.query.get(id)
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
    item = Item.query.get(id)
    db.session.delete(item)
    db.session.commit()
    return item_schema.jsonify(item)


if __name__ == "__main__":
    app.run(debug = True)