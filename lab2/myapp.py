import random
import string
import time
import json

def generate_password():
    lower = random.choice(string.ascii_lowercase)
    upper = random.choice(string.ascii_uppercase)
    digit = random.choice(string.digits)
    special = random.choice("#.,!@&^%*")
    
    length = random.randint(8, 16)
    
    all_chars = string.ascii_letters + string.digits + "#.,!@&^%*"
    remaining_chars = [random.choice(all_chars) for _ in range(length - 4)]
    
    password_list = [lower, upper, digit, special] + remaining_chars
    random.shuffle(password_list)
    
    password = ''.join(password_list)
    return password

def app(environ, start_response):
    password = generate_password()
    time.sleep(0.05)
    
    response_data = {
        "password": password,
        "length": len(password),
        "status": "success"
    }
    
    data = json.dumps(response_data, indent=2).encode('utf-8')
    
    start_response("200 OK", [
        ("Content-Type", "application/json"),
        ("Content-Length", str(len(data)))
    ])
    
    return iter([data])