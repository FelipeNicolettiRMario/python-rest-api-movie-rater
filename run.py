from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from controllers import user

app = FastAPI()

app.include_router(user.user)