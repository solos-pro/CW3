from app.dao.movie_dao import MovieDAO


class MovieService:
    def __init__(self, dao: MovieDAO):
        self.dao = dao

    def search(self, search_request):
        return self.dao.search(search_request)

    def get_one(self, mid):
        return self.dao.get_original(mid)

    def get_all(self):
        return self.dao.get_all()

    def create(self, data):
        return self.dao.create(data)

    def update(self, data):
        mid = data.get("id")
        movie = self.dao.get_original(mid)

        movie.title = data.get("title")
        movie.description = data.get("description")
        movie.trailer = data.get("trailer")
        movie.year = data.get("year")
        movie.rating = data.get("rating")
        movie.genre_id = data.get("genre_id")
        movie.genre = data.get("genre")
        movie.director_id = data.get("director_id")
        movie.director = data.get("director")

        self.dao.update(movie)

    def update_partial(self, data):
        mid = data.get("id")
        movie = self.dao.get_original(mid)

        if "title" in data:
            movie.title = data.get("title")
        if "description" in data:
            movie.description = data.get("description")
        if "trailer" in data:
            movie.trailer = data.get("trailer")
        if "year" in data:
            movie.year = data.get("year")
        if "rating" in data:
            movie.rating = data.get("rating")
        if "genre_id" in data:
            movie.genre_id = data.get("genre_id")
        if "genre" in data:
            movie.genre = data.get("genre")
        if "director_id" in data:
            movie.director_id = data.get("director_id")
        if "director" in data:
            movie.director = data.get("director")

        self.dao.update(movie)

    def delete(self, mid):
        self.dao.delete(mid)
"""
"""


# здесь бизнес логика, в виде классов или методов. сюда импортируются DAO классы из пакета dao и модели из dao.model
# некоторые методы могут оказаться просто прослойкой между dao и views,
# но чаще всего будет какая-то логика обработки данных сейчас или в будущем.

# Пример

# class BookService:
#
#     def __init__(self, book_dao: BookDAO):
#         self.book_dao = book_dao
#
#     def get_books(self) -> List["Book"]:
#         return self.book_dao.get_books()