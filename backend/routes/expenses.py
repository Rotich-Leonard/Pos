from flask import Blueprint, request, jsonify
from datetime import datetime
from models import connect_db

expenses_bp = Blueprint('expenses', __name__)

@expenses_bp.route('/', methods=['POST'])
def add_expense():
    data = request.get_json()
    con = connect_db()
    con.execute("INSERT INTO expenses (description, amount, exp_date) VALUES (?, ?, ?)",
                (data['description'], data['amount'], datetime.now().isoformat()))
    con.commit()
    return jsonify({"msg": "Expense added"}), 201

@expenses_bp.route('/', methods=['GET'])
def get_expenses():
    start = request.args.get('start')
    end = request.args.get('end')

    con = connect_db()
    query = "SELECT * FROM expenses WHERE 1=1"
    args = []
    if start and end:
        query += " AND exp_date BETWEEN ? AND ?"
        args.extend([start, end])
    cur = con.execute(query, args)
    return jsonify([dict(row) for row in cur.fetchall()])