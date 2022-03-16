from app.dao.user_dao import UserDAO
from app.exceptions import DuplicateError
from app.tools.security import get_password_hash
from typing import Optional
from app.dao.user_dao import User, Group


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def search(self, user):
        return self.dao.get_one_by_id(user)

    def get_one(self, uid):
        return self.dao.get_one_by_username(uid)

    def get_by_username(self, username) -> Optional[User]:
        user = self.dao.get_one_by_username(username)
        print(user.id, user.role_id, "(UserService)")

        return self.dao.get_one_by_username(username)

    def create(self, username, password, role: str = "user"):
        return self.dao.create({
            "username": username,
            "password": get_password_hash(password),
            "role": role
        })

    def create_alternative(self, username, password, role: str = "user"):
        duplicate_username = self.dao.get_one_by_username(username=username)
        if duplicate_username:
            raise DuplicateError

        bd_role = self.dao.get_role(role)       # search ID of str(role) in the database
        if bd_role:
            role_id = bd_role.id
            print('role_id=', role_id)
        else:
            role_id = self.dao.create_role(role)    # create a record in the database and return ID
        return self.dao.create_alternative({
            "username": username,
            "password": get_password_hash(password),
            "role_id": role_id
        })

    def update(self, data):
        uid = data.get("id")
        user = self.dao.get_one_by_id(uid)

        user.username = data.get("username")
        user.password = data.get("password")
        user.role = data.get("role")

        self.dao.update(user)

    def update_partial(self, data):
        uid = data.get("id")
        user = self.get_one(uid)

        if "username" in data:
            user.username = data.get("username")
        if "password" in data:
            user.password = data.get("password")
        if "role" in data:
            user.role = data.get("role")

        self.dao.update(user)

    def delete(self, mid):
        self.dao.delete(mid)


# ===============================================================================
