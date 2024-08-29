import uvicorn
from typing import List

from fastapi import FastAPI

import models
import schemas
from database import async_engine, async_session
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from models import Base
from sqlalchemy.orm import Session

async with async_engine.begin() as conn:
    conn.run_sync(Base.metadata.create_all)

app = FastAPI()

fake_notes = [
    {'note_id': 1, 'title': 'abd', 'content': 'xxxxxxxxxxxxx', 'owner_id': 1, 'owner': 'sedutor'},
    {'note_id': 2, 'title': 'abd2', 'content': 'xyxyxyxyxyxyyxy', 'owner_id': 1, 'owner': 'sedutor'},
    {'note_id': 3, 'title': 'zzz', 'content': 'rjfhaekrfljвшащ', 'owner_id': 2, 'owner': 'pretto'}
]

@app.get('/notes/', response_model=List[schemas.Note])
def read_notes(user_id: int):
    return [note for note in fake_notes if note.get('owner_id') == user_id]
    # return db.query(models.Note).filter(models.Note.owner_id == user_id).all()


# @app.post('/notes/', response_model=schemas.Note)
# def save_note(db: Session, ):
#     pass


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
