

from flask import Flask, request

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)



app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://practice_dev:123456@localhost:5432/practice_database"
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Product(db.Model):

    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)

    name= db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(1000))

class ProductSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "price", "stock", "description")


# handle all products
products_schema = ProductSchema(many=True)


#  handle singlr prodcuts

product_schema = ProductSchema(many=False)

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


@app.route("/products")
def get_products():
    stmt = db.select(Product)
    product_list = db.session.scalars(stmt)
    # non serializable to json
    data = products_schema.dump(product_list)
    return data

@app.route("/products/<int:product_id>")
def get_product(product_id):
    stmt = db.select(Product).filter_by(id=product_id)
    product = db.session.scalar(stmt)
    # non serializable to json

    if(product):

        data = product_schema.dump(product)
        return data
    else:
        return {"message": "Product not found"}, 404
    
@app.route("/products", methods=["POST"])
def create_product():
    product_fileds = request.get_json()
    new_product = Product(name = product_fileds.get("name"), price = product_fileds.get("price"), stock = product_fileds.get("stock"), description = product_fileds.get("description"))
    db.session.add(new_product)
    db.session.commit()
    data = product_schema.dump(new_product)
    return data, 201
