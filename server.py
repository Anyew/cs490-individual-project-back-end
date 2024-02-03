from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from datetime import datetime
 
#Create Flask Instance
app = Flask(__name__)

#Add Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

#Secret Key
app.config['SECRET_KEY'] = "password"

#Initialized The Database
db = SQLAlchemy(app)

#Create Model
class Users(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    #Create String
    def __repr__(self):
        return '<Name %r>' % self.name 



#Create Form Class
class CustomerNameForm(FlaskForm):
    name = StringField("Customer Name", validators=[DataRequired()])
    submit = SubmitField("Submit")

#Create Database Within Context
with app.app_context():
    db.create_all()

#Landing Page API route
@app.route("/")

#def index():
#    return "<h1>Hello World!</h1>"

def index():
    return render_template("index.html")

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


    
