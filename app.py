import httplib2
import json
import requests
import random
import string
import os
from flask import Flask, render_template, request, redirect
from flask import jsonify, url_for, flash, abort, g
from sqlalchemy import create_engine, asc, text, bindparam
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.orm import scoped_session
from db_setup import Categories, Lineage, Items, User, Base
from flask import session as login_session
from flask_httpauth import HTTPBasicAuth
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from flask import make_response

auth = HTTPBasicAuth()
ASSETS_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)

APPLICATION_NAME = "Auto Parts Application"

port = int(os.getenv("PORT", 3000))

engine = create_engine('sqlite:///itemCatalog.db')
Base.metadata.bind = engine

DBSession = scoped_session(sessionmaker(bind=engine))
session = DBSession()

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']


@auth.verify_password
def verify_password(username_or_token, password):
    session = DBSession()
# Try to see if it's a token first
    print "verifying the password now"
    user_id = User.verify_auth_token(username_or_token)
    print "user_id: " + str(user_id)
    if user_id:
        print "primary verification succeeded"
        user = session.query(User).filter_by(id=user_id).one()
    else:
        print "secondary verification"
        user = session.\
            query(User).\
            filter_by(username=username_or_token).\
            first()
        if not user or not user.verify_password(password):
            print "User not found, redirecting"
            return False
    g.user = user
    return True


