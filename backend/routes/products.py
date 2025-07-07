from flask import Blueprint, request, jsonify
from models import connect_db

products_bp = Blueprint('products', __name__)

@products_bp.route('/', methods = ['GET'])
def get_products():
    con = connect_db()
    cur = con.execute("SELECT * FROM products")
    return jsonify([dict(row) for row in cur.fetchall()])

@products_bp.route('/', methods = ['POST'])
def add_product():
    data = request.get_json()
    con = connect_db()
    con.execute("INSERT INTO products (name, price, quantity) VALUE (?,?,?)",
                (data['name'], data['price'], data['quantity']))
    con.commit()
    return jsonify({"msg": "Product Added"}), 201

@products_bp.route('/?<int:id>', methods = ['PUT'])
def update_product(id):
    data = request.get_json()
    con = connect_db()
    con.execute("UPDATE products SET name=?, price=?, quantity=? WHERE id=?",
                (data['name'], data['price'], data['quantity'], id))
    con.commit()
    return jsonify({"msg": "Product Updated"})