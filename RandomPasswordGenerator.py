import random
import string

def generate_password(length=12):
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    password = []
    
    # Ensure at least one character from each category
    password.append(random.choice(string.ascii_lowercase))
    password.append(random.choice(string.ascii_uppercase))
    password.append(random.choice("!@#$%^&*"))
    
    # Fill remaining characters
    for _ in range(length-4):
        password.append(random.choice(characters))
    
    random.shuffle(password)
    return ''.join(password)

print("Your new password:", generate_password())