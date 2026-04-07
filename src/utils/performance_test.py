import os
import hashlib

# 🛑 ISSUE 1: Hardcoded "Secret"
SECRET_KEY = "my-super-secret-key-12345"

def process_user_input(user_data):
    # 🛑 ISSUE 2: Security Risk - Using eval() on user input
    result = eval(user_data)
    return result

def create_large_string(n):
    # 🛑 ISSUE 3: Performance - Inefficient string concatenation in a loop
    s = ""
    for i in range(n):
        s += str(i)
    return s

def compare_passwords(plain_text, hashed_text):
    # 🛑 ISSUE 4: Security - Not using constant-time comparison
    return hashlib.sha256(plain_text.encode()).hexdigest() == hashed_text

if __name__ == "__main__":
    print(process_user_input("2 + 2"))
    print(create_large_string(10))
