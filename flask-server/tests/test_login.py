import logging

# Configure logging to output to a text file
logging.basicConfig(filename="login_activity.txt", level=logging.INFO, format='%(asctime)s - %(message)s')

# Simulate a simple User class for testing
class User:
    def __init__(self, username):
        self.username = username

    def __str__(self):
        return self.username

# A simple function to simulate login
def login(username, password):
    # In-memory users database (replace with your actual user data logic)
    users = {"testuser": "password123", "admin": "admin123"}
    
    # Check if user exists and password matches
    if username in users and users[username] == password:
        user = User(username)
        logging.info(f"User '{username}' logged in successfully")
        print(f"Login successful for {username}")
    else:
        logging.info(f"Failed login attempt for '{username}'")
        print(f"Failed login for {username}")

# Test the login function
if __name__ == "__main__":
    # Simulate valid and invalid logins
    login("testuser", "password123")  # Valid login
    login("admin", "wrongpassword")   # Invalid login
    login("nonexistentuser", "password123")  # Invalid login
