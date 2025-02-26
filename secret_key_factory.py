#!/usr/bin/env python3
import secrets
import string


def generate_secret_key(length=50):
    # Define the characters to choose from: letters, digits, and punctuation.
    # Optionally, you can remove characters that may cause issues (like quotes).
    chars = string.ascii_letters + string.digits + string.punctuation
    # Remove problematic characters (optional)
    safe_chars = "".join(c for c in chars if c not in "'\"\\")
    return "".join(secrets.choice(safe_chars) for _ in range(length))


if __name__ == "__main__":
    secret_key = generate_secret_key()
    print("Your Django secret key is:")
    print(secret_key)
