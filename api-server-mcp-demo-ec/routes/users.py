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
    ---
    parameters:
      - name: name
        in: query
        type: string
        required: false
        description: Search users by name (case-insensitive partial match)
      - name: email
        in: query
        type: string
        required: false
        description: Filter users by email (case-insensitive exact match)
    responses:
      200:
        description: List of users
        schema:
          type: array
          items:
            type: object
            properties:
              user_id:
                type: string
              name:
                type: string
              email:
                type: string
      404:
        description: No users found
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
    """
    Get user by ID
    ---
    parameters:
      - name: user_id
        in: path
        type: string
        required: true
        description: The user ID
    responses:
      200:
        description: User details
        schema:
          type: object
          properties:
            user_id:
              type: string
            name:
              type: string
            email:
              type: string
      404:
        description: User not found
    """
    user = query_db(
        'SELECT * FROM users WHERE user_id = ?',
        (user_id,),
        one=True
    )
    if user:
        return success_response(user)
    return not_found_response("User")