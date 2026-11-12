
from pydantic import BaseModel, ConfigDict


class MovieResponse(BaseModel):
    id: int
    title: str
    genre: str | None = None

    model_config = ConfigDict(from_attributes=True)
class MovieCreate(BaseModel):
    title: str
    genre: str | None = None

class MovieUpdate(BaseModel):
    title: str
    genre: str | None = None

class RatingCreate(BaseModel):
    user_id: int
    movie_id: int
    rating: float

class UserCreate(BaseModel):
    username: str
    email: str

class UserRegister(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str
