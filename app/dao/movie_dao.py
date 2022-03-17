from app.model.movie import Movie


# CRUD
class MovieDAO:
    def __init__(self, session):
        self.session = session

    def search(self, search_request):
        result = self.session.query(Movie)
        if search_request["director_id"]:
            result = result.filter(Movie.director_id == search_request["director_id"])
        if search_request["genre_id"]:
            result = result.filter(Movie.genre_id == search_request["genre_id"])
        if search_request["status"]:
                    result = result.sorted_by(Movie.year == search_request["genre_id"]) # TODO: descending sort
        if search_request["page"]:
                    result = result.filter(Movie.genre_id == search_request["genre_id"])

        return result.all()

    def update(self, movie):
        self.session.add(movie)
        self.session.commit()
        self.session.refresh(movie)
        return movie.id

    def get_original(self, mid):
        return self.session.query(Movie).get(mid)

    def get_all(self):
        return self.session.query(Movie).all()

    def create(self, data):
        movie = Movie(**data)
        return self.update(movie)

    def delete(self, mid):
        movie = self.get_original(mid)
        self.session.delete(movie)
        self.session.commit()



