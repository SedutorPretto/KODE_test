from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.orm import  relationship, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user'

    user_id: Mapped[int] = mapped_column(primary_key=True, unique=True, index=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    notes: Mapped[List['Note']] = relationship(back_populates='note', cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return f'User(id={self.user_id}, username={self.username})'


class Note(Base):
    __tablename__ = 'note'

    note_id: Mapped[int] = mapped_column(primary_key=True, unique=True, index=True, autoincrement=True)
    title: Mapped[str] = mapped_column(index=True)
    content: Mapped[str]
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'))
    owner: Mapped['User'] = relationship(back_populates='notes')

    def __repr__(self) -> str:
        return f'Note(id={self.note_id}, title={self.title})'
