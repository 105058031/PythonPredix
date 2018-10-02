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
	Main_Cats = session.query(Lineage).with_entities(Lineage.child_id).filter_by(parent_id = mcid).all()
	Main_Cats = [r for r, in Main_Cats]
		
	Cats_Disp = session.query(Categories).filter(Categories.id.in_((Main_Cats))).all() 
	return render_template("mCategories.html", items = Cats_Disp)
@app.route('/mcategory/<int:mcid>/s')
def subCategories(mcid):
	session = DBSession()
	Main_Cats = session.query(Lineage).with_entities(Lineage.child_id).filter_by(parent_id = mcid).all()
	Main_Cats = [r for r, in Main_Cats]
		
	Cats_Disp = session.query(Categories).filter(Categories.id.in_((Main_Cats))).all() 
	return render_template("mCategories.html", items = Cats_Disp)
@app.route('/mcategory/new')
def newmainCategory():
	session = DBSession()
	return render_template("newCategory.html")   
@app.route('/mcategory/<int:mcid>/edit')
def editmainCategory(mcid):
	session = DBSession()
	return render_template("editCategory.html", mcid = mcid) 
	
@app.route('/mcategory/<int:mcid>/delete')
def deletemainCategory(mcid):
	session = DBSession()
	return render_template("deleteCategory.html", mcid = mcid)   

@app.route('/mcategory/<int:mcid>/items')
@app.route('/mcategory/<int:mcid>/i')
def mainItems(mcid):
	session = DBSession()
	stmt = text("SELECT i.*, l.parent_id as pid FROM items i OUTER LEFT JOIN lineage l ON i.category_id==l.child_id WHERE i.category_id = :x")
	stmt = stmt.bindparams(x=mcid)
	Main_Its = session.execute(stmt,{}).fetchall()
	#(Items).filter_by(category_id = mcid).all()
	rowcount = len(Main_Its)
	print str(rowcount)
	
	return render_template("mItems.html", items = Main_Its)
@app.route('/mcategory/<int:mcid>/scategory/<int:scid>/dcategory/<int:dcid>/item/new')
def newItem(mcid,itid):
	session = DBSession()
	return 'This is for creating a new item in detail category # %(dcid)s in the sub category # %(scid)s in main category # %(mcid)s' % locals()
@app.route('/item/<int:itid>/edit')
def editItem(itid):
	session = DBSession()
	return 'This is for editing the item # %(itid)s' % locals()
@app.route('/item/<int:itid>/delete')
def deleteItem(itid):
	session = DBSession()
	return 'This is for deleting the item %(itid)s' 
	
	
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
	
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=port)