import httpx

from fastapi import HTTPException
from database import session_maker
from models import User
from hashing import get_password_hash
from sqlalchemy import select


async def create_predefined_users():
    async with session_maker() as session:
        async with session.begin():
            predefined_users = [
                {"username": "user1", "password": "password1"},
                {"username": "user2", "password": "password2"},
            ]

            for user_data in predefined_users:
                result = await session.execute(
                    select(User).filter_by(username=user_data["username"])
                )
                user = result.scalars().first()
                if not user:
                    hashed_password = get_password_hash(user_data["password"])
                    new_user = User(
                        username=user_data["username"], hashed_password=hashed_password
                    )
                    session.add(new_user)
            await session.commit()


async def check_spelling(text: str) -> bool:
    url = "https://speller.yandex.net/services/spellservice.json/checkText"
    params = {"text": text}

    async with httpx.AsyncClient() as client:
        response = await client.get(url=url, params=params)
        response.raise_for_status()
        errors = response.json()
        print("Received errors:", errors)

    if errors:
        error_messages = [
            f"Ошибка в слове '{error['word']}': {error['s']}" for error in errors
        ]
        raise HTTPException(status_code=400, detail=error_messages)

    return True
