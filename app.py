from flask import Flask, jsonify, request
from flask_restful import Resource, Api
# importing methods from SQL handler module for CRUD operations
from sql_handler import get_item, insert_item, remove_item, sell_item
import json

app = Flask(__name__)
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
                "total_count":item_detail[2],
                "price":item_detail[3],
                "date_created":item_detail[4]
                }
        else:
            resp={"Error":"No matching record for given ID"}
        return jsonify(resp)

    # PUT method
    def put(self):
        # extract item details from request body form
        param=request.form['details']
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

# API resources routing
api.add_resource(HelloWorld, '/')
api.add_resource(Items, '/item')

if __name__ == '__main__':
    app.run(debug=True)