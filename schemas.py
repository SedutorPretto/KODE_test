from pydantic import BaseModel
from sqlalchemy import Text


class NoteBase(BaseModel):
    title: str
    content: str


class NoteCreate(NoteBase):
    pass


class Note(NoteBase):
    owner_id: int

    class Config:
        from_attributes = True
