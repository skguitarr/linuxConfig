from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine, desc, text
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Items

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#API Endpoint 1
@app.route('/catalog/JSON')
def categoryJSON():
    categories = session.query(Category).all()
    return jsonify(Category=[i.serialize for i in categories])

#API Endpoint 2
@app.route('/catalog/<int:category_id>/items/JSON')
def itemsJSON(category_id):
    items = session.query(Items).filter_by(category_id = category_id).all()
    return jsonify(Catalog=[i.serialize for i in items])

# Show all categories
@app.route('/')
@app.route('/catalog/')
def showCategories():
    sqlStatement = 'select i.name, i.creation_date, c.name as category_name from Items i, Category c where i.category_id = c.id order by i.creation_date desc limit 10'
    mostRecent = session.execute(sqlStatement).fetchall()
    categories = session.query(Category).all()
    #mostRecent = session.query(Items).order_by(desc(Items.creation_date)).limit(10)
    return render_template('categories.html', categories=categories, mostRecent=mostRecent)

# Show items for category 
@app.route('/catalog/<string:category_name>/')
@app.route('/catalog/<string:category_name>/items/')
def showItems(category_name):
    category = session.query(Category).filter_by(name=category_name).one()
    categories = session.query(Category).all()
    items = session.query(Items).filter_by(category_id=category.id).all()
    count = session.query(Items).filter_by(category_id=category.id).count()
    return render_template('items.html', items=items, category=category, categories=categories, count = count)

# Show item details
@app.route('/catalog/<string:category_name>/<string:item_name>/')
def showItemDetails(category_name, item_name):
    item = session.query(Items).filter_by(name=item_name).one()
    return render_template('itemDetails.html', category_name=category_name, item=item)

# Add Item
@app.route('/catalog/add', methods=['GET','POST'])
def addItem():
    if request.method == 'POST':
        print ('Add item \"POST\" triggered...')
        formCategory = session.query(Category).filter_by(name=request.form['categoryName']).one()
        addItem = Items(name=request.form['itemName'], description=request.form['description'], category_id=formCategory.id)
        session.add(addItem)
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        categories = session.query(Category).all()
        return render_template('addItem.html', categories=categories)

# Edit Item
@app.route('/catalog/<string:category_name>/<string:item_name>/edit', methods=['GET','POST'])
def editItem(category_name, item_name):
    editedItem = session.query(Items).filter_by(name=item_name).one()
    if request.method == 'POST':
        print ('Edit item \"POST\" triggered...')
        if request.form['itemName']:
            editedItem.name = request.form['itemName']
            item_name = editedItem.name
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['categoryName']:
            formCategory = session.query(Category).filter_by(name=request.form['categoryName']).one()
            editedItem.category_id = formCategory.id

        #print("Item name: " + editedItem.name)
        #print("Description: " + editedItem.description)
        #print("category ID: ", editedItem.category_id)
        session.add(editedItem)
        session.commit()
        return redirect(url_for('showItemDetails', category_name=formCategory.name, item_name=item_name))
    else:
        categories = session.query(Category).all()
        return render_template('editItem.html', categories=categories, category_name=category_name, item=editedItem)

# Delete Item

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
