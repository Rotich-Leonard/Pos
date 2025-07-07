import os
class config: #configering class for security key and path to SQLite db
    SECRET_KEY = os.environ.get('SECRET_KEY', 'my-secret-key')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret')
    DATABASE = os.path.join(os.getcwd(), 'database', 'pos.db')
    