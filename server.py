from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Geometry
from datetime import datetime    
 
#Create Flask Instance
app = Flask(__name__)

#Add Database
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
#MySQL db
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:0725@127.0.0.1/sakila'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


#Secret Key
app.config['SECRET_KEY'] = "password"

#Initialized The Database
db = SQLAlchemy(app)

#In Context
app.app_context().push()

#Create Model
class Users(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

#EXAMPLE TO COPY FROM :)
class Sock(db.Model):
    __tablename__ = 'socks'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String)
    style = db.Column(db.String)
    color = db.Column(db.String)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    updated = db.Column(db.String)

#Actor Table
class Actors(db.Model):
    __tablename__ = 'actor'
    actor_id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    first_name = db.Column(db.String(45))
    last_name = db.Column(db.String(45))
    last_update = db.Column(db.String)

#Address Table
class Address(db.Model):
    __tablename__ = 'address'
    address_id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    address = db.Column(db.String(50))
    address2 = db.Column(db.String(50))
    district = db.Column(db.String(20))
    city_id = db.Column(db.Integer, unique=True)
    postal_code = db.Column(db.String(10))
    phone = db.Column(db.String(20))

    last_update = Column(DateTime, default=func.now())  # Timestamp column with default value of current time


#Category Table
class Sock(db.Model):
    __tablename__ = 'socks'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String)
    style = db.Column(db.String)
    color = db.Column(db.String)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    updated = db.Column(db.String)

#City Table
class Sock(db.Model):
    __tablename__ = 'socks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    style = db.Column(db.String)
    color = db.Column(db.String)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    updated = db.Column(db.String)

#Country Table
class Sock(db.Model):
    __tablename__ = 'socks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    style = db.Column(db.String)
    color = db.Column(db.String)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    updated = db.Column(db.String)

#Customer Table
class Sock(db.Model):
    __tablename__ = 'socks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    style = db.Column(db.String)
    color = db.Column(db.String)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    updated = db.Column(db.String)

#Film Table
class Sock(db.Model):
    __tablename__ = 'socks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    style = db.Column(db.String)
    color = db.Column(db.String)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    updated = db.Column(db.String)

#Film_Actor Table
class Sock(db.Model):
    __tablename__ = 'socks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    style = db.Column(db.String)
    color = db.Column(db.String)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    updated = db.Column(db.String)

#Film_Category Table
class Sock(db.Model):
    __tablename__ = 'socks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    style = db.Column(db.String)
    color = db.Column(db.String)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    updated = db.Column(db.String)

#Film_Text Table
class Sock(db.Model):
    __tablename__ = 'socks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    style = db.Column(db.String)
    color = db.Column(db.String)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    updated = db.Column(db.String)

#Inventory Table
class Sock(db.Model):
    __tablename__ = 'socks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    style = db.Column(db.String)
    color = db.Column(db.String)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    updated = db.Column(db.String)

#Language Table
class Sock(db.Model):
    __tablename__ = 'socks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    style = db.Column(db.String)
    color = db.Column(db.String)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    updated = db.Column(db.String)

#Payment Table
class Sock(db.Model):
    __tablename__ = 'socks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    style = db.Column(db.String)
    color = db.Column(db.String)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    updated = db.Column(db.String)

#Rental Table
class Sock(db.Model):
    __tablename__ = 'socks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    style = db.Column(db.String)
    color = db.Column(db.String)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    updated = db.Column(db.String)

#Staff Table
class Sock(db.Model):
    __tablename__ = 'socks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    style = db.Column(db.String)
    color = db.Column(db.String)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    updated = db.Column(db.String)

#Store Table
class Sock(db.Model):
    __tablename__ = 'socks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    style = db.Column(db.String)
    color = db.Column(db.String)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    updated = db.Column(db.String)





    #Create String
    def __repr__(self):
        return '<Name %r>' % self.name 

#Create Form Class
class CustomerAddForm(FlaskForm):
    name = StringField("Customer Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")

#Create Form Class
class CustomerNameForm(FlaskForm):
    name = StringField("Customer Name", validators=[DataRequired()])
    submit = SubmitField("Submit")

#Landing Page API route
@app.route("/")

#def index():
#    return "<h1>Hello World!</h1>"

def index():
    return render_template("index.html")

#Add a Customer 
@app.route("/customers/add", methods=['GET', 'POST'])

def add_customer():
    name = None
    form = CustomerAddForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        flash("User Added Successfully")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_customer.html", form=form, name=name, our_users=our_users) 

#Move Search Page
@app.route("/movies")

def movies():
    return render_template("movies.html")

#Customer Lookup and Info Page
@app.route("/customers", methods=['GET', 'POST'])

def customers():
    name = None
    form = CustomerNameForm()
    #Form Validation
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = '' 
        flash("Form Submitted Successfully")
        
    return render_template("customers.html", name = name, form = form)

#Full Customer Report Page
@app.route("/report")

def report():
    return render_template("report.html")

#Members API route
@app.route("/members")
def members():
    return{"members": ["Member1", "Member2", "Member3"]}

if __name__ == "__main__":
    app.run(debug=True)


    
