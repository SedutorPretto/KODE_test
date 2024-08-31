from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.orm import relationship, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(primary_key=True, unique=True, index=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    # notes: Mapped[list['Note']] = relationship('Note', back_populates='owner', cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f'User(id={self.user_id}, username={self.username})'


class NoteModel(Base):
    __tablename__ = 'notes'

    note_id: Mapped[int] = mapped_column(primary_key=True, unique=True, index=True, autoincrement=True)
    title: Mapped[str] = mapped_column(unique=True, index=True)
    content: Mapped[str] = mapped_column(Text)
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.user_id', ondelete='CASCADE'))

    def __repr__(self) -> str:
        return f'Note(id={self.note_id}, title={self.title})'
