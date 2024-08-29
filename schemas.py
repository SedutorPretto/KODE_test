from pydantic import BaseModel


class NoteBase(BaseModel):
    note_id: int
    title: str
    content: str


class NoteCreate(NoteBase):
    pass


class Note(NoteBase):
    owner_id: int
    owner: str

    # class Config:
    #     orm_mode = True
