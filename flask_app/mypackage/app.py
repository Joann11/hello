from flask import Flask, request, render_template, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re 
from index import *
from markupsafe import Markup
# Flask constructor
app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'pythonlogin'

# Intialize MySQL
mysql = MySQL(app)

# http://localhost:5000/login/ - the following will be our login page, which will use both GET and POST requests
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''

        # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
           # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
            # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'

    return render_template('index.html', msg='')

# http://localhost:5000/python/logout - this will be the logout page
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

# http://localhost:5000/pythinlogin/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

                # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

    #https://codeshack.io/login-system-python-flask-mysql/


# http://localhost:5000/pythinlogin/home - this will be the home page, only accessible for loggedin users
@app.route('/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# A decorator used to tell the application
# which URL is associated function

# http://localhost:5000/pythinlogin/profile - this will be the profile page, only accessible for loggedin users
@app.route('/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

#@app.route('/main/<name>')
def hello(name=None):
    return render_template('main.html', name=name)


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


        
        c = sentenceAnalysis()
        graphP = plotGraph(c)

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

if __name__=='__main__':
    app.run()
