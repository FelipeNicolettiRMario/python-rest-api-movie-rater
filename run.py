from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from controllers import user, participant

app = FastAPI()

app.include_router(user.user)
app.include_router(participant.participant)