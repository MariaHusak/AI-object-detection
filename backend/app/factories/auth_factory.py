from app.auth.jwt_service import JWTService
from app.auth.password_service import PasswordService
from app.facades.auth_facade import AuthFacade
from app.repositories.user_repository import UserRepository


class AuthFactory:

    @staticmethod
    def create(db):
        return AuthFacade(
            users=UserRepository(db),
            password_service=PasswordService(),
            jwt_service=JWTService()
        )
