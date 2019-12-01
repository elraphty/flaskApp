from flask import Flask, render_template, flash, session, redirect, url_for, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, SelectField, PasswordField, TextAreaField, validators, StringField
from passlib.hash import sha256_crypt
from data import Articles

app = Flask(__name__)

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Elraphty1'
app.config['MYSQL_DB'] = 'myflaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MYSQL
mysql = MySQL(app)

Articles = Articles()

# Index
@app.route('/')
def index():
    return render_template('index.html')

# About 
@app.route('/about')
def about():
    return render_template('about.html')

# Get Articles
@app.route('/articles')
def articles():
    return render_template('articles.html', articles = Articles)

#Single Articles
@app.route('/article/<string:id>/')
def article(id):
    return render_template('article.html', id=id)

# User Register Form Class
class RegisterForm(Form):
    name = StringField(u'Name', validators=[validators.input_required(), validators.Length(min=1, max=50 )])
    username  = StringField(u'Username', validators=[validators.Length(min=4, max=25 )])
    email = StringField(u'Email', validators=[validators.input_required(), validators.Length(min=6, max=50 )])
    password = PasswordField('Password', validators=[
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('index'))
    return render_template('register.html', form=form)

if __name__ == '__main__':
    app.secret_key='elraphtySECRET12345690'
    app.run(debug=True)