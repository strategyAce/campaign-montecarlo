# Hardcoded username and password
# In production, these should be stored securely
import os

def authenticate(username: str, password: str) -> bool:
    """
    Authenticate user credentials
    
    Args:
        username (str): Input username
        password (str): Input password
    
    Returns:
        bool: True if credentials are valid, False otherwise
    """
    USERNAME = os.environ.get('USERNAME')
    PASSWORD = os.environ.get('PASSWORD')
    return username == USERNAME and password == PASSWORD
