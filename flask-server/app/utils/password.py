import hashlib


def hash_password(password):
    """
    Hashes the password using SHA256.

    Args:
        password (str): The password to hash.

    Returns:
        str: A hashed version of the password.
    """
    return hashlib.sha256(password.encode("utf-8")).hexdigest()