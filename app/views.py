# Importing flask library
from app import app, models, db
from .models import *
from flask import Flask, redirect, make_response, render_template, url_for, session, request, escape, flash, jsonify
import os
import pprint
import requests
import sys
import urllib
import random
import string

app.secret_key = os.environ.get('SECRET_KEY') or 'hard to guess string'


# As soon as someone goes onto the app site, they will be redirected to a URL with an
# appended group name

@app.route('/')
def onboard():
    if 'groupname' in session:
        groupname = session['groupname']
        return render_template('preferences.html')
    else:
        groupname = ''.join(random.sample(string.ascii_uppercase, 6))
        return redirect('/'+groupname, code=302)

# Each unique group then gets rerouted to the login page.
@app.route('/<groupname>')
def dynamicgroup(groupname):
    print(groupname)
    urlshare = ("where2eat.me/"+groupname)
    if group_user_count(groupname) > 0:
        group_city = find_location(groupname)[0]
        print(group_city)
        group_state =  find_location(groupname)[1]
        readonly = "readonly"
        already_input = "class=already_input"
        group_decision_required = ""
    else:
        group_city = ""
        group_state = ""
        readonly = ""
        already_input = ""
        group_decision_required = ", your dining city, and dining state "
    return render_template('login.html', groupname=groupname, urlshare=urlshare, group_city=group_city, group_state=group_state, readonly=readonly, already_input=already_input, group_decision_required=group_decision_required)


# User fills out name, city, state for where they want to eat.
@app.route('/login', methods = ['GET','POST'])
def login():
    session['groupname'] = str.capitalize(request.form['groupname'])
    session['name'] = request.form['name']
    if request.method == 'POST':
        session['groupname'] = request.form['groupname']
        session['city'] = request.form['city']
        session['state'] = request.form['state']
        groupname = str.capitalize(session['groupname'])
        city = session['city']
        state = session['state']

        render_template('personalpreferences.html')     
    return render_template('preferences.html', groupname=groupname, name=name, city=city, state=state, urlshare=urlshare, grouplocation=grouplocation)  


# User now fills out their cuisine, their spend preferences, and travel preferences.
@app.route('/preferences', methods = ['GET','POST'])
def preferences():
    if request.method == 'GET':
        groupname = session['groupname']
        name = session['name']
        city = session['city']
        state = session['state']
        delete_vote(groupname, name)   
        return render_template('preferences.html')
    if request.method == 'POST':
        session['groupname'] = request.form['groupname']
        session['name'] = request.form['name']
        session['city'] = request.form['city']
        session['state'] = request.form['state']

        groupname = session['groupname']
        name = session['name']
        city = session['city']
        state = session['state'] 
        urlshare = ("where2eat.me/"+groupname)
        insert_data(groupname, name, city, state)   
        delete_vote(groupname, name)   
        return render_template('preferences.html', groupname=groupname, urlshare=urlshare, city=city, state=state)  


# Once the user has put in their preferences, they get taken to a personal preferences page.
# This page basically confirms to the user what they had put.
@app.route('/personalpreferences', methods = ['GET','POST']) # You need to specify something here for the function to get requests
def personalpreferences():
    if request.method == 'POST':
        cuisine = str.lower(request.form['cuisine'])
        priceInput = request.form['priceInput']
        if request.form['priceInput'] is '4':
            priceInput = '1,2,3,4'
            priceInputSign = '$$$$'
        elif  request.form['priceInput'] is '3':
            priceInput = '1,2,3'
            priceInputSign = '$$$'
        elif  request.form['priceInput'] is '2':
            priceInput = '1,2'
            priceInputSign = '$$'
        elif  request.form['priceInput'] is '1':
            priceInput = '1'
            priceInputSign = '$'
        radius = round((float(request.form['rangeInput']) * 1609.34),0)
        rangeInputSign = request.form['rangeInput'] + ' mi'
        city = session['city']
        groupname = session['groupname']
        name = session['name']
        urlshare = ("where2eat.me/"+groupname)

        if "chinese" in cuisine:
            chinese = '1'
        else: chinese ='0'
        if "pizza" in cuisine:
            pizza = '1'
        else: pizza ='0'
        if "mexican" in cuisine:
            mexican = '1'
        else: mexican ='0'
        if "italian" in cuisine:
            italian = '1'
        else: italian ='0'
        if "ethiopian" in cuisine:
            ethiopian = '1'
        else: ethiopian ='0'
        if "sandwiches" in cuisine:
            sandwiches = '1'
        else: sandwiches ='0'
        if "steak" in cuisine:
            steak = '1'
        else: steak ='0'
        if "french" in cuisine:
            french = '1'
        else: french ='0'
        if "diners" in cuisine:
            diners = '1'
        else: diners ='0'
        if "burgers" in cuisine:
            burgers = '1'
        else: burgers ='0'
        if "barbecue" in cuisine:
            barbecue = '1'
        else: barbecue ='0'

        insert_preferences(groupname, name, cuisine, priceInput, radius, chinese, pizza, mexican, italian, ethiopian, sandwiches, steak, french, diners, burgers, barbecue)
        count = vote_count(groupname)
        if count == 1:
            count = "you're the only one that's voted so far"
        elif count == 2:
            count = "you and one of your friends have voted so far"
        else: count =  ("we have ") + str(count) + (" total votes in the group so far")
        print(count)
        return render_template('personalpreferences.html', priceInput=priceInput, radius=radius, priceInputSign=priceInputSign, rangeInputSign=rangeInputSign, cuisine=cuisine, urlshare=urlshare, count=count, groupname=groupname)
    # Here, you need to have logic like if there's a post request method, store the term and email from the form into
    # session dictionary
    if request.method == 'GET':
        return redirect(url_for('home'))


