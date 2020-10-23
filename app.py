from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security from authenticate, identity

app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app, authenticate, identity)

items = []

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', 
    type=float,
    required=True,
    help="This field cannot be blank"
    )
    @jwt_required()
    def get(self, name):
        for item in items:
            if item['name'] == name:
                return item, 200
        return {'item':None}, 404

    def post(self, name):
        data = request.get_json()
        item = {'name':name, 'price':data['price']}
        items.append(item)
        return item, 201

    @jwt_required()
    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message':'Item Deleted'}
    
    def put(self, name):
        data = Item.parser.parse_args()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name':name, 'price':data['price']}
            items.append(item)
        else:
            item.update(data)
        return item



class ItemList(Resourse):
    def get(self):
        return {'items':items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)
