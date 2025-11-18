"""
User-related API routes
"""
from flask import Blueprint, request
from utils.db_helper import query_db
from utils.response_helper import (
    success_response,
    not_found_response,
    no_results_response,
    validate_and_respond
)

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('/', methods=['GET'])
def get_users():
    """
    Get all users or search by criteria
    Query params: name, email
    """
    name = request.args.get('name')
    email = request.args.get('email')

    if email:
        user = query_db(
            'SELECT * FROM users WHERE LOWER(email) = LOWER(?)',
            (email,),
            one=True
        )
        if user:
            return success_response(user)
        return not_found_response("User")

    elif name:
        users = query_db(
            'SELECT * FROM users WHERE LOWER(name) LIKE LOWER(?)',
            (f'%{name}%',)
        )
        if not users:
            return no_results_response("users")
        return success_response(users)

    else:
        users = query_db('SELECT * FROM users LIMIT 100')
        return success_response(users)

@users_bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get user by ID"""
    user = query_db(
        'SELECT * FROM users WHERE user_id = ?',
        (user_id,),
        one=True
    )
    if user:
        return success_response(user)
    return not_found_response("User")