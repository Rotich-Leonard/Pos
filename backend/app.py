#importing libraries
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS 
from config import Config 
import os

app = Flask(_name_)
app.config.from_object(config)

jwt = JWTManager(app)
CORS(app)

from auth import auth_bp
from routes.products import products_bp
from routes.sales import sales_bp
from routes.expenses import expenses_bp
from routes.reports import reports_bp

app.register_blueprint(auth_bp)
app.register_blueprint(products_bp, url_prefix='/products')
app.register_blueprint(sales_bp, url_prefix='/sales')
app.register_blueprint(expenses, url_prefix='expenses')
app.register_blueprint(reports_bp, url_prefix='/reports')

if _name_ == '_main_':
    if not os.path.exists(Config.DATABASE):
        from models import init_db
        init_db()
    app.run(debug = True)