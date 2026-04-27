from passlib.context import CryptContext


class PasswordService:

    def __init__(self):
        self.context = CryptContext(
            schemes=["pbkdf2_sha256"],
            deprecated="auto"
        )

    def hash(self, password):
        return self.context.hash(password)

    def verify(self, plain, hashed):
        return self.context.verify(plain, hashed)
