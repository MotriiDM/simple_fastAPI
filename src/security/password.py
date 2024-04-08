import hashlib


async def encrypt_password(password: str):
    salt = "5gz"
    encrypted_password = password + salt
    hashed = hashlib.md5(encrypted_password.encode())
    return hashed.hexdigest()