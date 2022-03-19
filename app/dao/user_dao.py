# import sqlalchemy
from typing import Optional
from sqlalchemy.exc import IntegrityError
from app.model.user import User

# CRUD
from app.exceptions import IncorrectData, DuplicateError


class UserDAO:
    def __init__(self, session):
        self.session = session
        self._roles = {"user", "admin"}

    # def create_role(self, role) -> int:
    #     group = Group(role=role)
    #     self.session.add(group)
    #     self.session.flush()
    #     self.session.commit()
    #     print(group.id)
    #     return group.id

    # def get_role(self, role):
    #     return self.session.query(Group).filter_by(role=role).one_or_none()

    def get_one_by_id(self, id):
        return self.session.query(User).get(id)

    def get_one_by_username(self, username) -> Optional[User]:
        tech = self.session.query(User).filter(User.name == username).one_or_none()
        print(tech.name)
        return self.session.query(User).filter(User.name == username).one_or_none()

    def get_all(self):
        return self.session.query(User).all()

    def create(self, data):
        try:
            # role = data.pop('role')
            # group = Group.query.filter_by(role=role).one_or_none()
            # if not group:
            #     group = Group(role=role)
            #     self.session.add(group)
            #     self.session.commit()
            #
            # data['role_id'] = group.id
            # print(data, "DAO_create")
            user = User(**data)
            self.session.add(user)
            self.session.commit()
            return user
        except IntegrityError:
            raise DuplicateError

    def create_alternative(self, data):
        try:
            print(data)
            user = User(**data)
            self.session.add(user)
            self.session.commit()
            return user
        except IntegrityError:
            raise DuplicateError

    def update_role(self, username: str, role: str):
        if role not in self._roles:
            raise IncorrectData

        user = self.get_one_by_username(username)
        user.role = role
        self.session.delete(user)
        self.session.commit()

    def update_password(self, username: str, password_hash: str):
        user = self.get_one_by_username(username)
        user.password = password_hash
        self.session.add(user)
        self.session.commit()

    def delete(self, uid):
        user = self.get_one_by_id(uid)
        self.session.delete(user)
        self.session.commit()