# This page shows the group's results
@app.route('/results', methods = ['GET','POST'])
def results():
    city = session['city']
    state = session['state']
    if request.method == 'POST':
        return render_template('page_not_found.html'), 404
    if request.method == 'GET':
        groupprefs = retrieve_prefs([0],[0],[0])
        # goes back into database, retrieves groups preferences and stores it for the API
        groupcuisine = (groupprefs[0])
        GroupRadius = (groupprefs[1])
        GroupPrice = (groupprefs[2])
        url = "https://api.yelp.com/v3/businesses/search"
        params = {
            'location': str(city+','+state),
            'categories': groupcuisine,
            'price': GroupPrice,
            'sort_by': 'rating',
            'radius' : GroupRadius
        }
        headers = {
            "Authorization": "Bearer APIKEYGOESHERE",
            "content-type": "application/json"
        }
        response = requests.get(url=url, params=params, headers=headers)
        data = response.json()
        groupname = session['groupname']
        name = session['name']
        cuisine = groupprefs[0]
        radius = GroupRadius
        radiusinmiles = str(round(0.000621371*GroupRadius,2))+str(" miles")
        milesoutout = str(radiusinmiles + " miles")
        rangeInputSign = GroupRadius
        searchresults = data['total']
        pprint.pprint (searchresults)
        if '4' in GroupPrice:
            priceInputSign = '$$$$'
        elif '3' in GroupPrice:
            priceInputSign = '$$$'
        elif '2' in GroupPrice:
            priceInputSign = '$$'
        else: priceInputSign = '$'
        pprint.pprint ("Yelp API is being called.")
        count = vote_count(groupname)


        allresults = {}


        if searchresults == 4:
            allresults = {}
            allresults['0name'] = str((data['businesses'][0]['name']))
            allresults['0image'] = str((data['businesses'][0]['image_url']))
            allresults['0rating'] = str((data['businesses'][0]['rating']))
            allresults['0price'] = str((data['businesses'][0]['price']))
            allresults['0link'] = str((data['businesses'][0]['url']))

            allresults['1name'] = str((data['businesses'][1]['name']))
            allresults['1image'] = str((data['businesses'][1]['image_url']))
            allresults['1rating'] = str((data['businesses'][1]['rating']))
            allresults['1price'] = str((data['businesses'][1]['price']))
            allresults['1link'] = str((data['businesses'][1]['url']))

            allresults['2name'] = str((data['businesses'][2]['name']))
            allresults['2image'] = str((data['businesses'][2]['image_url']))
            allresults['2rating'] = str((data['businesses'][2]['rating']))
            allresults['2price'] = str((data['businesses'][2]['price']))

            allresults['3name'] = str((data['businesses'][3]['name']))
            allresults['3image'] = str((data['businesses'][3]['image_url']))
            allresults['3rating'] = str((data['businesses'][3]['rating']))
            allresults['3price'] = str((data['businesses'][3]['price']))

            allresults['4name'] = "n/a"
            allresults['4image'] = "n/a"
            allresults['4rating'] = "n/a"
            allresults['4price'] = "n/a"

        elif searchresults == 3:
            allresults = {}
            allresults['0name'] = str((data['businesses'][0]['name']))
            allresults['0image'] = str((data['businesses'][0]['image_url']))
            allresults['0rating'] = str((data['businesses'][0]['rating']))
            allresults['0price'] = str((data['businesses'][0]['price']))
            allresults['0link'] = str((data['businesses'][0]['url']))

            allresults['1name'] = str((data['businesses'][1]['name']))
            allresults['1image'] = str((data['businesses'][1]['image_url']))
            allresults['1rating'] = str((data['businesses'][1]['rating']))
            allresults['1price'] = str((data['businesses'][1]['price']))
            allresults['1link'] = str((data['businesses'][1]['url']))

            allresults['2name'] = str((data['businesses'][2]['name']))
            allresults['2image'] = str((data['businesses'][2]['image_url']))
            allresults['2rating'] = str((data['businesses'][2]['rating']))
            allresults['2price'] = str((data['businesses'][2]['price']))
            allresults['2link'] = str((data['businesses'][2]['url']))

            allresults['3name'] = "n/a"
            allresults['3image'] = "n/a"
            allresults['3rating'] = "n/a"
            allresults['3price'] = "n/a"

            allresults['4name'] = "n/a"
            allresults['4image'] = "n/a"
            allresults['4rating'] = "n/a"
            allresults['4price'] = "n/a"
        elif searchresults == 2:
            allresults = {}
            allresults['0name'] = str((data['businesses'][0]['name']))
            allresults['0image'] = str((data['businesses'][0]['image_url']))
            allresults['0rating'] = str((data['businesses'][0]['rating']))
            allresults['0price'] = str((data['businesses'][0]['price']))
            allresults['0link'] = str((data['businesses'][0]['url']))
            
            allresults['1name'] = str((data['businesses'][1]['name']))
            allresults['1image'] = str((data['businesses'][1]['image_url']))
            allresults['1rating'] = str((data['businesses'][1]['rating']))
            allresults['1price'] = str((data['businesses'][1]['price']))
            allresults['1link'] = str((data['businesses'][1]['url']))

            allresults['2name'] = "n/a"
            allresults['2image'] = "n/a"
            allresults['2rating'] = "n/a"
            allresults['2price'] = "n/a"

            allresults['3name'] = "n/a"
            allresults['3image'] = "n/a"
            allresults['3rating'] = "n/a"
            allresults['3price'] = "n/a"

            allresults['4name'] = "n/a"
            allresults['4image'] = "n/a"
            allresults['4rating'] = "n/a"
            allresults['4price'] = "n/a"

        elif searchresults == 1:
            allresults = {}
            allresults['0name'] = str((data['businesses'][0]['name']))
            allresults['0image'] = str((data['businesses'][0]['image_url']))
            allresults['0rating'] = str((data['businesses'][0]['rating']))
            allresults['0price'] = str((data['businesses'][0]['price']))

            allresults['1name'] = "n/a"
            allresults['1image'] = "n/a"
            allresults['1rating'] = "n/a"
            allresults['1price'] = "n/a"

            allresults['2name'] = "n/a"
            allresults['2image'] = "n/a"
            allresults['2rating'] = "n/a"
            allresults['2price'] = "n/a"

            allresults['3name'] = "n/a"
            allresults['3image'] = "n/a"
            allresults['3rating'] = "n/a"
            allresults['3price'] = "n/a"

            allresults['4name'] = "n/a"
            allresults['4image'] = "n/a"
            allresults['4rating'] = "n/a"
            allresults['4price'] = "n/a"

        elif searchresults == 0:
            allresults = "sad"
        else:
            allresults = {}
            allresults['0name'] = str((data['businesses'][0]['name']))
            allresults['0image'] = str((data['businesses'][0]['image_url']))
            allresults['0rating'] = str((data['businesses'][0]['rating']))
            allresults['0price'] = str((data['businesses'][0]['price']))
            allresults['0link'] = str((data['businesses'][0]['url']))

            allresults['1name'] = str((data['businesses'][1]['name']))
            allresults['1image'] = str((data['businesses'][1]['image_url']))
            allresults['1rating'] = str((data['businesses'][1]['rating']))
            allresults['1price'] = str((data['businesses'][1]['price']))
            allresults['1link'] = str((data['businesses'][1]['url']))

            allresults['2name'] = str((data['businesses'][2]['name']))
            allresults['2image'] = str((data['businesses'][2]['image_url']))
            allresults['2rating'] = str((data['businesses'][2]['rating']))
            allresults['2price'] = str((data['businesses'][2]['price']))
            allresults['2link'] = str((data['businesses'][2]['url']))

            allresults['3name'] = str((data['businesses'][3]['name']))
            allresults['3image'] = str((data['businesses'][3]['image_url']))
            allresults['3rating'] = str((data['businesses'][3]['rating']))
            allresults['3price'] = str((data['businesses'][3]['price']))
            allresults['3link'] = str((data['businesses'][3]['url']))

            allresults['4name'] = str((data['businesses'][4]['name']))
            allresults['4image'] = str((data['businesses'][4]['image_url']))
            allresults['4rating'] = str((data['businesses'][4]['rating']))
            allresults['4price'] = str((data['businesses'][4]['price']))
            allresults['4link'] = str((data['businesses'][4]['url']))
        return render_template('results.html',data=data, searchresults=searchresults, allresults=allresults, radius=radius, priceInputSign=priceInputSign, rangeInputSign=rangeInputSign, cuisine=cuisine, radiusinmiles=radiusinmiles, count=count)

@app.route('/restart')
def restart():
    session.pop('groupname', None)
    name = ''.join(random.sample(string.ascii_uppercase, 6))
    pprint.pprint(name)
    return redirect('/'+name, code=302)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404