from flask import Flask, request, render_template, flash, redirect, url_for, session
from flask_socketio import SocketIO
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re 
from datetime import datetime
from plotGraph import *
from index import *
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from markupsafe import Markup
from flask_sqlalchemy import SQLAlchemy
from flask_user import current_user, login_required, roles_required, UserManager, UserMixin
from flask_babelex import Babel
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from http import HTTPStatus
from flask_bcrypt import Bcrypt
from sqlalchemy import desc
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask import jsonify
import json





# Class-based application configurationcd
class ConfigClass(object):
    """ Flask application config """

    # Flask settings
    SECRET_KEY = 'This is an INSECURE secret!! DO NOT use this in production!!'

    # Flask-SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = 'mysql://jthp:.15is8Ssf8Wm0j@jthp.host.cs.st-andrews.ac.uk/jthp_pythonlogin'    # File-based SQL database
    #SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False    # Avoids SQLAlchemy warning

    # Flask-User settings
    USER_APP_NAME = "SH Project"      # Shown in and email templates and page footers
    USER_ENABLE_EMAIL = False        # Enable email authentication
    USER_ENABLE_USERNAME = True    # Disable username authentication
    USER_REQUIRE_RETYPE_PASSWORD = False    # Simplify register form
    USER_ENABLE_AUTH0 = False
   






