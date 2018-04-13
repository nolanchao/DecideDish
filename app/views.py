# Importing flask library
from app import app
from flask import Flask, redirect, make_response, render_template, url_for, session, request, escape, flash, jsonify
import os
import pprint
import requests
import sys
import urllib

app.secret_key = os.environ.get('SECRET_KEY') or 'hard to guess string'



@app.route('/')
def onboard():
    if 'username' in session:
        username = session['username']
        render_template('preferences.html')
    return render_template('login.html')

@app.route('/login', methods = ['GET','POST'])
def login():
    session['username'] = request.form['username']
    if request.method == 'POST':
        session['username'] = request.form['username']
        username = session['username']
        print (username)
        render_template('results.html')      
    return render_template('preferences.html', username=username)  

@app.route('/preferences', methods = ['GET','POST'])
def preferences():
    session['username'] = request.form['username']
    if request.method == 'POST':
        session['username'] = request.form['username']
        username = session['username']
        print (username)
        render_template('preferences.html')      
    return render_template('preferences.html', username=username)  

@app.route('/results', methods = ['GET','POST']) # You need to specify something here for the function to get requests
def results():
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
            priceInput = '1,2',
            priceInputSign = '$$'
        elif  request.form['priceInput'] is '1':
            priceInput = '1',
            priceInputSign = '$'
        radius = request.form['rangeInput']
        if int(request.form['rangeInput']) <= 804:
            rangeInputSign = '.5mi'
        elif  int(request.form['rangeInput']) <= 1608:
            rangeInputSign = '1mi'
        elif  int(request.form['rangeInput']) <= 3216:
            rangeInputSign = '2.5mi'
        elif  int(request.form['rangeInput']) <= 8040:
            rangeInputSign = '5mi'
        else: rangeInputSign = '10mi'
        url = "https://api.yelp.com/v3/businesses/search"
        params = {
            'location': '94704',
            'categories' : cuisine,
            'price': priceInput,
            'sort_by': 'rating',
            'radius' : radius
        }
        headers = {
            "Authorization": "Bearer API KEY",
            "content-type": "application/json"
        }
        response = requests.get(url=url, params=params, headers=headers)
        data = response.json()
        pprint.pprint ("Yelp API is being called.")
        searchresults = (data['total'])
        allresults = {}
        allresults['1name'] = str((data['businesses'][1]['name']))
        allresults['2name'] = str((data['businesses'][2]['name']))
        allresults['3name'] = str((data['businesses'][3]['name']))
        allresults['4name'] = str((data['businesses'][4]['name']))
        allresults['5name'] = str((data['businesses'][5]['name']))
        allresults['1rating'] = str((data['businesses'][1]['rating']))
        allresults['2rating'] = str((data['businesses'][2]['rating']))
        allresults['3rating'] = str((data['businesses'][3]['rating']))
        allresults['4rating'] = str((data['businesses'][4]['rating']))
        allresults['5rating'] = str((data['businesses'][5]['rating']))
        allresults['1price'] = str((data['businesses'][1]['price']))
        allresults['2price'] = str((data['businesses'][2]['price']))
        allresults['3price'] = str((data['businesses'][3]['price']))
        allresults['4price'] = str((data['businesses'][4]['price']))
        allresults['5price'] = str((data['businesses'][5]['price']))
        allresults['1image'] = str((data['businesses'][1]['image_url']))
        allresults['2image'] = str((data['businesses'][2]['image_url']))
        allresults['3image'] = str((data['businesses'][3]['image_url']))
        allresults['4image'] = str((data['businesses'][4]['image_url']))
        allresults['5image'] = str((data['businesses'][5]['image_url']))
        return render_template('results.html', data=data, priceInput=priceInput, searchresults=searchresults, allresults=allresults, radius=radius, priceInputSign=priceInputSign, rangeInputSign=rangeInputSign, cuisine=cuisine)
    # Here, you need to have logic like if there's a post request method, store the term and email from the form into
    # session dictionary
    if request.method == 'GET':
        return redirect(url_for('home'))

@app.route('/restart')
def restart():
    session.pop('username', None)
    return render_template('login.html')

@app.route('/yelp')
def yelp():  
        return render_template('results.html', data=data, searchresults=searchresults, term=term, allresults=allresults, cuisine=cuisine)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404
