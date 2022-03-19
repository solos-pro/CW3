from app.model.genre import Genre
from constants import ITEMS_PER_PAGE

# CRUD



class GenreDAO:
    def __init__(self, session):
        self.session = session

    def db_update(self, genre):
        self.session.add(genre)
        self.session.commit()
        self.session.refresh(genre)         # ?
        return genre.id

    def get_one(self, gid):
        return self.session.query(Genre).get(gid)

    def get_all(self, page_num):
        result = self.session.query(Genre)
        if page_num:
            result = result.limit(ITEMS_PER_PAGE).offset((int(page_num) - 1) * ITEMS_PER_PAGE)
        return result.all()

    def create(self, data):
        genre = Genre(**data)
        return self.db_update(genre)

    def delete(self, gid):
        genre = self.get_one(gid)
        self.session.delete(genre)
        self.session.commit()


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