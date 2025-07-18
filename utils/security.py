# app/utils/security.py
import secrets

def generate_admin_key():
    return secrets.token_urlsafe(16)

def check_admin_key(input_key, stored_key):
    return input_key == stored_key
