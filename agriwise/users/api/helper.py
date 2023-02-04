import re

def check_password_strength(password):
    return re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])", password)
    