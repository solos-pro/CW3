# import sqlalchemy
from typing import Optional
from sqlalchemy.exc import IntegrityError
from app.model.user import User

# CRUD
from app.exceptions import IncorrectData, DuplicateError


class UserDAO:
    def __init__(self, session):
        self.session = session
        # self._roles = {"user", "admin"}

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

    def get_one_by_username(self, name) -> Optional[User]:
        return self.session.query(User).filter(User.name == name).one_or_none()

    def get_one_by_email(self, email) -> Optional[User]:
        return self.session.query(User).filter(User.email == email).one_or_none()

    def get_all(self):
        return self.session.query(User).all()

    def create(self, data):
        try:
            user = User(**data)
            self.session.add(user)
            self.session.commit()
            return user
        except IntegrityError:
            raise DuplicateError

    def create_alternative(self, data):
        try:
            user = User(**data)
            self.session.add(user)
            self.session.commit()
            return user
        except IntegrityError:
            raise DuplicateError

    def update(self, data):
        user = data             # TODO: Is it correct?
        print(user.password, " - WR to the db a password")
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def update_password(self, username: str, password_hash: str):
        user = self.get_one_by_username(username)
        user.password = password_hash
        self.session.add(user)
        self.session.commit()

    def delete(self, uid):
        user = self.get_one_by_id(uid)
        self.session.delete(user)
        self.session.commit()
