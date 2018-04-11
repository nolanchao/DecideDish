import sqlite3 as sql

def insert_data(trip_name, destination, friend):
    # SQL statement to insert into database goes here
    with sql.connect("app.db") as con:
    	cur = con.cursor()
    	cur.execute("insert into trips (trip_name, destination, friend) VALUES (?, ? ,?)", (trip_name, destination, friend))
    	con.commit()

def insert_address(street_address, city, state, country, zip_code):
    # SQL statement to insert into database goes here
    with sql.connect("app.db") as con:
    	cur = con.cursor()
    	cur.execute("insert into address (street_address, city, state, country, zip_code) VALUES (?,?,?,?,?)", (street_address, city, state, country, zip_code))
    	con.commit()

def retrieve_trips(destination, friend):
    # SQL statement to query database goes here
    with sql.connect("app.db") as con:
    	con.row_factory = sql.Row
    	# above sets up connection to accept data in the form of row objects
    	cur = con.cursor()
    	result = cur.execute("select * from trips").fetchall()
    	print (result)
    return result
	
def retrieve_companions(destination, friend):
    # SQL statement to query database goes here
    with sql.connect("app.db") as con:
    	con.row_factory = sql.Row
    	# above sets up connection to accept data in the form of row objects
    	cur = con.cursor()
    	result = cur.execute("select * from trips WHERE FRIEND IS 'sdf' ").fetchall()
    	print (result)
    return result



def insert_orders(name_of_part, manufacturer_of_part, value):
    # SQL statement to insert into database goes here
    with sql.connect("app.db") as con:
    	cur = con.cursor()
    	cur.execute("insert into orders (name_of_part, manufacturer_of_part, customer_ordered) VALUES (?,?,?)", (name_of_part, manufacturer_of_part, value))
    	con.commit()

##You might have additional functions to access the database