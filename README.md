# Flask Item Catalog Project v1.0

This is an SQLite web application on a Flask framework using the 
GE Predix Python source code and python buildpacks for deployment to predix server.

#List of Files

README2.txt
populateCatalog.py
db_setup.py
app.py
db_setup.pyc
client_secrets.json
itemCatalog.db
requirements.txt
manifest.yml
README.md
Procfile
cascading stylesheets and font files in the static folder
templates for
	login
	displaying categories or subcategories
	editing categories or subcategories
	deleting categories or subcategories
	creating new categories or subcategories

# Description

The db_setup.py script is designed to create the main database for the items, categories and users of the application
the populateCatalog.py file fills the application database with some starter information, which creates a 4 level Lineage. 
Meaning that the longest category tree has 3 child categories before the user is presented with the items withheld in any one child category

The application utilizes Google API for logging in to the application.
Without authentication it is possible to view all categories, subcategories and items contained within, 
but it requires a signed in user to create new items and categories and to edit or delete existing ones.
When a new category is created it's possible to add either subcategories to it or items, but not both.
If a category has been given a child category, any items will have to be added to the child category. 
Similarly a category that contains items cannot receive a child category.
The tree or Lineage of categories is displayed with working links to any level of the lineage on the navigation bar. 

The package includes requirements.txt with the correct dependencies for Predix deployment.
Heroku deployment can utilize later pip packages(pip@18.1)

# Getting Started

Clone the PythonPredix repository from https://github.com/105058031/PythonPredix.git

# Prerequisites

Python2.7
pip 9.0.3 or later
https://files.pythonhosted.org/packages/ee/a7/d6d238d927df355d4e4e000670342ca4705a72f0bf694027cf67d9bcf5af/passlib-1.7.1-py2.py3-none-any.whl
werkzeug@0.14.1
Flask@1.0.2
Flask-Login@0.1.3
Flask-SQLAlchemy@0.16
git+https://github.com/miguelgrinberg/Flask-HTTPAuth.git@master
oauth2client
requests
httplib2

# Installing

A step by step series of examples that tell you how to get a development env running

Install Python 2.7
	download get-pip.py
	run get-pip.py with python2.7
	run the command 'pip install -r requirements.txt' in python2.7
Delete the itemCatalog.db # optional
Create the main database by running # if original database was deleted
	'python db_setup.py' 
Populate the database with # if original database was deleted
	'python populateCatalog.py'
Run the application in development environment:
	'python app.py'
Deploy to heroku/predix

Example application:
	https://itemcatalog.run.aws-usw02-pr.ice.predix.io/

# Credits
Used Codehandbooks predix supported flask package:
https://github.com/codehandbook/PythonPredix

The sample database information was sourced from wikipedia and www.jegs.com 

# Authors

* **Gabor Dubniczki** 

#Releases
2018 - Oct - 10  - v1.0
	first release
