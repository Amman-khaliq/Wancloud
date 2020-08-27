import main
from werkzeug.security import generate_password_hash, check_password_hash

#User Class for signing up of new user
class User(main.db.Model):
    __tablename__ = 'users'
    #id = db.Column(db.Integer, primary_key=True)
    username = main.db.Column(main.db.String(32), primary_key=True, unique=True, index=True)
    name = main.db.Column(main.db.String(120))
    password_hash = main.db.Column(main.db.String(120))
    number = main.db.Column(main.db.String(35))


    def __init__(self, uname,name, passs,num):
        self.name = name
        self.username = uname
        self.password_hash = passs
        self.number = num


    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)



#Item Class for lost and found items
class Item(main.db.Model):
    id = main.db.Column(main.db.Integer, primary_key=True)
    name = main.db.Column(main.db.String(80))
    location_item = main.db.Column(main.db.String(100))
    description = main.db.Column(main.db.String(100))
    datee = main.db.Column(main.db.String(50))

    def __init__(self, name,loc, description,date):
        self.name = name
        self.location_item = loc
        self.description = description
        self.datee = date

#Schemas to help us when we make HTTP request
class ItemSchema(main.ma.Schema):
    class Meta:
        fields = ('id', 'name', 'location_item', 'description','datee')


class UserSchema(main.ma.Schema):
    class Meta:
        fields = ('username', 'name', 'password_hash', 'number')

