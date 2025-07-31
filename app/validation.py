import re

# Function to validate email format
def is_valid_email(email: str) -> bool:
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$" # Basic regex for email validation, a-z, A-Z, 0-9, ., _, %, +, -, @, and domain with at least two characters
    return bool(re.match(email_regex, email))

# Function to validate password strength
def is_valid_password(password: str) -> bool:
    password_regex = r"^(?=.*[A-Z])(?=.*[a-z])(?=(.*\d){2})[A-Za-z\d]+$" # Password must contain at least one uppercase letter, one lowercase letter, and two digits
    return bool(re.match(password_regex, password))