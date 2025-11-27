"""
Response helper functions for standardized API responses
"""
from flask import jsonify


def success_response(data, status_code=200):
    """
    Return a standardized success response

    Args:
        data: The response data (dict, list, or any JSON-serializable object)
        status_code: HTTP status code (default: 200)

    Returns:
        Tuple of (response_dict, status_code)
    """
    return jsonify(data), status_code


def error_response(message, status_code=400, error_code=None):
    """
    Return a standardized error response

    Args:
        message: Error message
        status_code: HTTP status code (default: 400)
        error_code: Optional error code for client handling

    Returns:
        Tuple of (response_dict, status_code)
    """
    response = {"error": message}
    if error_code:
        response["code"] = error_code
    return jsonify(response), status_code


def not_found_response(resource_name="Resource"):
    """
    Return a standardized 404 not found response

    Args:
        resource_name: Name of the resource that was not found

    Returns:
        Tuple of (response_dict, 404)
    """
    return error_response(f"{resource_name} not found", 404)


def no_results_response(resource_name="Resources"):
    """
    Return a standardized response when no results found (empty list)

    Args:
        resource_name: Name of the resources being searched for

    Returns:
        Tuple of (response_dict, 404)
    """
    return error_response(f"No {resource_name} found", 404)


def created_response(data, status_code=201):
    """
    Return a standardized creation response

    Args:
        data: The created resource data
        status_code: HTTP status code (default: 201)

    Returns:
        Tuple of (response_dict, status_code)
    """
    return jsonify(data), status_code


def updated_response(data=None):
    """
    Return a standardized update response

    Args:
        data: The updated resource data (optional)

    Returns:
        Tuple of (response_dict, 200)
    """
    response_data = data if data else {"message": "Resource updated successfully"}
    return jsonify(response_data), 200


def deleted_response(resource_name="Resource"):
    """
    Return a standardized delete response

    Args:
        resource_name: Name of the deleted resource

    Returns:
        Tuple of (response_dict, 200)
    """
    return jsonify({"message": f"{resource_name} deleted successfully"}), 200


def validate_and_respond(result, resource_name="Resource", is_list=False):
    """
    Helper function to validate query result and return appropriate response

    Args:
        result: Query result (single object or list)
        resource_name: Name of the resource for error messages
        is_list: Whether the result should be a list (default: False)

    Returns:
        Tuple of (response_dict, status_code) or None if valid
    """
    if is_list:
        if not result or len(result) == 0:
            return no_results_response(resource_name)
    else:
        if not result:
            return not_found_response(resource_name)

    return None  # Return None if validation passes
