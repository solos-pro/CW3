from app.dao.director_dao import DirectorDAO


class DirectorService:
    def __init__(self, dao: DirectorDAO):
        self.dao = dao

    def get_one(self, did):
        return self.dao.get_one(did)

    def get_all(self, page_num):
        return self.dao.get_all(page_num)

    def create(self, data):
        return self.dao.create(data)

    def get_update(self, data):
        did = data.get("id")
        director = self.get_one(did)

        director.name = data.get("name")

        self.dao.db_update(director)

    def update_partial(self, data):
        did = data.get("id")
        director = self.get_one(did)

        if "name" in data:
            director.name = data.get("name")
        self.dao.db_update(director)

    def delete(self, did):
        self.dao.delete(did)



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