from flask import Flask
from flask_restful import Api 
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  #this is only changing trhe extension behaviour not changing the uderling sql behavior.
app.secret_key = 'jose'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

# this create the new endpoit that is /auth
jwt = JWT(app, authenticate, identity)  

    
api.add_resource(Item, '/item/<string:name>') 
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')

api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from dbms import db   # import here bcz of circular import
    db.init_app(app)
    app.run(port=5000, debug=True)