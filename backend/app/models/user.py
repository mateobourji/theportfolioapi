import string
from typing import Optional
from pydantic import EmailStr, constr, validator
from backend.app.models.core import DateTimeModelMixin, IDModelMixin, CoreModel
from backend.app.models.token import AccessToken

# simple check for valid username
def validate_username(username: str) -> str:
    allowed = string.ascii_letters + string.digits + "-" + "_"
    assert all(char in allowed for char in username), "Invalid characters in username."
    assert len(username) >= 3, "Username must be 3 characters or more."
    return username


class UserBase(CoreModel):
    """
    Leaving off password and salt from base model
    """
    email: Optional[EmailStr]
    username: Optional[str]
    email_verified: bool = False
    is_active: bool = True
    is_superuser: bool = False


class UserCreate(CoreModel):
    """
    Email, username, and password are required for registering a new user
    """
    email: EmailStr
    password: constr(min_length=7, max_length=100)
    username: str

    @validator("username", pre=True)
    def username_is_valid(cls, username: str) -> str:
        return validate_username(username)


class UserUpdate(CoreModel):
    """
    Users are allowed to update their email and/or username
    """
    email: Optional[EmailStr]
    username: Optional[str]

    @validator("username", pre=True)
    def username_is_valid(cls, username: str) -> str:
        return validate_username(username)


class UserPasswordUpdate(CoreModel):
    """
    Users can change their password
    """
    password: constr(min_length=7, max_length=100)
    salt: str


class UserInDB(IDModelMixin, DateTimeModelMixin, UserBase):
    """
    Add in id, created_at, updated_at, and user's password and salt
    """
    password: constr(min_length=7, max_length=100)
    salt: str


class UserPublic(IDModelMixin, DateTimeModelMixin, UserBase):
    access_token: Optional[AccessToken]

