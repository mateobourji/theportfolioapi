import logging
from pydantic import EmailStr
from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
from databases import Database
from app.db.repositories.base import BaseRepository
from app.models.user import UserCreate, UserUpdate, UserInDB
from app.services import auth_service
from typing import Optional

GET_USER_BY_EMAIL_QUERY = """
    SELECT id, username, email, email_verified, password, salt, is_active, is_superuser, added_at, updated_at
    FROM users
    WHERE email = :email;
"""
GET_USER_BY_USERNAME_QUERY = """
    SELECT id, username, email, email_verified, password, salt, is_active, is_superuser, added_at, updated_at
    FROM users
    WHERE username = :username;
"""
REGISTER_NEW_USER_QUERY = """
    INSERT INTO users (username, email, password, salt)
    VALUES (:username, :email, :password, :salt)
    RETURNING id, username, email, email_verified, password, salt, is_active, is_superuser, added_at, updated_at;
"""

db_logger = logging.getLogger("DB")


class UsersRepository(BaseRepository):

    def __init__(self, db: Database) -> None:
        super().__init__(db)
        self.auth_service = auth_service

    async def get_user_by_email(self, *, email: EmailStr) -> UserInDB:
        user_record = await self.db.fetch_one(query=GET_USER_BY_EMAIL_QUERY, values={"email": email})
        if not user_record:
            db_logger.log(level=logging.INFO,
                          msg="No registered user exists with e-mail: %s" % email)
            return None
        db_logger.log(level=logging.INFO,
                      msg="Returning user with e-mail: %s" % email)
        return UserInDB(**user_record)

    async def get_user_by_username(self, *, username: str) -> UserInDB:
        user_record = await self.db.fetch_one(query=GET_USER_BY_USERNAME_QUERY, values={"username": username})
        if not user_record:
            db_logger.log(level=logging.INFO,
                          msg="No registered user exists with username: %s" % username)
            return None
        db_logger.log(level=logging.INFO,
                      msg="Returning user with username: %s" % username)
        return UserInDB(**user_record)

    async def register_new_user(self, *, new_user: UserCreate) -> UserInDB:
        # make sure email isn't already taken
        if await self.get_user_by_email(email=new_user.email):
            db_logger.log(level=logging.INFO,
                          msg="Unable to register new user, e-mail: %s already used."
                              "Raising HTTP 400 Bad Request Exception." % new_user.email)
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="That email is already taken. Login with that email or register with another one."
            )
        # make sure username isn't already taken
        if await self.get_user_by_username(username=new_user.username):
            db_logger.log(level=logging.INFO,
                          msg="Unable to register new user, username: %s already taken. "
                              "Raising HTTP 400 Bad Request Exception." % new_user.username)
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="That username is already taken. Please try another one."
            )

        user_password_update = self.auth_service.create_salt_and_hashed_password(plaintext_password=new_user.password)
        new_user_params = new_user.copy(update=user_password_update.dict())
        created_user = await self.db.fetch_one(query=REGISTER_NEW_USER_QUERY, values=new_user_params.dict())
        db_logger.log(level=logging.INFO,
                      msg="Registered new user with username: %s and e-mail: %s" % (new_user.username, new_user.email))
        return UserInDB(**created_user)

    async def authenticate_user(self, *, username: str, password: str) -> Optional[UserInDB]:
        # make user user exists in db
        user = await self.get_user_by_username(username=username)
        if not user:
            return None
        # if submitted password doesn't match
        if not self.auth_service.verify_password(password=password, salt=user.salt, hashed_pw=user.password):
            db_logger.log(level=logging.INFO,
                          msg="Could not authenticate user with username: %s. Incorrect password." % username)
            return None
        db_logger.log(level=logging.INFO,
                      msg="Successfully authenticated user with username: %s." % username)
        return user
