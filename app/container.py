from app.database import db

from app.dao.movie_dao import MovieDAO
from app.dao.genre_dao import GenreDAO
from app.dao.director_dao import DirectorDAO
from app.dao.user_dao import UserDAO

from app.service.service_genre import GenreService
from app.service.service_movie import MovieService
from app.service.service_director import DirectorService
from app.service.service_user import UserService
# from app.service.service_auth import AuthService


movie_dao = MovieDAO(db.session)
movie_service = MovieService(dao=movie_dao)

genre_dao = GenreDAO(db.session)
genre_service = GenreService(dao=genre_dao)

director_dao = DirectorDAO(db.session)
director_service = DirectorService(dao=director_dao)

user_dao = UserDAO(db.session)
user_service = UserService(dao=user_dao)

# auth_service = AuthService()


