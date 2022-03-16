from app.model.genre import Genre


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

    def get_all(self):
        return self.session.query(Genre).all()

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