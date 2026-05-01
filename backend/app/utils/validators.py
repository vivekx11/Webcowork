"""
Input validation utilities
"""
import re
from email_validator import validate_email, EmailNotValidError

def validate_email_format(email):
    """Validate email format"""
    try:
        validate_email(email)
        return True, None
    except EmailNotValidError as e:
        return False, str(e)

def validate_password(password):
    """
    Validate password strength
    Requirements: At least 6 characters
    """
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    return True, None

def validate_phone(phone):
    """Validate phone number format"""
    if not phone:
        return True, None
    
    # Remove common separators
    cleaned = re.sub(r'[\s\-\(\)]', '', phone)
    
    # Check if it contains only digits and optional + at start
    if not re.match(r'^\+?\d{10,15}$', cleaned):
        return False, "Invalid phone number format"
    
    return True, None

def validate_required_fields(data, required_fields):
    """Validate that all required fields are present"""
    missing_fields = []
    for field in required_fields:
        if field not in data or not data[field]:
            missing_fields.append(field)
    
    if missing_fields:
        return False, f"Missing required fields: {', '.join(missing_fields)}"
    
    return True, None

def validate_positive_number(value, field_name):
    """Validate that a number is positive"""
    try:
        num = float(value)
        if num <= 0:
            return False, f"{field_name} must be a positive number"
        return True, None
    except (ValueError, TypeError):
        return False, f"{field_name} must be a valid number"

def validate_integer(value, field_name):
    """Validate that a value is an integer"""
    try:
        int(value)
        return True, None
    except (ValueError, TypeError):
        return False, f"{field_name} must be an integer"

def validate_rating(rating):
    """Validate rating is between 1 and 5"""
    try:
        rating_int = int(rating)
        if rating_int < 1 or rating_int > 5:
            return False, "Rating must be between 1 and 5"
        return True, None
    except (ValueError, TypeError):
        return False, "Rating must be a valid integer"
