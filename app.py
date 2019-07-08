from flask import Flask, render_template
from flask import request, flash, url_for, redirect, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
from config import DATABASE_URL

app = Flask(__name__)

engine = create_engine(DATABASE_URL)
Base.metadata.bind=engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/')
@app.route('/restaurants/')
def Home():
    restaurants = session.query(Restaurant).all()
    return render_template("home.html", restaurants=restaurants)

@app.route('/restaurants/JSON/')
def restaurantsJSON():
	restaurants = session.query(Restaurant).all()
	return jsonify(Restaurants=[r.serialize for r in restaurants])

@app.route('/restaurants/create/', methods = ['POST', 'GET'])
def createRestaurant():
    if request.method=='POST':
        if request.form['name']:
            name = request.form['name']
            restaurant = Restaurant(name=name)
            session.add(restaurant)
            session.commit()
            flash("New restaurant created!")
            return redirect(url_for('Home'))
        else:
            return "ERROR"
    else:
        return render_template('createRestaurant.html')
    return render_template('createRestaurant.html')

@app.route('/restaurant/<int:restaurant_id>/menu_items/')
def readRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).first()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id).all()
    return render_template('menuItems.html', items=items, restaurant=restaurant)

@app.route('/restaurant/<int:restaurant_id>/menu_items/JSON')
def menuItemsJSON(restaurant_id):
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurant/<int:restaurant_id>/update/',  methods = ['POST', 'GET'])
def updateRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method=='POST':
        name = request.form['name']
        restaurant.name = name
        session.add(restaurant)
        session.commit()
        flash("Restaurant editado!")
        return redirect(url_for('Home'))
    else:
        return render_template("updateRestaurant.html", restaurant=restaurant)

@app.route('/restaurant/<int:restaurant_id>/delete/', methods = ['POST', 'GET'])
def deleteRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method=="POST":
        session.delete(restaurant)
        session.commit()
        flash("Restaurant deletado!")
        return redirect(url_for('Home'))
    else:
        return render_template('deleteRestaurant.html', restaurant=restaurant)

@app.route('/restaurant/<int:restaurant_id>/menu_items/create/',  methods=['POST','GET'])
def createMenuItem(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method=='POST':
        if request.form['name']:
            name = request.form['name']
            description = request.form['description']
            price = request.form['price']
            course = request.form['course']
            item = MenuItem(
                name = name,
                description = description,
                price = price,
                course = course,
                restaurant_id = restaurant.id
            )
            session.add(item)
            session.commit()
            flash("New item menu created!")
            return redirect(url_for('readRestaurant', restaurant_id=restaurant.id))
        else:
            return "ERROR"
    else:
        return render_template('createMenuItem.html', restaurant=restaurant)

@app.route('/restaurant/<int:restaurant_id>/menu_item/<int:item_id>/update/', methods=["POST","GET"])
def updateMenuItem(restaurant_id, item_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    item = session.query(MenuItem).filter_by(id=item_id).one()
    if request.method=='POST':
        item.name = request.form['name']
        item.description = request.form['description']
        item.price = request.form['price']
        item.course = request.form['course']
        session.add(item)
        session.commit()
        flash("Item editado!")
        return redirect(url_for('readRestaurant', restaurant_id=restaurant.id))
    else:
        return render_template("updateMenuItem.html", restaurant=restaurant, item=item)

@app.route('/restaurant/<int:restaurant_id>/menu_item/<int:item_id>/JSON/')
def itemJSON(restaurant_id, item_id):
    item = session.query(MenuItem).filter_by(id=item_id).one()
    return jsonify(Item=item.serialize)

@app.route('/restaurant/<int:restaurant_id>/menu_item/<int:item_id>/delete/',methods=["POST","GET"])
def deleteMenuItem(restaurant_id, item_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    item = session.query(MenuItem).filter_by(id=item_id).one()
    if request.method == "POST":
    	session.delete(item)
    	session.commit()
    	flash("Item deletado!")
    	return redirect(url_for('readRestaurant',restaurant_id=restaurant.id))
    else:
    	return render_template('deleteMenuItem.html',item=item, restaurant=restaurant)

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.debug = True
    app.run(host = 'localhost', port = 5000, threaded=False)
    # app.run(port=8989,threaded=False) # old