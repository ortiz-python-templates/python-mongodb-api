import base64
import os
from uuid import uuid4


class EncryptionUtil:

    def generate_uuid():
        return str(uuid4())
    
    def generate_random_token(length: int):
        byte_length = (length * 3) // 4 + 1 
        random_bytes = os.urandom(byte_length)
        token = base64.urlsafe_b64encode(random_bytes).decode('utf-8')
        return token[:length]
    
