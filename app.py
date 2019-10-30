from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_cors import CORS

# importing methods from SQL handler module for CRUD operations
from sql_handler import get_item, insert_item, remove_item, sell_item, list_items
import json

app = Flask(__name__)
CORS(app)
api=Api(app)

class HelloWorld(Resource):
    def get(self):
        return"Hello World"
# defination for Items
# allowes to get item details based on id and add a new item to the DB
class Items(Resource):
    # POST method
    def post(self):
        id = request.form['item_id']
        # calling get_item method from database handler module
        item_detail = get_item(id)
        # checking database response for given ID and generating response
        if item_detail!=[]:
            resp={
                "id":item_detail[0],
                "name":item_detail[1],
                "category":item_detail[2],
                "total_count":item_detail[3],
                "price":item_detail[4],
                "date_created":item_detail[5]
                }
        else:
            resp={"Error":"No matching record for given ID"}
        return jsonify(resp)

    # PUT method
    def put(self):
        # extract item details from request body form
        param=request.form['details']
	print (param)
        # insert item details into the database
        commit = insert_item(json.loads(param))
        # return status keyword and description
        return jsonify({"status":commit[0],"desc":commit[1]})
    
    # DELETE by ID
    def delete(self):
        # get item id from request form
        id=request.form['item_id']
        # pass id to handler method to remove record
        commit = remove_item (id)
        # return commit status
        return jsonify({"status":commit[0],"desc":commit[1]})

class Sell(Resource):
    def post(self):
        # get ID and quantity of item sold from request parameter
        id=request.form['item_id']
        quant = int (request.form['quantity'])
        # update the item in database through handler
        resp = sell_item (id,quant)
        # return handler response
        return jsonify(resp)

class get_all(Resource):
    def get(self):
        # get all records from the inventory table in database
        resp = list_items()
        # return item list
        return jsonify(resp)

# API resources routing
api.add_resource(HelloWorld, '/')
api.add_resource(Items, '/item')
api.add_resource(Sell, '/item_sell')
api.add_resource(get_all, '/get_items')
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