@app.route('/login')
def showLogin(Bool=False):
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('oauthLogin.html', bool=Bool, STATE=state, LG=False)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') ! =  login_session['state']:
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
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token = %s'
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
    if result['user_id'] ! =  gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] ! =  CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('''Current user is
                                            already connected.'''),
                                 200)
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

    output = ''
    output + =  '<h1>Welcome, '
    output + =  login_session['username']
    output + =  '!</h1>'
    output + =  '<img src = "'
    output + =  login_session['picture']
    output + =  ''' " style = "width: 300px; height:
    300px;border-radius: 150px;-webkit-border-radius: 150px;
    -moz-border-radius: 150px;"> '''
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return redirect(url_for('mainCategories', mcid=1))


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('''Current user not
                                            connected.'''), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token = %s' % \
        login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('''Failed to revoke token for
                                            given user.''', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/api/users', methods=['POST'])
def new_user():
    session = DBSession()
    if 'username' not in login_session:
        return redirect('/login')
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400)
# missing arguments
    if session.query(User).filter_by(username=username).first() is not None:
        abort(400)
# existing user
    user = User(username=username)
    user.hash_password(password)
    session.add(user)
    session.commit()
    return jsonify({'username':
                   user.username}), 201, {'Location': url_for('get_user',
                                                              id=user.id,
                                                              _external=True)}


@app.route('/api/users/<int:id>')
def get_user(id):
    session = DBSession()
    if 'username' not in login_session:
        return redirect('/login')
    user = session.query(User).filter_by(id=id).one()
    if not user:
        abort(400)
    return jsonify({'username': user.username})


@app.route('/service-worker.js', methods=['GET'])
def sw():
    session = DBSession()
    return app.send_static_file('service-worker.js')


@app.route('/')
@app.route('/mcategory')
def mainCategories(mcid='1'):
    session = DBSession()
    if 'username' not in login_session:
        Bool = False
    else:
        Bool = True
    Navs = [[1, "Main Categories"]]
    Main_Cats = session.query(Lineage).\
        with_entities(Lineage.child_id).\
        filter_by(parent_id=mcid).\
        all()
    Main_Cats = [r for r, in Main_Cats]

    Cats_Disp = session.query(Categories).\
        filter(Categories.id.in_((Main_Cats))).\
        all()
    return render_template("mCategories.html",
                           items=Cats_Disp,
                           navs=Navs,
                           LG=Bool)


@app.route('/mcategory/<int:mcid>/s')
def subCategories(mcid):
    session = DBSession()
    if 'username' not in login_session:
        Bool = False
    else:
        Bool = True
    Main_Cats = session.query(Lineage).\
        with_entities(Lineage.child_id).\
        filter_by(parent_id=mcid).\
        all()
    Main_Cats = [r for r, in Main_Cats]

    Cats_Disp = session.query(Categories).\
        filter(Categories.id.in_((Main_Cats))).\
        all()
    # Fill the navs array
    NavItems = navigationSnippet(mcid)
    return render_template("mCategories.html",
                           items=Cats_Disp,
                           navs=NavItems,
                           LG=Bool)


@app.route('/mcategory/<int:mcid>/new', methods=['GET', 'POST'])
def newmainCategory(mcid):
    session = DBSession()
    if 'username' not in login_session:
        return redirect('/login')
    else:
        Bool = True
    Main_Cats = session.query(Lineage).\
        with_entities(Lineage.child_id).\
        filter_by(parent_id=mcid).\
        all()
    Main_Cats = [r for r, in Main_Cats]
    Cats_Disp = session.query(Categories).\
        filter(Categories.id.in_((Main_Cats))).\
        all()
    NavItems = navigationSnippet(mcid)
    if request.method == 'POST':
        newCategory = Categories(name=request.form['name'])
        session.add(newCategory)
        session.commit()
        nId = session.query(Categories).\
            with_entities(Categories.id).\
            filter_by(name=request.form['name']).\
            limit(1).\
            one()
        print nId[0]
        newLineage = Lineage(parent_id=mcid, child_id=nId[0])
        session.add(newLineage)
        session.commit()

        return redirect(url_for('decide', mcid=mcid))
    else:
        return render_template('newCategory.html', navs=NavItems, LG=Bool)


@app.route('/mcategory/<int:mcid>/edit', methods=['GET', 'POST'])
def editmainCategory(mcid):
    session = DBSession()

    if 'username' not in login_session:
        return redirect('/login')
    else:
        Bool = True
    if request.method == 'POST':
        if request.form['name']:
            print("request name to change to is:" + request.form['name'])
            session.query(Categories).\
                filter_by(id=mcid).\
                update({"name": request.form['name']})
            session.commit()
            return redirect(url_for('subCategories', mcid=pid))
    else:
        NavItems = navigationSnippet(mcid)
        return render_template("editCategory.html",
                               mcid=mcid,
                               navs=NavItems,
                               LG=Bool)


@app.route('/mcategory/<int:mcid>/delete', methods=['GET', 'POST'])
def deletemainCategory(mcid):
    session = DBSession()
    if 'username' not in login_session:
        return redirect('/login')
    else:
        Bool = True
    categoriesToDelete = session.query(Categories).filter_by(id=mcid).one()
    parentCatId = session.query(Lineage).\
        with_entities(Lineage.parent_id).\
        filter_by(child_id=mcid).\
        first()
    pid = parentCatId[0]
    print "This is the parentCatid: " + str(pid)
    if request.method == 'POST':
        session.delete(categoriesToDelete)
        session.commit()
        return redirect(url_for('subCategories', mcid=pid))
    else:
        NavItems = navigationSnippet(mcid)
        return render_template("deleteCategory.html",
                               mcid=mcid,
                               navs=NavItems,
                               LG=Bool)


@app.route('/mcategory/<int:mcid>/items')
@app.route('/mcategory/<int:mcid>/i')
def mainItems(mcid):
    session = DBSession()
    if 'username' not in login_session:
        Bool = False
    else:
        Bool = True
    stmt = text("""SELECT i.*, l.parent_id as pid FROM items i
               INNER JOIN lineage l ON i.category_id =  = l.child_id
               WHERE i.category_id = :x""")
    stmt = stmt.bindparams(x=mcid)
    Main_Its = session.execute(stmt, {}).fetchall()
    print "----------------------"
    print "Length of results: " + str(len(Main_Its))

    Bool = (len(Main_Its) == 0)
    print "Condition: " + str(Bool)
    print "----------------------"
    NavItems = navigationSnippet(mcid)
    return render_template("mItems.html",
                           bool=Bool,
                           items=Main_Its,
                           navs=NavItems,
                           LG=Bool)


@app.route('/mcategory/<int:mcid>/item/new', methods=['GET', 'POST'])
def newItem(mcid):
    session = DBSession()
    if 'username' not in login_session:
        return redirect('/login')
    else:
        Bool = True
    print "MCID: " + str(mcid)
    NavItems = navigationSnippet(mcid)

    if request.method == 'POST':
        print "Request method was POST"
        newItem = Items(name=request.form['name'],
                        description=request.form['description'],
                        price=request.form['price'],
                        category_id=mcid)
        print
        session.add(newItem)
        session.commit()
        return redirect(url_for('mainItems', mcid=mcid))
    else:
        return render_template('newItems.html',
                               mcid=mcid,
                               navs=NavItems,
                               LG=Bool)


@app.route('/item/<int:itid>/edit', methods=['GET', 'POST'])
def editItem(itid):
    session = DBSession()
    if 'username' not in login_session:
        return redirect('/login')
    else:
        Bool = True
    parentCatId = session.query(Items).\
        with_entities(Items.category_id).\
        filter_by(id=itid).\
        one()
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
        stmt = text("""SELECT i.id, i.name, i.description, i.price,
                    l.parent_id as pid FROM items i OUTER LEFT JOIN
                    lineage l ON i.category_id =  = l.child_id
                    WHERE i.category_id = :x""")
        stmt = stmt.bindparams(x=mcid)
        editedItem = session.execute(stmt, {}).fetchall()
        return render_template('editItems.html',
                               navs=NavItems,
                               item=editedItem[0], LG=Bool)


@app.route('/item/<int:itid>/delete', methods=['GET', 'POST'])
def deleteItem(itid):
    session = DBSession()
    if 'username' not in login_session:
        return redirect('/login')
    else:
        Bool = True
    itemToDelete = session.query(Items).filter_by(id=itid).one()
    parentCatId = session.query(Items). \
        with_entities(Items.category_id). \
        filter_by(id=itid).one()
    mcid = parentCatId[0]
    NavItems = navigationSnippet(mcid)
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('subCategories', mcid=mcid))
    else:
        return render_template('deleteItems.html',
                               item=itemToDelete,
                               navs=NavItems, LG=Bool)


@app.route('/redirect/<int:mcid>')
@app.route('/redirect/<int:mcid>/')
def decide(mcid):
    session = DBSession()
    Main_Cats = session.query(Lineage).\
        with_entities(Lineage.child_id).\
        filter_by(parent_id=mcid).all()
    nr = len(Main_Cats)
    print "The query returned the following number of records: %s " % nr
    print "The condition: " + str(nr < 1)
    if (nr < 1):
        return redirect(url_for('mainItems', mcid=mcid))
    else:
        return redirect(url_for('subCategories', mcid=mcid))


def navigationSnippet(id):
    session = DBSession()
    if (id > 0):
        lastChild = id
        Navs = []
        stmt = text("SELECT c.name FROM categories c WHERE c.id  =  =  :x")
        stmt = stmt.bindparams(x=lastChild)
        Results = session.execute(stmt, {}).fetchall()
        Navs.append([id, Results[0][0]])
        print "----------------------"
        print str(id) + " - " + str(Results[0][0])
        while (lastChild > 1):
            stmt = text("""SELECT l.parent_id, c.name FROM lineage l
                        LEFT OUTER JOIN categories c ON c.id  =  =  l.parent_id
                        WHERE l.child_id = :x""")
            stmt = stmt.bindparams(x=lastChild)
            Results = session.execute(stmt, {}).fetchall()
            print(str(Results[0][0]) + " - " + str(Results[0][1]))
            lastChild = Results[0][0]
            Navs.append(Results[0])
        print "----------------------"
        return Navs

if(__name__ == '__main__'):
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=port)
