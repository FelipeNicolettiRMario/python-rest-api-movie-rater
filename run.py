from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from controllers import user, participant, movie

app = FastAPI()

app.include_router(user.user)
app.include_router(participant.participant)
app.include_router(movie.movie)