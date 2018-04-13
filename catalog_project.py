from flask import (
    Flask, render_template, request,
    redirect, url_for, flash, jsonify
)
from sqlalchemy import create_engine, desc, text
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Items, User
from flask import session as login_session
import random
import string
import httplib2
import requests
import json
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from flask import make_response

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Guitar Catalog"

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/catalog/login/')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template(
            'login.html', STATE=state, login_session=login_session
    )


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
                json.dumps('Current user is already connected.'), 200
        )
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['logged_in'] = True

    # If user does not exist add them to the DB
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " class = "redirect-style"> '
    flash("You are now logged in as %s!" % login_session['username'])
    print("done!")
    return output


# Create a new user
def createUser(login_session):
    newUser = User(username=login_session['username'],
                   email=login_session['email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


# Get the user data from the DB object
def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


# Get the user's id based on email
def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/gdisconnect')
def gdisconnect():
    url_pre = 'https://accounts.google.com/o/oauth2/revoke?token=%s'
    access_token = login_session.get('access_token')
    if access_token is None:
        print('Access Token is None')
        response = make_response(
                json.dumps('Current user not connected.'), 401
        )
        response.headers['Content-Type'] = 'application/json'
        return response
    print('In gdisconnect access token is %s', access_token)
    print('User name is: ')
    print(login_session['username'])
    url = url_pre % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print('result is ')
    print(result)
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['logged_in']
        del login_session['user_id']
        flash("Successfully disconnected!")
        return redirect(url_for('showCategories'))
    else:
        response = make_response(
                json.dumps('Failed to revoke token for given user.', 400)
        )
        response.headers['Content-Type'] = 'application/json'
        return response


# API Endpoint 1 - return all categories
@app.route('/catalog/JSON')
def categoryJSON():
    categories = session.query(Category).all()
    return jsonify(Category=[i.serialize for i in categories])


# API Endpoint 2 - return all items for each category
@app.route('/catalog/<int:category_id>/items/JSON')
def itemsJSON(category_id):
    items = session.query(Items).filter_by(category_id=category_id).all()
    return jsonify(Catalog=[i.serialize for i in items])


# API Endpoint 3 - return details of a single item
@app.route('/catalog/<int:category_id>/items/<int:item_id>/JSON')
def itemDetailsJSON(category_id, item_id):
    query = session.query(Items)
    item = query.filter_by(category_id=category_id, id=item_id).all()
    return jsonify(Item=[i.serialize for i in item])


# Show all categories
@app.route('/')
@app.route('/catalog/')
def showCategories():
    sqlStatement = 'select i.name, i.creation_date, c.name as category_name'
    sqlStatement += ' from Items i, Category c where i.category_id=c.id order'
    sqlStatement += ' by i.creation_date desc limit 10'
    mostRecent = session.execute(sqlStatement).fetchall()
    categories = session.query(Category).all()
    # mostRecent=session.query(Items).order_by(desc(Items.creation_date)).limit(10)
    return render_template(
            'categories.html', categories=categories,
            mostRecent=mostRecent, login_session=login_session
    )


# Show items for category
@app.route('/catalog/<string:category_name>/')
@app.route('/catalog/<string:category_name>/items/')
def showItems(category_name):
    category = session.query(Category).filter_by(name=category_name).one()
    categories = session.query(Category).all()
    items = session.query(Items).filter_by(category_id=category.id).all()
    count = session.query(Items).filter_by(category_id=category.id).count()
    return render_template(
            'items.html', items=items, category=category,
            categories=categories, count=count,
            login_session=login_session
    )


# Show item details
@app.route('/catalog/<string:category_name>/<string:item_name>/')
def showItemDetails(category_name, item_name):
    item = session.query(Items).filter_by(name=item_name).one()
    return render_template(
            'itemDetails.html', category_name=category_name,
            item=item, login_session=login_session
    )


# Add Item
@app.route('/catalog/add', methods=['GET', 'POST'])
def addItem():
    if 'username' not in login_session:
        flash("You must login first before adding an item!")
        return redirect('/catalog/login/')
    if request.method == 'POST':
        print ('Add item \"POST\" triggered...')
        qry = session.query(Category)
        formCategory = qry.filter_by(name=request.form['categoryName']).one()
        addItem = Items(
                name=request.form['itemName'],
                description=request.form['description'],
                category_id=formCategory.id, user_id=login_session['user_id']
        )
        session.add(addItem)
        session.commit()
        flash("New item successfully created!")
        return redirect(url_for('showCategories'))
    else:
        categories = session.query(Category).all()
        return render_template(
                'addItem.html', categories=categories,
                login_session=login_session
        )


# Edit Item
@app.route('/catalog/<string:category_name>/<string:item_name>/edit',
           methods=['GET', 'POST'])
def editItem(category_name, item_name):
    editedItem = session.query(Items).filter_by(name=item_name).one()
    if 'username' not in login_session:
        flash("You must login first before editing an item!")
        return redirect('/catalog/login/')
    elif editedItem.user_id != login_session['user_id']:
        flash("You did not create this item, therefore you cannot EDIT it!")
        return redirect(
                url_for(
                    'showItemDetails', category_name=category_name,
                    item_name=item_name, login_session=login_session
                )
        )

    if request.method == 'POST':
        print ('Edit item \"POST\" triggered...')
        if request.form['itemName']:
            editedItem.name = request.form['itemName']
            item_name = editedItem.name
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['categoryName']:
            q = session.query(Category)
            formCategory = q.filter_by(name=request.form['categoryName']).one()
            editedItem.category_id = formCategory.id

        session.add(editedItem)
        session.commit()
        flash("Successfully updated!")
        return redirect(
                url_for(
                    'showItemDetails', category_name=formCategory.name,
                    item_name=item_name, login_session=login_session
                )
        )
    else:
        categories = session.query(Category).all()
        return render_template(
                'editItem.html', categories=categories,
                category_name=category_name, item=editedItem,
                login_session=login_session
        )


# Delete Item
@app.route('/catalog/<string:category_name>/<string:item_name>/delete',
           methods=['GET', 'POST'])
def deleteItem(category_name, item_name):
    itemForDelete = session.query(Items).filter_by(name=item_name).one()
    if 'username' not in login_session:
        flash("You must login first before deleting an item!")
        return redirect('/catalog/login/')
    elif itemForDelete.user_id != login_session['user_id']:
        flash("You did not create this item, therefore you cannot DELETE it!")
        return redirect(
                url_for(
                    'showItemDetails', category_name=category_name,
                    item_name=item_name, login_session=login_session
                )
        )

    if request.method == 'POST':
        print ('Delete item \"POST\" triggered...')
        session.delete(itemForDelete)
        session.commit()
        flash("Successfully deleted!")
        return redirect(url_for('showCategories'))
    else:
        return render_template(
                'deleteItem.html', category_name=category_name,
                item_name=item_name, login_session=login_session
        )


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
