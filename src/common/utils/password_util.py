from passlib.context import CryptContext

class PasswordUtil:
   
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    def hash(password: str) -> str:
        return PasswordUtil.pwd_context.hash(password)

    @staticmethod
    def verify(plain_password: str, hashed_password: str) -> bool:
        return PasswordUtil.pwd_context.verify(plain_password, hashed_password)
