# import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import  jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item needs a store id."
    )
    
    @jwt_required()
    def get(self, name): 
        # for item in items:
        #     if item['name'] == name:
        #         return item
        # item = next(filter(lambda x: x['name'] == name, items), None)
        # return {'item': item}, 200 if item else 404
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404
    

    def post(self, name):
        
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists,".format(name)}, 400
        
        data = Item.parser.parse_args()
        # data = request.get_json()
        item = ItemModel(name, **data)  #  **data = data['price'], data['store_id']
        
        try:
            item.save_to_db()
            
        except:
            return {'message': "An error occurred inserting the item."}, 500 # internal server error
        
        return item.json(), 201
    
    
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            
        return {'message': 'Item deleted'}
    
    # put method is used to create the new item as well as update the already exising item.
    def put(self, name):
       
        data = Item.parser.parse_args()
        # print(data['another'])  this give the error bcz data does not have key that is another.
        # item = next(filter(lambda x: x['name'] == name, items), None)
        item = ItemModel.find_by_name(name)
        
        if item is None:
            item = ItemModel(name, **data)
                
        else:
            item.price = data['price']
            
        item.save_to_db()
           
        return item.json()
    
    
class ItemList(Resource):
    def get(self):
        return {'items': [x.json() for x in ItemModel.query.all()]}
        # return {'items':list(map(lambda x: x.json(), ItemModel.query.all()))}   #list comprehenssion