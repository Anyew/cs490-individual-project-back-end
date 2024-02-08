from flask import Flask, request, render_template, flash, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func, ForeignKey, Numeric, Table
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime    
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import inspect
from flask_cors import CORS
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

 
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

#Testing Database API
'''@app.route('/')
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


    return (jsonify(customer_list, top_films, top_actors))
'''

# HOME PAGE -----------------------------------------------------
# Top 5 Movie for home page
@app.route("/top_films")
def top_films():
    try:
        # Execute SQL query to get top 5 films
        with engine.connect() as connection:
            sql_query_top_films = text("""
                SELECT 
                    f.film_id, 
                    f.title, 
                    COUNT(r.rental_id) AS rental_count, 
                    f.description, 
                    f.release_year, 
                    f.rating,    
                    ROUND(AVG(py.amount), 2) AS average_rental_cost
                FROM film AS f
                JOIN film_category AS fc ON f.film_id = fc.film_id
                JOIN category AS c ON fc.category_id = c.category_id
                JOIN inventory AS i ON i.film_id = f.film_id
                JOIN rental AS r ON r.inventory_id = i.inventory_id
                JOIN payment AS py ON py.rental_id = r.rental_id
                GROUP BY f.film_id, f.title, c.name 
                ORDER BY rental_count DESC
                LIMIT 5;
            """)
            
            result_top_films = connection.execute(sql_query_top_films)
            top_films = []
            for row in result_top_films.fetchall():
                film_dict = {
                    "film_id": row[0],
                    "title": row[1],
                    "rental_count": row[2],
                    "description": row[3],
                    "release_year": row[4],
                    "rating": row[5],
                    "average_rental_cost": row[6]
                }
                top_films.append(film_dict)

        return jsonify(top_films)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/top_actors")
#Top 5 actors for home page
def top_actors():
    # Execute SQL query to get top 5 actors
    try:
        with engine.connect() as connection:
            sql_query_top_actors = text("""
                SELECT 
                    actor.actor_id, 
                    actor.first_name, 
                    actor.last_name, 
                    COUNT(*) AS film_count
                FROM actor
                JOIN film_actor ON actor.actor_id = film_actor.actor_id
                GROUP BY actor.actor_id, actor.first_name, actor.last_name
                ORDER BY film_count DESC
                LIMIT 5;
            """)
            result_top_actors = connection.execute(sql_query_top_actors)
            top_actors = []
            for row in result_top_actors.fetchall():
                actor_dict = {
                    "actor_id": row[0],
                    "first_name": row[1],
                    "last_name": row[2],
                    "film_count": row[3],
                }
                top_actors.append(actor_dict)

        return(jsonify(top_actors))
    except Exception as e:
            return jsonify({"error": str(e)})          

#MOVIES PAGE--------------------------------------------------
film_actor = db.Table(
    'film_actor',
    db.Column('film_id', db.Integer, db.ForeignKey('film.film_id')),
    db.Column('actor_id', db.Integer, db.ForeignKey('actor.actor_id'))
)

film_category = db.Table(
    'film_category',
    db.Column('film_id', db.Integer, db.ForeignKey('film.film_id')),
    db.Column('category_id', db.Integer, db.ForeignKey('category.category_id'))
)
class Film(db.Model):
    __tablename__ = 'film'

    film_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.Text)
    release_year = db.Column(db.Integer)
    rental_rate = db.Column(db.Numeric(4, 2))
    length = db.Column(db.Integer)

    # Define the many-to-many relationship with Actor and Category
    actors = db.relationship('Actor', secondary='film_actor', backref='films')
    categories = db.relationship('Category', secondary='film_category', backref='films')

class Actor(db.Model):
    __tablename__ = 'actor'

    actor_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45))
    last_name = db.Column(db.String(45))

class Category(db.Model):
    __tablename__ = 'category'

    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))

@app.route('/search', methods=['GET'])
def search_movies():
    query = request.args.get('query')
    session = Session()
    try:
        results = session.query(Film).filter(
            (Film.title.ilike(f'%{query}%')) |
            (Film.actors.any(Actor.first_name.ilike(f'%{query}%'))) |
            (Film.actors.any(Actor.last_name.ilike(f'%{query}%'))) |
            (Film.categories.any(Category.name.ilike(f'%{query}%')))
        ).all()
        return jsonify([{
            'film_id': result.film_id,
            'title': result.title,
            'description': result.description,
            'release_year': result.release_year,
            'rental_rate': float(result.rental_rate),
            'length': result.length,
            'actors': [{'first_name': actor.first_name, 'last_name': actor.last_name} for actor in result.actors],
            'categories': [category.name for category in result.categories]
        } for result in results])
    finally:
        session.close()


#CUSTOMERS PAGE-----------------------------------------------

class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    # Add more customer attributes as needed

# Route to fetch all customers with pagination support
@app.route('/api/customers')
def get_customers():
    # Get query parameters for filtering
    customer_id = request.args.get('customer_id')
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')

    # Construct the base query
    query = Customer.query

    # Filter customers based on query parameters
    if customer_id:
        query = query.filter(Customer.customer_id == customer_id)
    if first_name:
        query = query.filter(Customer.first_name.ilike(f'%{first_name}%'))
    if last_name:
        query = query.filter(Customer.last_name.ilike(f'%{last_name}%'))

    # Execute the query to get filtered customers
    customers = query.all()

    # Construct response data
    customer_data = []
    for customer in customers:
        customer_data.append({
            'customer_id': customer.customer_id,
            'first_name': customer.first_name,
            'last_name': customer.last_name
            # Add more attributes if needed
        })

    return jsonify({'customers': customer_data})

#REPORT PAGE-------------------------------------------------





#END________________________________________________________________
if __name__ == "__main__":
    app.run(debug=True)
CORS(app)


    
