from typing import List

from fastapi import FastAPI, Depends, HTTPException, status

import schemas
from database import async_engine, get_async_session
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from models import Base, User, NoteModel
from utils import create_predefined_users, check_spelling
from hashing import verify_password
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


app = FastAPI()


async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("startup")
async def on_startup():
    await init_db()
    await create_predefined_users()


security = HTTPBasic()


async def get_current_user(
    credentials: HTTPBasicCredentials = Depends(security),
    session: AsyncSession = Depends(get_async_session),
):
    result = await session.execute(
        select(User).filter(User.username == credentials.username)
    )
    user = result.scalars().first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user


@app.get("/notes/", response_model=List[schemas.Note])
async def read_notes(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    # return [note for note in fake_notes if note.get('owner_id') == user_id]
    result = await db.execute(
        select(NoteModel).filter(NoteModel.owner_id == current_user.user_id)
    )
    notes = result.scalars().all()
    return notes


@app.post("/notes/", response_model=schemas.Note)
async def save_note(
    note: schemas.NoteCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    db_note = NoteModel(**note.dict(), owner_id=current_user.user_id)
    await check_spelling(db_note.content)
    db.add(db_note)
    await db.commit()
    await db.refresh(db_note)
    return db_note
