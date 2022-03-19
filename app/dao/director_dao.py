from app.model.director import Director


# CRUD
from constants import ITEMS_PER_PAGE


class DirectorDAO:
    def __init__(self, session):
        self.session = session

    def db_update(self, director):
        self.session.add(director)
        self.session.commit()
        self.session.refresh(director)
        return director.id

    def get_one(self, did):
        return self.session.query(Director).get(did)

    def get_all(self, page_num):
        result = self.session.query(Director)
        if page_num:
            result = result.limit(ITEMS_PER_PAGE).offset((int(page_num) - 1) * ITEMS_PER_PAGE)
        return result.all()

    def create(self, data):
        director = Director(**data)
        return self.db_update(director)

    def delete(self, did):
        director = self.get_one(did)
        self.session.delete(director)
        self.session.commit() 
        # self.db_update(director)


"""
# это файл для классов доступа к данным 
(Data Access Object). Здесь должен быть класс с 
методами доступа к данным
# здесь в методах можно построить сложные запросы 
к БД

# Например

# class BookDAO:
#     def get_all_books(self):
#         books = Book.query.all()
#         return"""