import requests
from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse
import json
from pymongo import MongoClient
from bson.json_util import dumps, loads
from bson.objectid import ObjectId
import graphene

app = Flask(__name__)
api = Api(app)

class HomePage(Resource):
    def get(self):

        apis = []
        apis.append('http://127.0.0.1:5000/getProducts: The MongoDb database returns a collection of products within the database.')
        apis.append('http://127.0.0.1:5000/getTitles: Connects to the Mongodb database and returns all the titles of the products in the database.')
        apis.append('http://127.0.0.1:5000/insertProduct: Allows the end user to insert a product into the database through url arguments.')
        return apis

api.add_resource(HomePage, '/')


class GetProduct(Resource):
    def get(self):
        client = MongoClient("mongodb://root:example@localhost:27017/")
        db = client.products
        collection = db.products_data
        results = dumps(collection.find())
        return json.loads(results)


api.add_resource(GetProduct, '/getProducts')


class Product(graphene.ObjectType):
    id = graphene.ID()
    ProductId = graphene.Int()
    title = graphene.String()
    cost = graphene.Decimal()


class Query(graphene.ObjectType):
    product = graphene.Field(Product)
    all_products = graphene.List(Product)


    def resolve_product(root, info):
        client = MongoClient("mongodb://root:example@localhost:27017/")
        db = client.products
        collection = db.products_data

        products = []
        #results = json.loads(dumps(collection.find()))
        results = collection.find()
        json_content = json.loads(dumps(collection.find()))

        #extractedTitle = json_content[:'Name']

        #json_content = json.loads(data.text)

        for result in json_content:
            product = Product(title=result.get('Name'))
            products.append(product)

        #product = Product(title=results.get('Name'))
        #product = Product(title=extractedTitle)
        #Product.ProductId = results.find('ProductId')

        product = Product(title=json_content[0].get('Name'))
        #extractedTitle = json_content['Name']

        return products


class GetTitles(Resource):
    def get(self):
        schema = graphene.Schema(query=Query)
        query = """
                {
                    allProducts {
                        title
                    }
                 }
        """

        results = schema.execute(query)
        return {'results ': str(results)}


api.add_resource(GetTitles, '/getTitles')


class InsertProduct(Resource):
    def get(self):
        client = MongoClient("mongodb://root:example@localhost:27017/")
        db = client.products
        collection = db.products_data

        parser = reqparse.RequestParser()
        res = parser.add_argument('ProductId', type=int, location='args')
        res = parser.add_argument('Name', type=str, location='args')
        res = parser.add_argument('Price', type=float, location='args')

        args = parser.parse_args()

        ProductID = args['ProductId']
        Name = args['Name']
        Price = args['Price']

        if (ProductID is not None) and (Name is not None) and (Price is not None):
            newRecord = {"ProductId": ProductID, "Name": Name, "Price": Price}
            res = collection.insert_one(newRecord)

            return {'status': 'Inserted'}
        else:
            return {'status': 'failed'}


api.add_resource(InsertProduct, '/insertProduct')


if __name__ == '__main__':
    app.run(debug=True)
