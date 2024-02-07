from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime    
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import inspect

 
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

# Define SQLAlchemy engine and session
engine = create_engine('mysql+pymysql://root:0725@127.0.0.1/sakila') 

# 1. Create MetaData object
metadata = MetaData()

# 2. Bind MetaData to the engine
metadata.reflect(bind=engine)

# 3. Automap Base
Base = automap_base(metadata=metadata)
Base.prepare()

# 4. Access tables
Actor = Base.classes.actor
Address = Base.classes.address
Category = Base.classes.category
City = Base.classes.city
Country = Base.classes.country
Customer = Base.classes.customer
Film = Base.classes.film
Film_Actor = Base.classes.film_actor
Film_Category = Base.classes.film_category
Film_Text = Base.classes.film_text
Inventory = Base.classes.inventory
Language = Base.classes.language
Payment = Base.classes.payment
Rental = Base.classes.rental
Staff = Base.classes.staff
Store = Base.classes.store

# 5. Create session
Session = sessionmaker(bind=engine)
session = Session()

# 6. Query data
actors = session.query(Actor).all()

# 7. Example manipulation
for actor in actors:
    print(actor.actor_id, actor.first_name, actor.last_name)



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
def actors():
    # Reflect the actor table using metadata
    actor_table = metadata.tables['actor']

    # Execute a raw SQL query to select all columns from the actor table
    with engine.connect() as connection:
        result = connection.execute(actor_table.select())
        actors = result.fetchall()

    return render_template('actors.html', actors=actors)

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


    
