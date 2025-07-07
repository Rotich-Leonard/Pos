from flask import Blueprint, request, jsonify
from models import connect_db

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/financial', methods=['GET'])
def financial_summary():
    start = request.args.get('start')
    end = request.args.get('end')
    args = []

    sales_query = "SELECT SUM(total_price) AS total_sales FROM sales WHERE 1=1"
    expense_query = "SELECT SUM(amount) AS total_expenses FROM expenses WHERE 1=1"

    if start and end:
        sales_query += " AND trans_date BETWEEN ? AND ?"
        expense_query += " AND exp_date BETWEEN ? AND ?"
        args.extend([start, end])

    con = connect_db()
    sales_total = con.execute(sales_query, args).fetchone()['total_sales'] or 0
    expense_total = con.execute(expense_query, args).fetchone()['total_expenses'] or 0
    profit = sales_total - expense_total

    return jsonify({
        "total_sales": sales_total,
        "total_expenses": expense_total,
        "profit": profit
    })

@reports_bp.route('/inventory_value', methods=['GET'])
def inventory_value():
    con = connect_db()
    cur = con.execute("SELECT SUM(price * quantity) AS total_inventory_value FROM products")
    val = cur.fetchone()['total_inventory_value'] or 0
    return jsonify({"inventory_value": val})