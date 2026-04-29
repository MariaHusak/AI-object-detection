from fastapi import HTTPException


class AuthFacade:

    def __init__(
        self,
        users,
        password_service,
        jwt_service
    ):
        self.users = users
        self.password = password_service
        self.jwt = jwt_service

    def register(self, username, password):
        existing = self.users.get_by_username(username)
        if existing:
            raise HTTPException(400, "User exists")
        hashed = self.password.hash(password)
        user = self.users.create(
            username,
            hashed
        )

        return {
            "id": user.id,
            "username": user.username
        }

    def login(self, username, password):
        user = self.users.get_by_username(username)
        if not user:
            raise HTTPException(401, "Invalid credentials")
        if not self.password.verify(password, user.password):
            raise HTTPException(401, "Invalid credentials")

        token = self.jwt.create_token(user.id)

        return {
            "access_token": token
        }
