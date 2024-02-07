from flask import Flask, render_template, flash, jsonify
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
from flask_cors import CORS


 
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

#Testing Database API
@app.route('/')
def top_actors():
    # Execute SQL query to get top 5 actors
    with engine.connect() as connection:
        sql_query_top_actos = text("""
            SELECT actor.actor_id, actor.first_name, actor.last_name, COUNT(*) AS film_count
            FROM actor
            JOIN film_actor ON actor.actor_id = film_actor.actor_id
            GROUP BY actor.actor_id, actor.first_name, actor.last_name
            ORDER BY film_count DESC
            LIMIT 5;
        """)
        result_top_actors = connection.execute(sql_query_top_actos)
        top_actors = result_top_actors.fetchall()

    # Execute SQL query to get top 5 films
    with engine.connect() as connection:
        sql_query_top_films = text("""
            select f.film_id, f.title, count(r.rental_id) as rental_count
            from film as f
            join  film_category as fc on f.film_id = fc.film_id
            join category as c on fc.category_id = c.category_id
            join inventory as i on i.film_id = f.film_id
            join rental as r on r.inventory_id = i.inventory_id
            group by f.film_id, f.title, c.name 
            order by rental_count desc
            limit 5;
        """)
        result_top_films = connection.execute(sql_query_top_films)
        top_films = result_top_films.fetchall()

    # Execute SQL query to get List of all Customers
    with engine.connect() as connection:
        sql_query_customers = text("""
            select cu.customer_id, cu.first_name, cu.last_name, count(r.rental_id) as rental_count
            from customer as cu
            join rental as r on r.customer_id = cu.customer_id
            group by cu.customer_id, cu.first_name, cu.last_name
            order by cu.customer_id asc;
        """)
        customers = connection.execute(sql_query_customers)
        customer_list = customers.fetchall()


    return render_template('top_actors.html', top_actors=top_actors, top_films=top_films, 
                           customer_list=customer_list)


#HOME PAGE-----------------------------------------------------
#Top 5 Movie for home page
@app.route("/home_page")
def top_films():
    # Execute SQL query to get top 5 films
    with engine.connect() as connection:
        sql_query_top_films = text("""
            select 
                f.film_id, f.title, 
                count(r.rental_id) as rental_count, 
                f.description, f.release_year, 
                f.rating,    
                ROUND(AVG(py.amount), 2) AS average_rental_cost
            from film as f
            join  film_category as fc on f.film_id = fc.film_id
            join category as c on fc.category_id = c.category_id
            join inventory as i on i.film_id = f.film_id
            join rental as r on r.inventory_id = i.inventory_id
            join payment as py on py.rental_id = r.rental_id
            group by f.film_id, f.title, c.name 
            order by rental_count desc
            limit 5;
        """)
        
        result_top_films = connection.execute(sql_query_top_films)
        top_films = result_top_films.fetchall()
    return render_template('top_actors.html', top_films=top_films)


#Top 5 actors for home page
def top_actors():
    # Execute SQL query to get top 5 actors
    with engine.connect() as connection:
        sql_query_top_actos = text("""
            SELECT actor.actor_id, actor.first_name, actor.last_name, COUNT(*) AS film_count
            FROM actor
            JOIN film_actor ON actor.actor_id = film_actor.actor_id
            GROUP BY actor.actor_id, actor.first_name, actor.last_name
            ORDER BY film_count DESC
            LIMIT 5;
        """)
        result_top_actors = connection.execute(sql_query_top_actos)
        top_actors = result_top_actors.fetchall()

    return render_template('top_actors.html', top_actors=top_actors)


#MOVIES PAGE--------------------------------------------------



#CUSTOMERS PAGE-----------------------------------------------

#Customer Lookup and Info Page
@app.route("/customers", methods=['GET', 'POST'])
def customers():
    # Execute SQL query to get List of all Customers
    with engine.connect() as connection:
        sql_query_customers = text("""
            select cu.customer_id, cu.first_name, cu.last_name, count(r.rental_id) as rental_count
            from customer as cu
            join rental as r on r.customer_id = cu.customer_id
            group by cu.customer_id, cu.first_name, cu.last_name
            order by cu.customer_id asc;
        """)
        customers = connection.execute(sql_query_customers)
        customer_list = customers.fetchall()
    return render_template('customers.html', customer_list=customers)

#REPORT PAGE-------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
CORS(app)


    
