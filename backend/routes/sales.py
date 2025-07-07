from flask import Blueprint, request, jsonify
from datetime import datetime
from models import connect_db

sales_bp = Blueprint('sales', __name__)

@sales_bp.route('/', methods = ['POST'])
def make_sale():
    data = request.get_json()
    con = connect_db()
    cur = con.execute("SELECT * FROM products WHERE id=?", (data['product_id'],))
    product = cur.fetchone()
    if not product or product['quantity'] < data['quantity']:
        return jsonify({"msg": "Not Enough Stock"}), 400
    
    total_price = product['price'] * data['quantity']
    con.execute("INSERT INTO sales (product_id, quantity, total_price, payment_type, trans_date) VALUES (?, ?, ?, ?, ?)",
                (data['product_id'], data['quantity'], total_price, data['payment_type'], datetime.now().isoformat()))
    con.execute("UPDATE products SET quantity = quantity - ? WHERE id=?",
                (data['quantity'], data['product_id']))
    con.commit()
    return jsonify({"msg": "Sale completed", "total": total_price})

@sales_bp.route('/', methods=['GET'])
def get_sales():
    payment_type = request.args.get('payment_type')
    start_date = request.args.get('start')
    end_date = request.args.get('end')

    con = connect_db()
    query = "SELECT * FROM sales WHERE 1=1"
    args = []

    if payment_type:
        query += " AND payment_type=?"
        args.append(payment_type)
    if start_date and end_date:
        query += " AND trans_date BETWEEN ? AND ?"
        args.extend([start_date, end_date])

    cur = con.execute(query, args)
    return jsonify([dict(row) for row in cur.fetchall()])

    