import uvicorn
import httpx
from typing import List

from fastapi import FastAPI, Depends, HTTPException, status

import schemas
from database import async_engine, session_maker, get_async_session
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from models import Base, User, NoteModel
from hashing import get_password_hash, verify_password
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


app = FastAPI()


async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def create_predefined_users():
    async with session_maker() as session:
        async with session.begin():
            predefined_users = [
                {"username": "user1", "password": "password1"},
                {"username": "user2", "password": "password2"}
            ]

            for user_data in predefined_users:
                result = await session.execute(select(User).filter_by(username=user_data["username"]))
                user = result.scalars().first()
                if not user:
                    hashed_password = get_password_hash(user_data["password"])
                    new_user = User(username=user_data["username"], hashed_password=hashed_password)
                    session.add(new_user)
            await session.commit()


@app.on_event("startup")
async def on_startup():
    await init_db()
    await create_predefined_users()

security = HTTPBasic()

# fake_notes = [
#     {'note_id': 1, 'title': 'abd', 'content': 'xxxxxxxxxxxxx', 'owner_id': 1, 'owner': 'sedutor'},
#     {'note_id': 2, 'title': 'abd2', 'content': 'xyxyxyxyxyxyyxy', 'owner_id': 1, 'owner': 'sedutor'},
#     {'note_id': 3, 'title': 'zzz', 'content': 'rjfhaekrfljвшащ', 'owner_id': 2, 'owner': 'user1'},
#     {'note_id': 4, 'title': 'zz', 'content': 'r3434fhaekrfljвшащ', 'owner_id': 1, 'owner': 'pretto'}
# ]
# predefined_users = {"user1": "password1", "user2": "password2"}


async def get_current_user(credentials: HTTPBasicCredentials = Depends(security), session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(User).filter(User.username == credentials.username))
    user = result.scalars().first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user


# def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
#     unauth_exc = HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Basic"},
#         )
#     username = credentials.username
#     password = credentials.password
#
#     # Проверка наличия пользователя в предустановленном списке
#     if username not in predefined_users or predefined_users[username] != password:
#         raise unauth_exc
#
#
#     # Возвращаем имя пользователя вместо объекта User
#     return {"username": username}
async def check_spelling(text: str):
    url = "https://speller.yandex.net/services/spellservice.json/checkText"
    params = {"text": text}

    async with httpx.AsyncClient() as client:
        response = await client.get(url=url, params=params)
        response.raise_for_status()
        errors = response.json()
        print("Received errors:", errors)

    if errors:
        # Формируем сообщение об ошибке
        error_messages = [f"Ошибка в слове '{error['word']}': {error['s']}" for error in errors]
        raise HTTPException(status_code=400, detail=error_messages)

    return True

# @app.get("/notes/")
# def read_notes(current_user: dict = Depends(get_current_user)):
#     return {'status': 200,
#             "message": f"Hello, {current_user['username']}! Here are your notes.",
#             'body': [note for note in fake_notes if note.get('owner') == current_user['username']]}


@app.get('/notes/', response_model=List[schemas.Note])
async def read_notes(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_session)):
    # return [note for note in fake_notes if note.get('owner_id') == user_id]
    result = await db.execute(select(NoteModel).filter(NoteModel.owner_id == current_user.user_id))
    notes = result.scalars().all()
    return notes


@app.post('/notes/', response_model=schemas.Note)
async def save_note(note: schemas.NoteCreate, db: AsyncSession = Depends(get_async_session), current_user: User = Depends(get_current_user)):
    # db_note = NoteModel(
    #     title=note.title,
    #     content=note.content,
    #     owner_id=current_user.user_id
    # )
    db_note = NoteModel(**note.dict(), owner_id=current_user.user_id)
    await check_spelling(db_note.content)
    db.add(db_note)
    await db.commit()
    await db.refresh(db_note)
    return db_note


# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8000)
