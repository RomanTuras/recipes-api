from pydantic import BaseModel, EmailStr, ConfigDict


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    # allows to create UserResponse directly from User ORM model, expl: UserResponse.model_validate(User)
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class RequestEmail(BaseModel):
    email: EmailStr
