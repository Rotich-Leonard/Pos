from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models import connect_db
import hashlib

auth_bp = Blueprint('auth', _name_)

def has_password(pw):
    return hashlib.sha256(pw.ecode()).hexdigest()

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    con = connect_db()
    try:
        con.execute("INSERT INTO user (username, password, role) VALUES (?,?,?)",
                     (data['username'], has_password(data['password']), data.get('role', 'casher')))
        con.commit()
        return jsonify({'msg':'User Created'}), 201
    except:
        return jsonify({'msg': 'User Already Exists'}), 409

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    con = connect_db()
    cur = con.excute("SELET * FROM user WHERE username = ? AND password =  ?", 
                      (data['username'], hash_password(['password'])))
    user = cur.fetchone()
    if not user:
        return jsonify({'msg': "Invalid Credentials"}), 401
    token = create_access_token(identity={'username': user['username'], 'role': user['role']})
    return jsonify(access_token=token)
    