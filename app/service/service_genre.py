from app.dao.genre_dao import GenreDAO


class GenreService:
    def __init__(self, dao: GenreDAO):
        self.dao = dao

    def get_one(self, gid):
        return self.dao.get_one(gid)

    def get_all(self, page_num):
        return self.dao.get_all(page_num)

    def create(self, data):
        return self.dao.create(data)

    def get_update(self, data):
        gid = data.get("id")
        genre = self.get_one(gid)

        genre.name = data.get("name")

        self.dao.db_update(genre)

    def update_partial(self, data):
        gid = data.get("id")
        genre = self.get_one(gid)

        if "name" in data:
            genre.name = data.get("name")
        self.dao.db_update(genre)

    def delete(self, gid):
        self.dao.delete(gid)



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