from app.dao.user_dao import UserDAO
from app.exceptions import DuplicateError
from app.tools.security import get_password_hash, compare_passwords, get_password_digest
from typing import Optional
from app.dao.user_dao import User
from typing import Any, Dict


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def search(self, user):
        return self.dao.get_one_by_id(user)

    def get_one(self, uid):
        return self.dao.get_one_by_id(uid)

    def get_by_username(self, name) -> Optional[User]:
        user = self.dao.get_one_by_username(name)
        print(user.id, "(UserService)")

        return self.dao.get_one_by_username(name)

    def get_by_email(self, email) -> Optional[User]:
        return self.dao.get_one_by_email(email)

    def create(self, email, password):
        return self.dao.create({
            "email": email,
            "password": get_password_hash(password)
        })

    def create_alternative(self, **user):
        duplicate_email = self.dao.get_one_by_email(email=user["email"])
        if duplicate_email:
            raise DuplicateError

        if "name" not in user:
            user["name"] = None
        if "surname" not in user:
            user["surname"] = None
        if "favorite_genre_id" not in user:
            user["favorite_genre_id"] = None

        return self.dao.create_alternative({
            "email": user["email"],
            "password": get_password_hash(user["password"]),
            "name": user["name"],
            "surname": user["surname"],
            "favorite_genre_id": user["favorite_genre_id"]
        })

    def update_partial(self, data: Dict, uid: int):
        user = self.get_one(uid)

        if "name" in data:
            user.name = data["name"]
        if "surname" in data:
            user.surname = data["surname"]
        if "favorite_genre_id" in data:
            user.favorite_genre_id = data["favorite_genre_id"]

        return self.dao.update(user)

    def compare_password(self, data: Dict, uid: int):
        user = self.get_one(uid)
        # print(user.password)
        return compare_passwords(user.password, data["password_1"])
        # return user.password

    def update_password(self, data: Dict, uid: int):
        user = self.get_one(uid)
        user.password = get_password_hash(data["password_2"])
        return self.dao.update(user)

    def delete(self, mid):
        self.dao.delete(mid)

# ===============================================================================
