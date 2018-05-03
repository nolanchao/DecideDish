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

API_KEY = "PUT THE API KEY HERE"

@app.route('/')
def onboard():
    # As soon as someone goes onto the app site, they either be redirected to eithe the preferences page or
    # to a URL with an appended, randomized group name
    if 'groupname' in session:
        groupname = session['groupname']
        return render_template('preferences.html')
    else:
        groupname = ''.join(random.sample(string.ascii_uppercase, 6))
        return redirect('/'+groupname, code=302)

@app.route('/<groupname>')
def dynamicgroup(groupname):
    # Once the randomized group name is generated, it takes them to the onboarding page, where the initial user specifies name and
    # dining location for the group.
    # urlshare is the URL access link for other users to copy and paste.
    urlshare = ("where2eat.me/"+groupname)
    # The below code autogenerates the group_city and group_state based on if an initial user has set one up yet (hence if group_user_count > 0).
    # It also changes the form parameters to read-only so that people in the group are using the location.
    if group_user_count(groupname) > 0:
        group_city = find_location(groupname)[0]
        group_state =  find_location(groupname)[1]
        readonly = "readonly"
        already_input = "class=already_input"
        group_decision_required = ""
        # These below conditionals are just to indicate how many other people are using Where2Eat. Helps to identify if more people
        # are voting than are in the group and if the group needs more people to vote.
        if group_user_count(groupname) == 1:
            group_count_status = str(group_user_count(groupname)) + " person in your group has already accessed Where2Eat. " 
        else: 
            group_count_status = str(group_user_count(groupname)) + " people in your group have already accessed Where2Eat. " 
        if vote_count(groupname) == 0:
            hidden = "hidden"
            group_voting_status = "No one in the group has voted yet."
        elif vote_count(groupname) == 1:
            hidden = ""
            group_voting_status = str(vote_count(groupname)) + " vote is in!"
        else: 
            hidden = ""
            group_voting_status = str(vote_count(groupname)) + " votes are in!"
    # The else condition is set up only for the initial user for the group so that they can specify city and state. It also hides
    # the dynamic messaging about how many users and votes there are.
    else:
        group_city = ""
        group_state = ""
        readonly = ""
        already_input = ""
        group_count_status = ""
        group_decision_required = ", your dining city, and dining state "
        group_voting_status = ""
        hidden = "hidden"
    return render_template('login.html', groupname=groupname, urlshare=urlshare, group_city=group_city, group_state=group_state, readonly=readonly, already_input=already_input, group_decision_required=group_decision_required, group_voting_status=group_voting_status, group_count_status=group_count_status, hidden=hidden)


@app.route('/preferences', methods = ['GET','POST'])
def preferences():
    
    # User now fills out their cuisine, their spend preferences, and travel preferences.
    if request.method == 'GET':
        # This is if someone clicks "Go back" on the personal preferences page because of a data entry error.
        groupname = session['groupname']
        name = session['name']
        city = session['city']
        state = session['state']
        # We delete the previous vote to avoid duplicate votes from the same user.
        delete_vote(groupname, name)   
        return render_template('preferences.html', groupname=groupname)
    
    if request.method == 'POST':
        session['groupname'] = request.form['groupname']
        session['name'] = request.form['name']
        session['city'] = request.form['city']
        session['state'] = request.form['state']
        groupname = session['groupname']
        # This is just for the SQL query to input the groupname into the groupnames table.
        name = session['name']
        city = session['city']
        state = session['state'] 
        insert_data(groupname, name, city, state)   
        delete_vote(groupname, name)   
        return render_template('preferences.html', groupname=groupname, city=city, state=state)  

@app.route('/personalpreferences', methods = ['GET','POST'])
def personalpreferences():
    # Once the user has put in their preferences, they get taken to a personal preferences page.
    # This page basically confirms to the user what they had entered in.
    if request.method == 'POST':
        cuisine = request.form['cuisine']
        priceInput = request.form['priceInput']
        city = session['city']
        groupname = session['groupname']
        name = session['name']

        # Yelp's API is based on meters. The front end is in miles so we change the radius to meters for hte backend..
        rangeInputSign = request.form['rangeInput'] + ' mi'
        radius = round((float(request.form['rangeInput']) * 1609.34),0)

        # Yelp's API does price input as a range from 1-4; this changes it to $ and $$$$ to make it more intelligible for the user.
        # priceInput is fed into the back end, priceInputSign to the front end.
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

        # Gives scores to each cuisine type.
        if "Chinese" in cuisine:
            chinese = '1'
        else: chinese ='0'
        if "Pizza" in cuisine:
            pizza = '1'
        else: pizza ='0'
        if "Mexican" in cuisine:
            mexican = '1'
        else: mexican ='0'
        if "Italian" in cuisine:
            italian = '1'
        else: italian ='0'
        if "Ethiopian" in cuisine:
            ethiopian = '1'
        else: ethiopian ='0'
        if "Sandwiches" in cuisine:
            sandwiches = '1'
        else: sandwiches ='0'
        if "Steak" in cuisine:
            steak = '1'
        else: steak ='0'
        if "French" in cuisine:
            french = '1'
        else: french ='0'
        if "Diners" in cuisine:
            diners = '1'
        else: diners ='0'
        if "Burgers" in cuisine:
            burgers = '1'
        else: burgers ='0'
        if "Barbecue" in cuisine:
            barbecue = '1'
        else: barbecue ='0'
        if "Ramen" in cuisine:
            ramen = '1'
        else: ramen ='0'
        # Inserts scores for each cusine type into SQLite3.
        insert_preferences(groupname, name, cuisine, priceInput, radius, chinese, pizza, mexican, italian, ethiopian, sandwiches, steak, french, diners, burgers, barbecue, ramen)
        
        # Establishes vote count so that we can send voe statuses.
        count = vote_count(groupname)
        if count == 1:
            count = "you're the only one that's voted so far. Click here to see where we'd pick for a party of 1."
        elif count == 2:
            count = "you and one of your friends have voted so far. Click here for the group results!"
        else: count = ("we have ") + str(count) + (" total votes in the group so far. Click here for the group results!")
        return render_template('personalpreferences.html', priceInput=priceInput, radius=radius, priceInputSign=priceInputSign, rangeInputSign=rangeInputSign, cuisine=cuisine, count=count, groupname=groupname)
    
    # Here, you need to have logic like if there's a post request method, store the term and email from the form into
    # session dictionary
    if request.method == 'GET':
        return redirect(url_for('home'))

