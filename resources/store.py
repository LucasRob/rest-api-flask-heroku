from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from sqlalchemy import exc
from models.store import StoreModel


class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help="This Field cannot be left blank!")

    @jwt_required
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 200
        return {'message': 'Store not found'}, 400

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': f"An store with name {name} already exists."}, 400

        data = Store.parser.parse_args()
        store = StoreModel(**data)

        try:
            store.save_to_db()
        except exc.SQLAlchemyError:
            return {"message": "An error occurred inserting the store."}, 500

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': 'Item deleted'}


class StoreList(Resource):
    def get(self):
        return {'stores': [x.json() for x in StoreModel.find_all()]}
