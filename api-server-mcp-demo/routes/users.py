"""
User-related API routes
"""
from flask import Blueprint, request, jsonify
from utils.db_helper import query_db

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('/', methods=['GET'])
def get_users():
    """
    Get all users or search by criteria
    Query params: name, user_id, email
    """
    name = request.args.get('name')
    user_id = request.args.get('user_id')
    email = request.args.get('email')
    
    if user_id:
        user = query_db(
            'SELECT * FROM users WHERE user_id = ?',
            (user_id,),
            one=True
        )
        if user:
            return jsonify(user)
        return jsonify({"error": "User not found"}), 404
    
    elif email:
        user = query_db(
            'SELECT * FROM users WHERE email = ?',
            (email,),
            one=True
        )
        if user:
            return jsonify(user)
        return jsonify({"error": "User not found"}), 404
    
    elif name:
        users = query_db(
            'SELECT * FROM users WHERE name LIKE ?',
            (f'%{name}%',)
        )
        if users:
            return jsonify(users)
        return jsonify({"error": "No users found"}), 404
    
    else:
        users = query_db('SELECT * FROM users LIMIT 100')
        return jsonify(users)

@users_bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get user by ID"""
    user = query_db(
        'SELECT * FROM users WHERE user_id = ?',
        (user_id,),
        one=True
    )
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404