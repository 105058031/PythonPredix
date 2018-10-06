from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc, text, bindparam
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from db_setup import Categories, Lineage, Items, Base
from flask import session as login_session

import random
import string
import os

ASSETS_DIR = os.path.dirname(os.path.abspath(__file__))
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

APPLICATION_NAME = "Auto Parts Application"

port = int(os.getenv("PORT", 3000))

engine = create_engine('sqlite:///itemCatalog.db')
Base.metadata.bind = engine

DBSession = scoped_session(sessionmaker(bind=engine))
session = DBSession()

categories=[{'id':'1','name':'Engines'},{'id':'2','name':'Intake Manifolds'},{'id':'3','name':'Carbs'},{'id':'4','name':'EFI systems'}]
#items=[{'id':'1','name':'Dodge 318', 'description':'OHV 90 degree V8 gasoline engine. 3.91 inch Bore x 3.31 inch Stroke. Built for economy and longevity.', 'catid':'4', 'price':'295 USD'},{'id':'2','name':'Dodge 340'},{'id':'3','name':'Dodge 383'},{'id':'4','name':'Dodge 426'},{'id':'4','name':'Dodge 440'}]
item = {'id':'1','name':'Dodge 318', 'description':'OHV 90 degree V8 gasoline engine. 3.91 inch Bore x 3.31 inch Stroke. Built for economy and longevity.', 'catid':'4', 'price':'295 USD'}
@app.route('/service-worker.js', methods=['GET'])
def sw():
	session = DBSession()
	return app.send_static_file('service-worker.js')


	
@app.route('/')
@app.route('/mcategory')
def mainCategories(mcid='1'):
	session = DBSession()
	
	Navs = [[1,"Main Categories"]]
	Main_Cats = session.query(Lineage).with_entities(Lineage.child_id).filter_by(parent_id = mcid).all()
	Main_Cats = [r for r, in Main_Cats]
			
	Cats_Disp = session.query(Categories).filter(Categories.id.in_((Main_Cats))).all() 
	return render_template("mCategories.html", items = Cats_Disp, navs=Navs)
@app.route('/mcategory/<int:mcid>/s')
def subCategories(mcid):
	session = DBSession()
	Main_Cats = session.query(Lineage).with_entities(Lineage.child_id).filter_by(parent_id = mcid).all()
	Main_Cats = [r for r, in Main_Cats]
		
	Cats_Disp = session.query(Categories).filter(Categories.id.in_((Main_Cats))).all()
	# Fill the navs array
	NavItems = navigationSnippet(mcid)
	return render_template("mCategories.html", items = Cats_Disp, navs = NavItems)
@app.route('/mcategory/<int:mcid>/new', methods=['GET', 'POST'])
def newmainCategory(mcid):
	session = DBSession()
	Main_Cats = session.query(Lineage).with_entities(Lineage.child_id).filter_by(parent_id = mcid).all()
	Main_Cats = [r for r, in Main_Cats]
	Cats_Disp = session.query(Categories).filter(Categories.id.in_((Main_Cats))).all()
	NavItems = navigationSnippet(mcid)
	if request.method == 'POST':
		newCategory = Categories(name=request.form['name'])
		session.add(newCategory)
		session.commit()
		nId = session.query(Categories).with_entities(Categories.id).filter_by(name = request.form['name']).limit(1).one()
		print nId[0]
		newLineage = Lineage(parent_id=mcid, child_id=nId[0])
		session.add(newLineage)
		session.commit()
		 
		return redirect(url_for('decide', mcid = mcid))
	else:
		return render_template('newCategory.html', navs=NavItems)
@app.route('/mcategory/<int:mcid>/edit', methods=['GET', 'POST'])
def editmainCategory(mcid):
	session = DBSession()
	#editedCategory = session.query(Categories).filter_by(id=mcid).one()
	
	
	if request.method == 'POST':
		if request.form['name']:
			print("request name to change to is:" + request.form['name'])
			#editedCategory.name = request.form['name']
			session.query(Categories).filter_by(id=mcid).update({"name": request.form['name']})
			session.commit()
			return redirect(url_for('subCategories', mcid = pid))
	else:
		NavItems = navigationSnippet(mcid)
		return render_template("editCategory.html", mcid = mcid, navs =NavItems) 
	
@app.route('/mcategory/<int:mcid>/delete', methods=['GET', 'POST'])
def deletemainCategory(mcid):
	session = DBSession()
	categoriesToDelete = session.query(Categories).filter_by(id=mcid).one()
	parentCatId = session.query(Lineage).with_entities(Lineage.parent_id).filter_by(child_id=mcid).first()
	pid = parentCatId[0]
	print "This is the parentCatid: " + str(pid)
	if request.method == 'POST':
		session.delete(categoriesToDelete)
		session.commit()
		return redirect(url_for('subCategories', mcid=pid))
	else:
		NavItems = navigationSnippet(mcid)
		return render_template("deleteCategory.html", mcid = mcid, navs=NavItems)   