def create_app():
        """ Flask application factory """
        
    # Flask constructor
        app = Flask(__name__)
        app.config.from_object(__name__+'.ConfigClass')
        socketio = SocketIO(app)

    # Initialize Flask-BabelEx
        babel = Babel(app)

        # Initialize Flask-SQLAlchemy
        db = SQLAlchemy(app)
        bcrypt = Bcrypt(app)
        

        login_manager = LoginManager()
        login_manager.init_app(app)
        login_manager.login_view = 'login'

        @login_manager.unauthorized_handler     # In unauthorized_handler we have a callback URL 
        def unauthorized_callback():            # In call back url we can specify where we want to 
            return redirect(url_for('login')) # redirect the user in my case it is login page!
            # User is not loggedin redirect to login page
        
        

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

    # # Change this to your secret key (can be anything, it's for extra protection)
    # app.secret_key = 'your secret key'

    # # Enter your database connection details below
    # app.config['MYSQL_HOST'] = 'jthp.host.cs.st-andrews.ac.uk'
    # app.config['MYSQL_USER'] = 'jthp'
    # app.config['MYSQL_PASSWORD'] = '.15is8Ssf8Wm0j'
    # app.config['MYSQL_DB'] = 'jthp_pythonlogin'

    # Intialize MySQL
    #mysql = MySQL(app)

    # Define the User data-model.
        # NB: Make sure to add flask_user UserMixin !!!
        class User(db.Model, UserMixin):
                __tablename__ = 'users'
                id = db.Column(db.Integer, primary_key=True)
                active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

                # User authentication information. The collation='NOCASE' is required
                # to search case insensitively when USER_IFIND_MODE is 'nocase_collation'.
                username = db.Column(db.String(100), nullable=False, unique=True)
                password = db.Column(db.String(255), nullable=False, server_default='')
                email = db.Column(db.String(255), nullable=False, unique=True)
                email_confirmed_at = db.Column(db.DateTime())
                
                # User information
                first_name = db.Column(db.String(100), nullable=False, server_default='')
                last_name = db.Column(db.String(100), nullable=False, server_default='')
                
                posts = db.relationship('Post', backref='author', lazy=True)

                score = db.relationship('Score', backref='user', uselist=False, lazy=True)

                  # Define the relationship to Role via UserRoles
                roles = db.relationship('Role', secondary='user_roles')

                 # Define the Role data-model
        class Role(db.Model):
            __tablename__ = 'roles'
            id = db.Column(db.Integer(), primary_key=True)
            name = db.Column(db.String(50), unique=True)

        # Define the UserRoles association table
        class UserRoles(db.Model):
            __tablename__ = 'user_roles'
            id = db.Column(db.Integer(), primary_key=True)
            user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
            role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))



            #createUserPost

        class Post(db.Model):

            __tablename__ = 'post'
            
            id = db.Column(db.Integer, primary_key=True)
            #alter table Post change text text longtext;
            text = db.Column(db. String(16000000))
            date = db.Column(db.Date)
            time = db.Column(db.Time)
            
            user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
        
        
        class Score(db.Model):

            __tablename__ = 'score'
            
            id = db.Column(db.Integer, primary_key=True)
            value = db.Column(db.Integer)
            user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    
    
    

      
           
       

        # Setup Flask-User and specify the User data-model
        user_manager = UserManager(app, db, User)
            # Create all database tables
        with app.app_context():
            db.create_all()

            # Create 'member@example.com' user with no roles
            if not User.query.filter(User.email == 'member@example.com').first():
                user = User(
                    username = 'testing',
                    email='member@example.com',
                    email_confirmed_at=datetime.datetime.utcnow(),
                    password=user_manager.hash_password('Password1'),
                )
                db.session.add(user)
                db.session.commit()

            # Create 'admin@example.com' user with 'Admin' and 'Agent' roles
            if not User.query.filter(User.email == 'admin@example.com').first():
                user = User(
                    username = 'testingadmin2',
                    email='admin@example.com',
                    email_confirmed_at=datetime.datetime.utcnow(),
                    password=user_manager.hash_password('Password1'),
                )
                user.roles.append(Role(name='User'))
                user.roles.append(Role(name='Professional'))
                user.score.append(Score(value = 0))
                user.score.append(Score(value = 0))
             
                db.session.add(user)
                db.session.commit()
                # create a new post associated with the user
            
            
            
            
            class SHModelView(ModelView):
                     
                    
                     def is_accessible(self):
                        return current_user.is_authenticated

                     def inaccessible_callback(self, name, **kwargs):
                    # redirect to login page if user doesn't have access
                        return redirect(url_for('login', next=request.url))


        
            class SHAdminIndexView(AdminIndexView):
            
                def is_accessible(self):
                        return current_user.is_authenticated
                def inaccessible_callback(self, name, **kwargs):
                    # redirect to login page if user doesn't have access
                     return redirect(url_for('login', next=request.url))



            admin = Admin(app, index_view = SHAdminIndexView()) 
            admin.add_view(SHModelView(User, db.session))
            admin.add_view(SHModelView(Post, db.session))



        
        class PostForm(FlaskForm):
            post = StringField(validators=[
                                InputRequired(), Length(min=6, max=200000)], render_kw={"placeholder": "Thoughts..."})
            submit = SubmitField('Post')
            
        
        
        class RegisterForm(FlaskForm):
            username = StringField(validators=[
                                InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

            password = PasswordField(validators=[
                                    InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
            
            email = StringField(validators=[
                                    InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Email"})
            first_name = StringField(validators=[
                                    InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "First Name"})
            
            last_name = StringField(validators=[
                                    InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Last Name"})

            submit = SubmitField('Register')

            def validate_username(self, username):
                existing_user_username = User.query.filter_by(
                    username=username.data).first()
                if existing_user_username:
                    raise ValidationError(
                        'That username already exists. Please choose a different one.')
            
        class LoginForm(FlaskForm):
            username = StringField(validators=[
                                InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

            password = PasswordField(validators=[
                                    InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

            submit = SubmitField('Login')


        
        @app.route('/')
        def home():
            return render_template('home.html')

        def messageReceived(methods=['GET', 'POST']):
            print('message was received!!!')

        @socketio.on('my event')
        def handle_my_custom_event(json, methods=['GET', 'POST']):
            print('received my event: ' + str(json))
            socketio.emit('my response', json, callback=messageReceived)

        

        
        @app.route('/login', methods=['GET', 'POST'])
        def login():


            form = LoginForm()
            print(form.validate_on_submit())


            if form.validate_on_submit():
                print("hoy ")
                user = User.query.filter_by(username=form.username.data).first()
                if user:
                    if bcrypt.check_password_hash(user.password, form.password.data):
                        login_user(user)
                        return redirect(url_for('diarypage'))
            else:
                    flash('You FAILED')
                    return render_template('flask_user/login.html', form=form)
        

            return render_template('flask_user/login.html', form=form)
        
        
        @app.route('/post', methods = ['GET', 'POST'])
        @login_required
        def postNow():
               
            if request.method == "POST":

                if 'post' in request.form:
            
                        text = request.form["post"]

                        postNew = Post(text= text, date=datetime.today().date(), time=datetime.now().time(), author= current_user)
                    
                        db.session.add(postNew)
                        db.session.commit()

                   

                return render_template('diary.html')

            return render_template('diary.html')



        @app.route('/diary', methods = ['GET', 'POST'])
        @login_required
        def diarypage():
            if 'post' in request.form:
            
                        text = request.form["post"]

                        postNew = Post(text= text, date=datetime.today().date(), time=datetime.now().time(), author= current_user)
                    
                        db.session.add(postNew)
                        db.session.commit()

        
        
             
            posts = db.session.query(Post).order_by(desc(Post.id)).all()
                            
                                   
            return render_template('diary.html', posts = posts)

   


        
          
                     


        @app.route('/dashboard', methods=['GET', 'POST'])
        @login_required
        def dashboard():
            return render_template('dashboard.html')


        @app.route('/logout', methods=['GET', 'POST'])
        @login_required
        def logout():
            logout_user()
            return redirect(url_for('login'))



        @ app.route('/adminLogin', methods=['GET', 'POST'])
        def adminLogin():

            form = LoginForm()
            print(form.validate_on_submit())


            if form.validate_on_submit():
                
                user = User.query.filter_by(username=form.username.data).first()
                if user:
                    if bcrypt.check_password_hash(user.password, form.password.data):
                        if user.has_roles('Professional'):
                            login_user(user)
                            return render_template('profilebackend.html')
            else:
                    flash('You FAILED')
                    return render_template('adminLogin.html', form=form)
        

            return render_template('adminLogin.html', form=form)
        
           



        @ app.route('/register', methods=['GET', 'POST'])
        def register():
            form = RegisterForm()

            if form.validate_on_submit():
                hashed_password = bcrypt.generate_password_hash(form.password.data)
                new_user = User(username=form.username.data, password=hashed_password, first_name=form.first_name.data, last_name=form.last_name.data, email= form.email.data)
               # asignrole = UserRoles(user_id =  current_user.user_id, role_id = 2)
                role = Role.query.filter_by(name='User').one()


                new_user.roles.append(role)
                new_user.score.append(Score(value = 0))
             
                
                db.session.add(new_user) 
               
             
                db.session.commit() 
                

                return redirect(url_for('login'))

            return render_template('flask_user/register.html', form=form)




        @ app.route('/adminRegister', methods=['GET', 'POST'])
        def adminRegister():
            form = RegisterForm()

            if form.validate_on_submit():
                hashed_password = bcrypt.generate_password_hash(form.password.data)
                new_user = User(username=form.username.data, password=hashed_password, first_name=form.first_name.data, last_name=form.last_name.data, email= form.email.data)
               # asignrole = UserRoles(user_id =  current_user.user_id, role_id = 2)
                role = Role.query.filter_by(name='Professional').one()

                new_user.roles.append(role)
                
                db.session.add(new_user) 
               
             
                db.session.commit() 
                

                return redirect(url_for('adminLogin'))

            return render_template('adminRegister.html', form=form)




        # Setup Flask-User and specify the User data-model
       # user_manager = UserManager(app, db, User)


        # The Members page is only accessible to authenticated users via the @login_required decorator
        @app.route('/members')
        @login_required    # User must be authenticated
        def member_page():
                # String-based templates
                return render_template('diary.html')
                   
        
        # The Admin page requires an 'Admin' role.
        @app.route('/admin2')
        @roles_required("Professional")    # Use of @roles_required decorator
        def admin_page():

            # Flask and Flask-SQLAlchemy initialization here

           
                return render_template('main.html')
  
     
        @app.route('/profilebackend/<username>')
        
        def profilebackend(username):

            user = User.query.filter_by(username=username).first()
            posts = db.session.query(Post).filter_by(author=user).all()


            return render_template('profilebackend.html', posts = posts, username = username)

        @app.route('/profilebackend/<username>', methods=['POST'] )
        
        def postanalyze(username):
                  if request.method == "POST":
                
              
                    postid = request.form['post_id']
                    post = Post.query.get(postid)
                    input_text = post.text

                    f = open("example.txt", "w")
                    f.write(input_text)
                    # f.write(t)
                    f.close()
                    
                    
                    textP = input_text
                    calculatescore_function()
                    sentences = list(getText().sents)
                    keywords = list(detectedwords.keys())
                    negativedictionary = negativedic
                    posdictionary = positivedic
                    
                    c = plotGraph.sentenceAnalysis(getText())
                    graphP = plotGraph.plotGraphC(c)

                    sentences = list(getText().sents)
                    sentences_list = [str(s) for s in sentences]
                     # your code here
                    data = {
                        'sentences': sentences_list,
                        'keywords': keywords,
                        'negativedictionary': negativedictionary,
                        'posdictionary': posdictionary,
                        'graph': graphP
                    }

                    user = User.query.filter_by(username=username).first()
                    posts = db.session.query(Post).filter_by(author=user).all()
                    
                    print(data)
                    
                    return jsonify(data)

 
      
                




        @app.route('/professionaldashboard')
        # @login_required
        # @roles_required
        def professionaldashboard():

            users = db.session.query(User).all()

            return render_template('professionaldashboard.html', users = users)

     





        # # http://localhost:5000/profile - this will be the profile page, only accessible for loggedin users
        @app.route('/profile')
        @login_required
        def profile():
            # Check if user is loggedin

                # We need all the account info for the user so we can display it on the profile page
                 #Show the profile page with account info
                
                return render_template('profile.html')
        
        @app.route('/', methods =["GET", "POST"])
        def gfg():
            if request.method == "POST":


                if 'test' in request.form:
                 #for testing 
                 #t = generaterandomSentTest()
                 t = request.form.get("test")
                 f = open("example.txt", "w")
                 f.write(t)
                # f.write(t)
                 f.close()
                 processed_text = t
                 calculatescore_function()
                 analysedText = printSA()
                 tableText = createWordTable()

                #text_doc = getText()
                # for token in text_doc:
                    
                #         strW += token.text             
                #       #  if token.text in detectedwords.values(): 
                        #    strW += "<mark>"  + detectedwords[0][2] +"</mark>"
                        #    print(str(detectedwords))
                           #  strW += "<mark>"+ token + "</mark>"
                    
                    

                return render_template('main.html', processed_text=processed_text,analysedText = analysedText, tableText = tableText)

                
            
        
            result = request.form
            
            return render_template("main.html", result = result)
        


        @app.route('/keyword', methods =["GET", "POST"])
        def keyword():
                if request.method == "POST":

                        keywords = request.form.getlist('keyword')
                        score = request.form.getlist('score')
                        category = request.form.getlist('category')
                        
                        for k in keywords:
                            if(category == "positive"):
                            
                                print("Pos")
                            elif(category == "negative"):
                                print("Neg")
                            elif(category == "neutral"):
                                print("Neu")
                            
                                        
                        return render_template('keyword.html')


                                
                        # Code to insert the values into the database or perform any other action
                        
                    # return redirect(url_for('index'))




                                    # if 'neg' in request.form:
                                    # negativeList = request.form.get("negativeList")
                                    # f = open("negdicfile.txt", "a")
                                    # f.write(negativeList)
                                    # f.close()
                                    # f = open("negdicfile.txt", "r")   
                                    # negativedic = keywords.addnewKeyWordNegative_function(negdicfile)
                                    # addedneg = negativeList
                                    # #database
                                    # # Check if word exists using MySQL
                                    # # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                                    # # cursor.execute('SELECT * FROM keywords WHERE Word = %s', (word,))
                                    # # word = cursor.fetchone()
                                

                                    # return render_template('keyword.html', addedneg=addedneg , negativedic = negativedic)

                                
                                # getting input with name = fname in HTML form
                                    
                                # getting input with name = lname in HTML form
                                    # if 'pos' in request.form:
                                
                                    # positiveList = request.form.get("positiveList")
                                    # neutralList = request.form.get("neutralList")

                                    # f = open("posdicfile.txt", "a")
                                    # f.write(positiveList)
                                    # f.close()
                                    # f = open("posdicfile.txt", "r")
                                    # positivedic = keywords.addnewKeyWordPositive_function(posdicfile)
                                    # addedpos = positiveList

                    
                
                    
            
                result = request.form
                
                return render_template("keyword.html", result = result)
            

        





        @app.route('/evaluation', methods=['GET', 'POST'])
        def analyze():
                if request.method == "POST":
                
                    input_text = request.form["input_text"]

                    f = open("example.txt", "w")
                    f.write(input_text)
                    # f.write(t)
                    f.close()
                    textP = input_text
                    calculatescore_function()
                    sentences = list(getText().sents)
                    keywords = list(detectedwords.keys())
                    negativedictionary = negativedic
                    posdictionary = positivedic


                    
                    c = plotGraph.sentenceAnalysis(getText())
                    graphP = plotGraph.plotGraphC(c)

                    # p,n,c = sentenceAnalysis()
                    # graphP = plotGraph(p,n,c)
                
                    
                    

                    #scores = analyzeScores()
                    # analysedText = printSA()
                    # tableText = createWordTable()

                # doc = nlp(text)
                    # Perform sentiment analysis on the document here
                    # ...
                    #return {'sentiment_score': 0.8, 'word_scores': {'happy': 0.9, 'sad': 0.2}}
                    return render_template('textanalysis.html', textP = textP, sentences = sentences, keywords = keywords, negativedictionary = negativedictionary, posdictionary = posdictionary, graphP = graphP)

                return render_template('textanalysis.html')



        return app

# # http://localhost:5000/login/ - the following will be our login page, which will use both GET and POST requests
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     # Output message if something goes wrong...
#     msg = ''

#         # Check if "username" and "password" POST requests exist (user submitted form)
#     if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
#         # Create variables for easy access
#         username = request.form['username']
#         password = request.form['password']
#            # Check if account exists using MySQL
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
#         # Fetch one record and return result
#         account = cursor.fetchone()
#             # If account exists in accounts table in out database
#         if account:
#             # Create session data, we can access this data in other routes
#             session['loggedin'] = True
#             session['id'] = account['id']
#             session['username'] = account['username']
#             # Redirect to home page
#             return redirect(url_for('home'))
#         else:
#             # Account doesnt exist or username/password incorrect
#             msg = 'Incorrect username/password!'

#     return render_template('index.html', msg='')

# # http://localhost:5000/python/logout - this will be the logout page
# @app.route('/logout')
# def logout():
#     # Remove session data, this will log the user out
#    session.pop('loggedin', None)
#    session.pop('id', None)
#    session.pop('username', None)
#    # Redirect to login page
#    return redirect(url_for('login'))

# # http://localhost:5000/pythinlogin/register - this will be the registration page, we need to use both GET and POST requests
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     # Output message if something goes wrong...
#     msg = ''
#     # Check if "username", "password" and "email" POST requests exist (user submitted form)
#     if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
#         # Create variables for easy access
#         username = request.form['username']
#         password = request.form['password']
#         email = request.form['email']

#                 # Check if account exists using MySQL
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
#         account = cursor.fetchone()
#         # If account exists show error and validation checks
#         if account:
#             msg = 'Account already exists!'
#         elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
#             msg = 'Invalid email address!'
#         elif not re.match(r'[A-Za-z0-9]+', username):
#             msg = 'Username must contain only characters and numbers!'
#         elif not username or not password or not email:
#             msg = 'Please fill out the form!'
#         else:
#             # Account doesnt exists and the form data is valid, now insert new account into accounts table
#             cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email,))
#             query = "SELECT id FROM users WHERE username = ' "+ username+"';"
#             cursor.execute(query)
#             id = cursor.fetchone()[0]

#             cursor.execute('INSERT INTO user_roles VALUES (%i, %i)', (id, 1,))
            
#             mysql.connection.commit()
#             msg = 'You have successfully registered!'
#     elif request.method == 'POST':
#         # Form is empty... (no POST data)
#         msg = 'Please fill out the form!'
#     # Show registration form with message (if any)
#     return render_template('register.html', msg=msg)

#     #https://codeshack.io/login-system-python-flask-mysql/


# # http://localhost:5000/pythinlogin/home - this will be the home page, only accessible for loggedin users
# @app.route('/home')
# def home():
#     # Check if user is loggedin
#     if 'loggedin' in session:
#         # User is loggedin show them the home page
#         return render_template('home.html', username=session['username'])
#     # User is not loggedin redirect to login page
#     return redirect(url_for('login'))

# # A decorator used to tell the application
# # which URL is associated function

# # http://localhost:5000/profile - this will be the profile page, only accessible for loggedin users
# @app.route('/profile')
# def profile():
#     # Check if user is loggedin
#     if 'loggedin' in session:
#         # We need all the account info for the user so we can display it on the profile page
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
#         account = cursor.fetchone()
#         # Show the profile page with account info
#         return render_template('profile.html', account=account)
#     # User is not loggedin redirect to login page
#     return redirect(url_for('login'))

# #@app.route('/main/<name>')
# def hello(name=None):
#     return render_template('main.html', name=name)


#@app.route('/', methods =["GET", "POST"])
# def gfg():
#     if request.method == "POST":


#         if 'test' in request.form:
#          #for testing 
#          #t = generaterandomSentTest()
#          t = request.form.get("test")
#          f = open("example.txt", "w")
#          f.write(t)
#         # f.write(t)
#          f.close()
#          processed_text = t
#          calculatescore_function()
#          analysedText = printSA()
#          tableText = createWordTable()

#         #text_doc = getText()
#         # for token in text_doc:
              
#         #         strW += token.text             
#         #       #  if token.text in detectedwords.values(): 
#                 #    strW += "<mark>"  + detectedwords[0][2] +"</mark>"
#                 #    print(str(detectedwords))
#                    #  strW += "<mark>"+ token + "</mark>"
            
              

#         return render_template('main.html', processed_text=processed_text,analysedText = analysedText, tableText = tableText)

        
       
   
#     result = request.form
      
#     return render_template("main.html", result = result)
 

# @app.route('/keyword', methods =["GET", "POST"])
# def keyword():
#     if request.method == "POST":

#             keywords = request.form.getlist('keyword')
#             score = request.form.getlist('score')
#             category = request.form.getlist('category')
            
#             for k in keywords:
#                 if(category == "positive"):
                  
#                   print("Pos")
#                 elif(category == "negative"):
#                   print("Neg")
#                 elif(category == "neutral"):
#                   print("Neu")
            
                            
#             return render_template('keyword.html')


                     
#             # Code to insert the values into the database or perform any other action
            
#            # return redirect(url_for('index'))




#                         # if 'neg' in request.form:
#                         # negativeList = request.form.get("negativeList")
#                         # f = open("negdicfile.txt", "a")
#                         # f.write(negativeList)
#                         # f.close()
#                         # f = open("negdicfile.txt", "r")   
#                         # negativedic = keywords.addnewKeyWordNegative_function(negdicfile)
#                         # addedneg = negativeList
#                         # #database
#                         # # Check if word exists using MySQL
#                         # # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#                         # # cursor.execute('SELECT * FROM keywords WHERE Word = %s', (word,))
#                         # # word = cursor.fetchone()
                    

#                         # return render_template('keyword.html', addedneg=addedneg , negativedic = negativedic)

                    
#                     # getting input with name = fname in HTML form
                        
#                     # getting input with name = lname in HTML form
#                         # if 'pos' in request.form:
                    
#                         # positiveList = request.form.get("positiveList")
#                         # neutralList = request.form.get("neutralList")

#                         # f = open("posdicfile.txt", "a")
#                         # f.write(positiveList)
#                         # f.close()
#                         # f = open("posdicfile.txt", "r")
#                         # positivedic = keywords.addnewKeyWordPositive_function(posdicfile)
#                         # addedpos = positiveList

        
      
        
   
#     result = request.form
      
#     return render_template("keyword.html", result = result)
 

 
# @app.route('/evaluation', methods=['GET', 'POST'])
# def analyze():
#     if request.method == "POST":
     
#         input_text = request.form["input_text"]

#         f = open("example.txt", "w")
#         f.write(input_text)
#         # f.write(t)
#         f.close()
#         textP = input_text
#         calculatescore_function()
#         sentences = list(getText().sents)
#         keywords = list(detectedwords.keys())
#         negativedictionary = negativedic
#         posdictionary = positivedic


        
#         c = plotGraph.sentenceAnalysis(getText())
#         graphP = plotGraph.plotGraphC(c)

#         # p,n,c = sentenceAnalysis()
#         # graphP = plotGraph(p,n,c)
       
        
        

#         #scores = analyzeScores()
#         # analysedText = printSA()
#         # tableText = createWordTable()

#        # doc = nlp(text)
#         # Perform sentiment analysis on the document here
#         # ...
#         #return {'sentiment_score': 0.8, 'word_scores': {'happy': 0.9, 'sad': 0.2}}
#         return render_template('textanalysis.html', textP = textP, sentences = sentences, keywords = keywords, negativedictionary = negativedictionary, posdictionary = posdictionary, graphP = graphP)

#     return render_template('textanalysis.html')

if __name__=='__main__':
    app = create_app()
    app.run()
    #socketio.run(app, debug=True)
