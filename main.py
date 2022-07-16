from dotenv import load_dotenv
load_dotenv()

from utils.session_manager import SessionManager
import os

print(os.getenv("DATABASE_URL"))

sm = SessionManager()
sm.get_session()

sm2 = SessionManager()

print(sm == sm2)
print(sm.session)
print(sm2.session)


from models.image import Image

img = Image()

from models.user import User

usu = User()

from models.role_user import RoleUser

rou = RoleUser()

from models.participant import Participant

par = Participant()

from models.movie import Movie

mov = Movie()

from models.cast import Cast

cas = Cast()

from models.review import Review

rev = Review()