@app.route('/mcategory/<int:mcid>/items')
@app.route('/mcategory/<int:mcid>/i')
def mainItems(mcid):
	session = DBSession()
	stmt = text("SELECT i.*, l.parent_id as pid FROM items i INNER JOIN lineage l ON i.category_id==l.child_id WHERE i.category_id = :x")
	stmt = stmt.bindparams(x=mcid)
	Main_Its = session.execute(stmt,{}).fetchall()
	print "----------------------" 
	print "Length of results: "  + str(len(Main_Its))
	
	Bool = (len(Main_Its)==0) 
	print "Condition: " + str(Bool)
	print "----------------------"
	#(Items).filter_by(category_id = mcid).all()
	NavItems = navigationSnippet(mcid)
	return render_template("mItems.html", bool = Bool, items = Main_Its, navs = NavItems)

@app.route('/mcategory/<int:mcid>/item/new', methods=['GET', 'POST'])
def newItem(mcid):
	session = DBSession()
	print "MCID: " + str(mcid)
	NavItems = navigationSnippet(mcid)
	
	if request.method == 'POST':
		print "Request method was POST"
		
		newItem = Items(name=request.form['name'], \
		description=request.form['description'], \
		price=request.form['price'], \
		category_id=mcid)
		print
		session.add(newItem)
		session.commit()
		return redirect(url_for('mainItems', mcid=mcid))
	else:
		return render_template('newItems.html', mcid=mcid, navs = NavItems )
		
@app.route('/item/<int:itid>/edit', methods=['GET', 'POST'])
def editItem(itid):
	session = DBSession()
	parentCatId = session.query(Items).with_entities(Items.category_id).filter_by(id=itid).one()
	print parentCatId[0]
	mcid = parentCatId[0]
	NavItems = navigationSnippet(mcid)
	if request.method == 'POST':
		editedItem = session.query(Items).filter_by(id=itid).one()
		if request.form['name']:
			editedItem.name = request.form['name']
		if request.form['description']:
			editedItem.description = request.form['description']
		if request.form['price']:
			editedItem.price = request.form['price']
		session.add(editedItem)
		session.commit()
		return redirect(url_for('mainItems', mcid=mcid))
	else:
		stmt = text("SELECT i.id, i.name, i.description, i.price, l.parent_id as pid FROM items i OUTER LEFT JOIN lineage l ON i.category_id==l.child_id WHERE i.category_id = :x")
		stmt = stmt.bindparams(x=mcid)
		editedItem = session.execute(stmt,{}).fetchall()
		return render_template('editItems.html', navs=NavItems, item=editedItem[0])
	
@app.route('/item/<int:itid>/delete', methods=['GET', 'POST'])
def deleteItem(itid):
	session = DBSession()
	itemToDelete = session.query(Items).filter_by(id=itid).one()
	parentCatId = session.query(Items).with_entities(Items.category_id).filter_by(id=itid).one()
	mcid = parentCatId[0]
	NavItems = navigationSnippet(mcid)
	if request.method == 'POST':
		session.delete(itemToDelete)
		session.commit()
		return redirect(url_for('subCategories', mcid=mcid))
	else:
		return render_template('deleteItems.html', item=itemToDelete, navs = NavItems )
	
	
	
@app.route('/redirect/<int:mcid>')
@app.route('/redirect/<int:mcid>/')
def decide(mcid):
	session = DBSession()
	Main_Cats = session.query(Lineage).with_entities(Lineage.child_id).filter_by(parent_id = mcid).all()
	nr = len(Main_Cats)
	#Main_Its = session.query(Items).filter_by(category_id = mcid).all()

	print "The query returned the following number of records: %s " % nr
	print "The condition: " + str(nr<1)
	if (nr<1):

		return redirect(url_for('mainItems', mcid = mcid))
		#return render_template("mainItems(mcid,itid))"no subcategories"
		#return redirect("/mcategory/"+mcid, code=302)
	else:
		return redirect(url_for('subCategories', mcid = mcid))


def navigationSnippet(id):
	session = DBSession()
	if (id > 0):
		lastChild=id
		Navs=[]
		stmt = text("SELECT c.name FROM categories c WHERE c.id == :x")
		stmt = stmt.bindparams(x=lastChild)
		Results = session.execute(stmt,{}).fetchall()
		Navs.append([id,Results[0][0]])
		print "----------------------"
		print str(id) + " - " + str(Results[0][0])
		while (lastChild > 1):
			stmt = text("SELECT l.parent_id, c.name FROM lineage l LEFT OUTER JOIN categories c ON c.id == l.parent_id WHERE l.child_id = :x")
			stmt = stmt.bindparams(x=lastChild)
			Results = session.execute(stmt,{}).fetchall()
			print(str(Results[0][0]) + " - " + str(Results[0][1])) 
			lastChild = Results[0][0]
			Navs.append(Results[0])
		print "----------------------"
		return Navs

		
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=port)