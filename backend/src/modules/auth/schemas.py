from pydantic import BaseModel, EmailStr, Field


class UserSignupRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=20)
    password: str = Field(..., min_length=6, max_length=100)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    phone: str
    role: str
    status: str

    model_config = {"from_attributes": True}