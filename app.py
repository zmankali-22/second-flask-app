

from flask import Flask

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)



app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://practice_dev:123456@localhost:5432/practice_database"
db = SQLAlchemy(app)

class Product(db.Model):

    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)

    name= db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(1000))



@app.cli.command("create")
def create_table():
    db.create_all()
    print("Table created")

@app.cli.command("seed")
def seed_db():

    # Create a product table

    product1 = Product(name="product1", price=100, stock=100, description="This is product 1")
    product2 = Product(name="product2", price=200, stock=200, description ="This is product 2 which is a blast product")

    db.session.add(product1)
    db.session.add(product2)
    db.session.commit()
    print("Table seeded")

@app.cli.command("drop")
def drop_table():
    db.drop_all()
    print("Table dropped")  

