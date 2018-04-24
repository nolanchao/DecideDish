from flask import session
import sqlite3 as sql

def insert_data(groupname, name, city, state):
    # SQL statement to insert into database goes here
    with sql.connect("app.db") as con:
    	cur = con.cursor()
    	cur.execute("insert into groupnames (groupnames, name, city, state) VALUES (?,?,?,?);", (groupname, name, city, state,))
    	con.commit()

def find_location(groupname):
     with sql.connect("app.db") as con:
        cur = con.cursor()
        group_city = cur.execute('SELECT city FROM groupnames where GROUPNAMES=?',(groupname,)).fetchone()[0]
        group_state = cur.execute('SELECT state FROM groupnames where GROUPNAMES=?',(groupname,)).fetchone()[0]
        print(group_city)
        con.commit()
        return group_city, group_state

def insert_preferences(groupname, name, cuisine, priceInput, radius, chinese, pizza, mexican, italian, ethiopian, sandwiches, steak, french, diners, burgers, barbecue):
    # SQL statement to insert into database goes here
    with sql.connect("app.db") as con:
        cur = con.cursor()
        cur.execute("insert into preferences (groupnames, name, cuisine, priceInput, radius, chinese, pizza, mexican, italian, ethiopian, sandwiches, steak, french, diners, burgers, barbecue) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (groupname, name, cuisine, priceInput, radius, chinese, pizza, mexican, italian, ethiopian, sandwiches, steak, french, diners, burgers, barbecue))
        con.commit()

def vote_count(groupname):
    with sql.connect("app.db") as con:
        cur = con.cursor()
        vote_count = cur.execute("select count(name) from (select DISTINCT name, groupnames, cuisine from preferences where groupnames = ?)", (groupname,)).fetchone()[0]
        con.commit()
    return vote_count

def group_user_count(groupname):
    with sql.connect("app.db") as con:
        cur = con.cursor()
        group_user_count = cur.execute('select count(name) from groupnames where groupnames = ?', (groupname,)).fetchone()[0]
        con.commit()
    return group_user_count

def delete_vote(groupname,name):
    with sql.connect("app.db") as con:
        cur = con.cursor()
        vote_count =cur.execute("delete from preferences where groupnames=? and name = ?", (groupname, name))
        con.commit()
        print ("success")


# This helps to determine what the group mutually wants.
def retrieve_prefs(groupcuisine, groupradius, groupprice):
    # SQL statement to query database goes here
    with sql.connect("app.db") as con:
        con.row_factory = sql.Row
        # above sets up connection to accept data in the form of row objects
        cur = con.cursor()
        groupname = session['groupname']
        groupradius = cur.execute('select min(radius) as groupradius from preferences where GROUPNAMES=?', (groupname,)).fetchone()[0]
        groupprice = cur.execute('select min(priceinput) as groupprice from preferences where GROUPNAMES=?', (groupname,)).fetchone()[0]
        groupcuisine = cur.execute('SELECT group_concat(cuisine, ",") FROM (SELECT cuisine FROM ( SELECT "chinese" AS Cuisine, ( SELECT sum(chinese) FROM preferences WHERE groupnames=? ) AS CuisinePoints UNION ALL SELECT "pizza" AS Cuisine, ( SELECT sum(pizza) FROM preferences WHERE groupnames=? ) AS CuisinePoints UNION ALL SELECT "mexican" AS Cuisine, ( SELECT sum(mexican) FROM preferences WHERE groupnames=? ) AS CuisinePoints UNION ALL SELECT "italian" AS Cuisine, ( SELECT sum(italian) FROM preferences WHERE groupnames=? ) AS CuisinePoints UNION ALL SELECT "ethiopian" AS Cuisine, ( SELECT sum(ethiopian) FROM preferences WHERE groupnames=? ) AS CuisinePoints UNION ALL SELECT "sandwiches" AS Cuisine, ( SELECT sum(sandwiches) FROM preferences WHERE groupnames=? ) AS CuisinePoints UNION ALL SELECT "steak" AS Cuisine, ( SELECT sum(steak) FROM preferences WHERE groupnames=? ) AS CuisinePoints UNION ALL SELECT "french" AS Cuisine, ( SELECT sum(french) FROM preferences WHERE groupnames=? ) AS CuisinePoints UNION ALL SELECT "diners" AS Cuisine, ( SELECT sum(diners) FROM preferences WHERE groupnames=? ) AS CuisinePoints UNION ALL SELECT "burgers" AS Cuisine, ( SELECT sum(burgers) FROM preferences WHERE groupnames=? ) AS CuisinePoints UNION ALL SELECT "barbecue" AS Cuisine, ( SELECT sum(barbecue) FROM preferences WHERE groupnames=? ) AS CuisinePoints ) WHERE CuisinePoints = ( SELECT max(sum(chinese), sum(pizza), sum(mexican), sum(italian), sum(ethiopian), sum(sandwiches), sum(steak), sum(french), sum(diners), sum(burgers), sum(barbecue) ) AS MostPreferredCuisine FROM preferences WHERE groupnames=? ));', (groupname,groupname,groupname,groupname,groupname,groupname,groupname,groupname,groupname,groupname,groupname,groupname,)).fetchone()[0]
        print (groupcuisine)
        print (groupradius)
        print (groupprice)
    return groupcuisine, groupradius, groupprice



# def retrieve_companions(destination, friend):
#     # SQL statement to query database goes here
#     with sql.connect("app.db") as con:
#     	con.row_factory = sql.Row
#     	# above sets up connection to accept data in the form of row objects
#     	cur = con.cursor()
#     	result = cur.execute("select * from trips WHERE FRIEND IS 'sdf' ").fetchall()
#     	print (result)
#     return result

