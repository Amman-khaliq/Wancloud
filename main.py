from flask import Flask,request,jsonify, abort, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_httpauth import HTTPBasicAuth
from blueprints import LF_blueprint
#from blueprints.items import item_model, add_item_view

#LFblueprint = Blueprint('LF_blueprint', __name__)

#Setting up the connection
app = Flask(__name__)
#app.register_blueprint(LF_blueprint.blueprintt)
#app.register_blueprint(models.models)
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




#This signs up a new user
@app.route('/signup', methods=['POST'])
def new_user():
    username = request.json.get('username')
    name = request.json.get('name')
    password = request.json.get('password_hash')
    number = request.json.get('number')
    if username is None or password is None:
        abort(400)    # missing arguments
    if LF_blueprint.User.query.filter_by(username=username).first() is not None:
        abort(400)
        # existing user
    user = LF_blueprint.User(username, name, password, number)
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
    userr = LF_blueprint.User.query.get(username)
    if userr.verify_password(password):
        login_check = True
        return("logged in")
    else:
        return("Try Again with correct username and password")




#This adds a new item into the lost and found
@app.route('/items',methods = ['POST'])
def create_item():
    name = request.json['name']
    location = request.json['location_item']
    description = request.json['description']
    date = request.json['datee']
    nItem = LF_blueprint.Item(name, location, description, date)
    db.session.add(nItem)
    db.session.commit()
    return LF_blueprint.items_schema.jsonify(nItem)



#To get all items in the lost and found
@app.route('/items',methods = ['GET'])
def get_item():
    allitems = LF_blueprint.Item.query.all()
    result = LF_blueprint.items_schema.dump(allitems)
    return jsonify(result)

#Get specific item
@app.route('/items/<id>',methods = ['GET'])
def get_item1(id):
    item = LF_blueprint.Item.query.get(id)
    return LF_blueprint.item_schema.jsonify(item)

#to update an item
@app.route('/items/<id>',methods = ['PUT'])
def update_item(id):
    item = LF_blueprint.Item.query.get(id)
    name = request.json['name']
    location = request.json['location_item']
    description = request.json['description']
    date = request.json['datee']
    item.title = name
    item.location_item = location
    item.description = description
    item.datee = date

    db.session.commit()
    return LF_blueprint.item_schema.jsonify(item)

#To delete an item
@app.route('/items/<id>',methods = ['DELETE'])
def delete_item(id):
    item = LF_blueprint.Item.query.get(id)
    db.session.delete(item)
    db.session.commit()
    return LF_blueprint.item_schema.jsonify(item)

if __name__ == "__main__":
    app.run(debug = True)

