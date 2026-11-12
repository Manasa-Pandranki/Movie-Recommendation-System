from backend.recommendation import get_recommendations
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from backend.auth import SECRET_KEY, ALGORITHM

from backend.database import get_db
from backend.models import Movie, User, Rating
from backend.schemas import (
    MovieResponse,
    MovieCreate,
    MovieUpdate,
    UserCreate,
    RatingCreate
)
from backend.auth import (
    hash_password,
    verify_password,
    create_access_token
)
from backend.schemas import UserRegister, UserLogin
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(
        User.id == int(user_id)
    ).first()

    if user is None:
        raise credentials_exception

    return user

app = FastAPI(title="Movie Recommendation System API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "message": "Welcome to Movie Recommendation System API",
        "status": "success"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
@app.get("/movies", response_model=list[MovieResponse])
def get_movies(db: Session = Depends(get_db)):
    movies = db.query(Movie).all()
    return movies
@app.post("/movies", response_model=MovieResponse, status_code=201)
def create_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    new_movie = Movie(
        title=movie.title,
        genre=movie.genre
    )

    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)

    return new_movie

@app.get("/movies/search", response_model=list[MovieResponse])
def search_movies(title: str, db: Session = Depends(get_db)):
    movies = db.query(Movie).filter(
        Movie.title.ilike(f"%{title}%")
    ).all()

    return movies


@app.get("/movies/{movie_id}", response_model=MovieResponse)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()

    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    return movie

@app.put("/movies/{movie_id}", response_model=MovieResponse)
def update_movie(
    movie_id: int,
    movie_data: MovieUpdate,
    db: Session = Depends(get_db)
):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()

    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    movie.title = movie_data.title
    movie.genre = movie_data.genre

    db.commit()
    db.refresh(movie)

    return movie


@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()

    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    db.delete(movie)
    db.commit()

    return {"message": "Movie deleted successfully"}
@app.post("/users", status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(
        username=user.username,
        email=user.email
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email
    }
@app.post("/ratings", status_code=201)
def create_rating(rating_data: RatingCreate, db: Session = Depends(get_db)):
    new_rating = Rating(
        user_id=rating_data.user_id,
        movie_id=rating_data.movie_id,
        rating=rating_data.rating
    )

    db.add(new_rating)
    db.commit()
    db.refresh(new_rating)

    return {
        "id": new_rating.id,
        "user_id": new_rating.user_id,
        "movie_id": new_rating.movie_id,
        "rating": new_rating.rating
    }
@app.get("/ratings")
def get_ratings(db: Session = Depends(get_db)):
    ratings = db.query(Rating).all()

    return [
        {
            "id": rating.id,
            "user_id": rating.user_id,
            "movie_id": rating.movie_id,
            "rating": rating.rating
        }
        for rating in ratings
    ]
@app.get("/ratings/movie/{movie_id}")
def get_movie_ratings(movie_id: int, db: Session = Depends(get_db)):
    ratings = db.query(Rating).filter(
        Rating.movie_id == movie_id
    ).all()

    return [
        {
            "id": rating.id,
            "user_id": rating.user_id,
            "movie_id": rating.movie_id,
            "rating": rating.rating
        }
        for rating in ratings
    ]

@app.get("/recommendations/{user_id}")
def recommend_movies(user_id: int, top_n: int = 5):
    recommendations = get_recommendations(user_id, top_n)

    return {
        "user_id": user_id,
        "recommendations": recommendations
    }
@app.post("/auth/register")
def register_user(user: UserRegister, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "user_id": new_user.id
    }


@app.post("/auth/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not existing_user or not existing_user.hashed_password:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        user.password,
        existing_user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={"sub": str(existing_user.id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
@app.post("/auth/token")
def login_for_swagger(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    if not existing_user or not existing_user.hashed_password:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        form_data.password,
        existing_user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={"sub": str(existing_user.id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
@app.get("/users/me")
def read_current_user(
    current_user: User = Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email
    }


    