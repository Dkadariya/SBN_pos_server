from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import json

app = Flask(__name__)
api=Api(app)

class HelloWorld(Resource):
    def get(self):
        return"Hello World"
# defination for Items
# Allowes to get item details based on id and add a new item to the DB
class Items(Resource):
    # POST defination
    def post(self):
        id = request.form['item_id']
        print (id)
        return jsonify({"id":101, "name":"apple", "total_count":20,"price":10})

    #PUT defination
    def put(self):
        param=request.form['details']
        print (json.loads(param))
        return "success"

# API resources routing
api.add_resource(HelloWorld, '/')
api.add_resource(Items, '/item')

if __name__ == '__main__':
    app.run(debug=True)