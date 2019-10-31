import mysql.connector
from config import CONFIG
from datetime import date, datetime, timedelta

# database configuration dictionary for connection
DB_CONFIG = {
  'user': CONFIG['user'],
  'password': CONFIG['password'],
  'host': '127.0.0.1',
  'database': 'SBN_pos',
  'raise_on_warnings': True
}

# establishing the database connection
try:
    connection = mysql.connector.connect(**DB_CONFIG)
    crsr=connection.cursor()

# raise an exction if connecion couldn't be established
except mysql.connector.Error as e:
    print ("DB connection Error: "+str(e))

def list_items():
    resp=[]
    query = ("SELECT * FROM item_inventory")
    crsr.execute(query)
    result=crsr.fetchall()
    if result!=[]:
        for r in result:
            resp.append({
                    "id":r[0],
                    "name":r[1],
                    "category":r[2],
                    "total_count":r[3],
                    "price":r[4],
                    "date_created":r[5]
                    })
    return resp

# get item detail by id
def get_item(id):
    # SQL select query to get the item details 
    get_qry= ("SELECT * FROM item_inventory WHERE Item_ID = %s")
    crsr.execute(get_qry,(id,))
    result=crsr.fetchall()
    # if query result is not None, return result
    if result!=[]:
        return result[0]
    else:
        return []

# function definition to insert item
def insert_item(item_detail):
    # SQL query to insert new item detail in to the database
    insert_qry = ("INSERT INTO item_inventory "
                "(Item_ID, item_name, category, total_count, price, created) "
                "VALUES (%s, %s, %s, %s, %s,%s)")
    # executing and commiting the query the database
    
    try:
	crsr.execute(insert_qry, (item_detail["id"], item_detail["name"],item_detail["category"],item_detail["total_count"], item_detail["price"], datetime.strptime(item_detail["created"], '%m-%d-%Y %H:%M')))
        connection.commit()
        return ("Success","write successful")
    except mysql.connector.Error as e:
        return ("Error",str(e))

# function definition to update the item inventory
def sell_item(sold_items):
    # iterate through each sold item an update its entry in the database
    for item in sold_items:
        current_count=0
        update_count=0
        # getting the current inventory size of the item.
        count_qry = ("SELECT total_count FROM item_inventory WHERE Item_ID = %s")
        crsr.execute(count_qry,(item['id'],))
        for (c,) in crsr:
            current_count=c

        # Calculating updated count while preventing inventory from going to negative value
        if current_count !=0 and (current_count-item['quantity'])>0:
            update_count=current_count-item['quantity']
        
        # updating the record with new count value
        update_qry = ("UPDATE item_inventory SET total_count = %s WHERE Item_ID = %s")
        try:
            crsr.execute(update_qry,(update_count,item['id']))
            connection.commit()
        except mysql.connector.Error as e:
            print (e)
        
        if update_count==0:
            delete_qry= ("DELETE FROM item_inventory WHERE Item_ID = %s")
            crsr.execute(del_qry,(id,))
            connection.commit()
    return {"status":"Success"}
    # print ("current count: {}".format(current_count))
    # print ("updated count: {}".format(update_count))
    
# funtion definition to delete an item record from the database
def remove_item(id):
    # delete query
    del_qry=("DELETE FROM item_inventory WHERE Item_ID = %s")
    #executing and commiting to database
    try:
        crsr.execute(del_qry,(id,))
        connection.commit()
        return ("Success","remove item successful")
    except mysql.connector.Error as e:
        return ("Error",str(e))


# sell(1,5)
# sell()
# print (insert_item(4,"carrot","25",1,date(2019,9,28)))
# delete_item(2)
# print (get_item (101))
# print (list_items())
# crsr.close()
