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

# function defination to insert item
def insert_item(id, name, count, price, created):
    # SQL query to insert new item detail in to the database
    insert_item = ("INSERT INTO item_inventory "
                "(Item_ID, item_name, total_count, price, created) "
                "VALUES (%s, %s, %s, %s, %s)")
    # executing and commiting the query the database
    crsr.execute(insert_item, (id, name, count, price, created))
    connection.commit()

# function defination to update the item inventory
def sell_item(id,count):
    current_count=0
    update_count=0
    # getting the current inventory size of the item.
    count_qry = ("SELECT total_count FROM item_inventory WHERE Item_ID = %s")
    crsr.execute(count_qry,(id,))
    for (c,) in crsr:
        current_count=c

    # Calculating updated count while preventing inventory from going to negative value
    if current_count !=0 and (current_count-count)>0:
        update_count=current_count-count
    
    # updating the record with new count value
    update_qry = ("UPDATE item_inventory SET total_count = %s WHERE Item_ID = %s")
    crsr.execute(update_qry,(update_count,id))
    connection.commit()
    # return the updated item count
    return (update_count)
    # print ("current count: {}".format(current_count))
    # print ("updated count: {}".format(update_count))
    
# funtion defination to delete an item record from the database
def delete_item(id):
    # delete query
    del_qry=("DELETE FROM item_inventory WHERE Item_ID = %s")
    #executing and commiting to database
    crsr.execute(del_qry,(id,))
    connection.commit()

# sell(1,5)
# sell()
# insert_item(3,"carrot",25,1,date(2019,9,28))
delete_item(2)
crsr.close()