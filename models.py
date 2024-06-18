from sqlalchemy import create_engine, Integer, String, ForeignKey, Date, Column, DateTime, select
from sqlalchemy.orm import declarative_base, sessionmaker, Mapped, mapped_column, relationship
from datetime import datetime

engine = create_engine('sqlite:///database.db')
DBSession = sessionmaker(bind=engine)
session = DBSession()

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)

class Note(Base):
    __tablename__ = 'note'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String)
    text: Mapped[str] = mapped_column(String)
    creation_date  = Column(DateTime, default=datetime.utcnow)
    user_id: Mapped[str] = mapped_column('user_id', Integer, ForeignKey('user.id'))
    user: Mapped['User'] = relationship(User)


Base.metadata.create_all(engine)