from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    # here we create the get, post and delete endpoints...we do not create the put endpoints bcz it upadate the data which create the error.. so we cannot allow to editing of stores.
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404
        
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': "A store with name '{}' already exists.".format(name)}, 400
        
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': 'An error occured while creating the store.'}, 500
        return store.json()
    
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.deleto_from_db()
        return {'message': 'Store deleted'}
    
    
class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]} # Here two way to return the list ...1st is [store.json() for store in StoreModel.query.all()].. 2nd is using list and lambda fun. 
    