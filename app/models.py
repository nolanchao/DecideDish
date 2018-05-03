from flask import session
import sqlite3 as sql

# Creates group in groupnames table.
def insert_data(groupname, name, city, state):
    with sql.connect("app.db") as con:
    	cur = con.cursor()
    	cur.execute("insert into groupnames (groupnames, name, city, state) VALUES (?,?,?,?);", (groupname, name, city, state,))
    	con.commit()

# Finds location of group based on groupname.
def find_location(groupname):
     with sql.connect("app.db") as con:
        cur = con.cursor()
        group_city = cur.execute('SELECT city FROM groupnames WHERE GROUPNAMES=?',(groupname,)).fetchone()[0]
        group_state = cur.execute('SELECT state FROM groupnames WHERE GROUPNAMES=?',(groupname,)).fetchone()[0]
        print(group_city)
        con.commit()
        return group_city, group_state

# Inserts preferences into database.
def insert_preferences(groupname, name, cuisine, priceInput, radius, chinese, pizza, mexican, italian, ethiopian, sandwiches, steak, french, diners, burgers, barbecue, ramen):
    # SQL statement to insert into database goes here
    with sql.connect("app.db") as con:
        cur = con.cursor()
        cur.execute("insert into preferences (groupnames, name, cuisine, priceInput, radius, chinese, pizza, mexican, italian, ethiopian, sandwiches, steak, french, diners, burgers, barbecue, ramen) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (groupname, name, cuisine, priceInput, radius, chinese, pizza, mexican, italian, ethiopian, sandwiches, steak, french, diners, burgers, barbecue, ramen))
        con.commit()

# Counts people who have voted in group.
def vote_count(groupname):
    with sql.connect("app.db") as con:
        cur = con.cursor()
        vote_count = cur.execute("SELECT count(name) FROM (SELECT DISTINCT name, groupnames, cuisine FROM preferences WHERE groupnames = ?)", (groupname,)).fetchone()[0]
        con.commit()
    return vote_count

# Counts people who have accessed in group.
def group_user_count(groupname):
    with sql.connect("app.db") as con:
        cur = con.cursor()
        group_user_count = cur.execute('SELECT count(name) FROM groupnames WHERE groupnames = ?', (groupname,)).fetchone()[0]
        con.commit()
    return group_user_count

# Deletes duplicate votes.
def delete_vote(groupname,name):
    with sql.connect("app.db") as con:
        cur = con.cursor()
        vote_count =cur.execute("DELETE FROM preferences WHERE groupnames=? and name = ?", (groupname, name))
        con.commit()
        print ("success")

# This helps to determine what the group mutually wants.
def retrieve_prefs(group_cuisine, group_radius, group_price):
    with sql.connect("app.db") as con:
        con.row_factory = sql.Row
        cur = con.cursor()
        groupname = session['groupname']
        group_radius = cur.execute('SELECT min(radius) AS groupradius FROM preferences WHERE GROUPNAMES=?', (groupname,)).fetchone()[0]
        group_price = cur.execute('SELECT min(priceinput) AS groupprice FROM preferences WHERE GROUPNAMES=?', (groupname,)).fetchone()[0]
        group_cuisine = cur.execute('SELECT group_concat(cuisine, ",") FROM ( SELECT cuisine FROM ( SELECT "chinese" AS Cuisine, ( SELECT sum(chinese) FROM preferences WHERE groupnames = ? ) AS CuisinePoints UNION ALL SELECT "pizza" AS Cuisine, ( SELECT sum(pizza) FROM preferences WHERE groupnames = ? ) AS CuisinePoints UNION ALL SELECT "mexican" AS Cuisine, ( SELECT sum(mexican) FROM preferences WHERE groupnames = ? ) AS CuisinePoints UNION ALL SELECT "italian" AS Cuisine, ( SELECT sum(italian) FROM preferences WHERE groupnames = ? ) AS CuisinePoints UNION ALL SELECT "ethiopian" AS Cuisine, ( SELECT sum(ethiopian) FROM preferences WHERE groupnames = ? ) AS CuisinePoints UNION ALL SELECT "sandwiches" AS Cuisine, ( SELECT sum(sandwiches) FROM preferences WHERE groupnames = ? ) AS CuisinePoints UNION ALL SELECT "steak" AS Cuisine, ( SELECT sum(steak) FROM preferences WHERE groupnames = ? ) AS CuisinePoints UNION ALL SELECT "french" AS Cuisine, ( SELECT sum(french) FROM preferences WHERE groupnames = ? ) AS CuisinePoints UNION ALL SELECT "diners" AS Cuisine, ( SELECT sum(diners) FROM preferences WHERE groupnames = ? ) AS CuisinePoints UNION ALL SELECT "burgers" AS Cuisine, ( SELECT sum(burgers) FROM preferences WHERE groupnames = ? ) AS CuisinePoints UNION ALL SELECT "barbecue" AS Cuisine, ( SELECT sum(barbecue) FROM preferences WHERE groupnames = ? ) AS CuisinePoints UNION ALL SELECT "ramen" AS Cuisine, ( SELECT sum(ramen) FROM preferences WHERE groupnames = ? ) AS CuisinePoints ) WHERE CuisinePoints = ( SELECT max(sum(chinese), sum(pizza), sum(mexican), sum(italian), sum(ethiopian), sum(sandwiches), sum(steak), sum(french), sum(diners), sum(burgers), sum(barbecue), sum(ramen) ) AS MostPreferredCuisine FROM preferences WHERE groupnames = ? ) );', (groupname,groupname,groupname,groupname,groupname,groupname,groupname,groupname,groupname,groupname,groupname,groupname,groupname,)).fetchone()[0]
    return group_cuisine, group_radius, group_price



