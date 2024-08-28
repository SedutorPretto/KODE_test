from fastapi import FastAPI
from database import async_engine, async_session
from models import Base

async with async_engine.begin() as conn:
    conn.run_sync(Base.metadata.create_all)

app = FastAPI()


@app.get('/')
def hello():
    return 'Hello World'