# This page shows the group's results
@app.route('/results', methods = ['GET','POST'])
def results():
    # Here we go. Time to find out what the group wants!
    # These next three lines make it simpified for the API call.
    groupname = session['groupname']
    city = session['city']
    state = session['state']

    if request.method == 'POST':
        return render_template('page_not_found.html'), 404
    if request.method == 'GET':
        
        # group_prefs goes back into database, retrieves groups preferences, renders the mutual preferences, and stores it for the API
        group_prefs = retrieve_prefs([0],[0],[0])
        group_cuisine = (group_prefs[0])
        group_radius = (group_prefs[1])
        group_price = (group_prefs[2])
        pprint.pprint(group_cuisine)
        
        # This is now the API call to Yelp.
        url = "https://api.yelp.com/v3/businesses/search"
        params = {
            'location': str(city+','+state),
            'categories': group_cuisine,
            'price': group_price,
            'sort_by': 'rating',
            'radius' : group_radius
        }
        headers = {
            "Authorization": str("Bearer "+ str(API_KEY)),
            "content-type": "application/json"
        }
        response = requests.get(url=url, params=params, headers=headers)
        data = response.json()
        pprint.pprint ("Yelp API is being called.")

        # Changes group_radius back to miles for the  front end.
        radius_in_miles = str(round(0.000621371*group_radius,2))+str(" miles")

        # Changes group_price back to $ signs for the front end.
        if '4' in group_price:
            priceInputSign = '$$$$'
        elif '3' in group_price:
            priceInputSign = '$$$'
        elif '2' in group_price:
            priceInputSign = '$$'
        else: priceInputSign = '$'

        # Shows number of votes. Conditional for grammar.
        if vote_count(groupname)==1:
            count = str(vote_count(groupname)) + ( " vote")
        else: count = str(vote_count(groupname)) + ( " votes")

        # Counts the number of results.
        searchresults = data['total']

        # Funny message if no results found.
        if searchresults > 0:
            zero = ""
        else:
            zero = "🙁 You all are a picky bunch. Maybe it's time to get some new friends."

        # Establishes a list to render for the API results
        list_of_restaurants = []
        business_names = []
        image_url = []
        rating = []
        price = []
        url = []

        # Conditionals to list index errors and also information overload.
        if 0 < searchresults < 5:
            max = searchresults
        elif searchresults > 5:
            max = 5
        else: max = 0

        # Dictionary time.
        for i in range(0, max):
            business_names = data['businesses'][i]['name']
            image_url = data['businesses'][i]['image_url']             
            rating = data['businesses'][i]['rating']
            price = data['businesses'][i]['price']
            url = data['businesses'][i]['url']
            i = int(i) 
            restaurant_result = dict(names=business_names, image_url=image_url, rating=rating, price=price, url=url)
            list_of_restaurants.append(restaurant_result)

        return render_template('results.html',data=data, searchresults=searchresults, priceInputSign=priceInputSign, group_cuisine=group_cuisine, radius_in_miles=radius_in_miles, count=count, zero=zero, business_names=business_names, image_url=image_url, url=url, rating=rating, price=price, list_of_restaurants=list_of_restaurants)

@app.route('/restart')
def restart():
    # Lets the user logout and start all over again.
    session.pop('groupname', None)
    groupname = ''.join(random.sample(string.ascii_uppercase, 6))
    return redirect('/'+groupname, code=302)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

@app.route('/<groupname>/results')
def return_visit(groupname):
    # If the user accesses Where2Eat via the group URL, they can click see the group's results from the login page without having to
    # do the whole process again.
    session['groupname'] = groupname
    session['city'] = find_location(groupname)[0]
    session['state'] =  find_location(groupname)[1]
    return redirect('/results', code=302)
    