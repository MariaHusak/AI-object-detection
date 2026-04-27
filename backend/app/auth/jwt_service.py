from jose import jwt, JWTError
from datetime import datetime, timedelta


class JWTService:
    SECRET = "supersecretkey"
    ALGORITHM = "HS256"

    def create_token(self, user_id):
        payload = {
            "sub": str(user_id),
            "exp": datetime.utcnow() + timedelta(hours=24)
        }

        return jwt.encode(
            payload,
            self.SECRET,
            algorithm=self.ALGORITHM
        )

    def verify_token(self, token):
        try:
            return jwt.decode(
                token,
                self.SECRET,
                algorithms=[self.ALGORITHM]
            )

        except JWTError:
            return None
