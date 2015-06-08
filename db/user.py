from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from db.session import Session
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)

    def __repr__(self):
        return "<User(name='%s', password='%s')>" % (
                self.username, self.password)
    @classmethod
    def create(cls, username, password):
        session = Session()
        session.execute(
            "INSERT INTO user(username, password) VALUES ('{username}', '{password}')".format(
                username=username, password=password
            )
        )
        session.commit()