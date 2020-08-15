from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from constant import \
    HTTP_STATUS_NOT_FOUND, \
    HTTP_STATUS_CONFLICT, \
    HTTP_STATUS_CREATED, \
    HTTP_STATUS_OK, \
    HTTP_STATUS_INTERNAL_SERVER_ERROR
import sqlite3
from models.item import ItemModel

items = []


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price', type=float, required=True, help='This filed can not be blank'
    )
    parser.add_argument(
        'store_id', type=int, required=True, help='store is required'
    )

    @jwt_required()
    def get(self, name):

        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), HTTP_STATUS_OK
        return {'message': 'item not found'}, HTTP_STATUS_NOT_FOUND

    @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': 'item with name {}  already exist!'.format(name)}, HTTP_STATUS_CONFLICT
        data = Item.parser.parse_args()

        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {'message': 'An error occurred when inserting the item'}, HTTP_STATUS_INTERNAL_SERVER_ERROR

        return item.json(), HTTP_STATUS_CREATED

    @jwt_required()
    def delete(self, name):

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'items deleted'}, HTTP_STATUS_OK
        else:
            return {'message': 'item not found'}, HTTP_STATUS_NOT_FOUND

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, **data)

        else:
            item.price = data['price']
            item.store_id = data['store_id']
        item.save_to_db()
        return item.json(), HTTP_STATUS_OK


class Items(Resource):
    @jwt_required()
    def get(self):

        return {'items': list(map(lambda x: x.json(), ItemModel.find_all()))}, HTTP_STATUS_OK
