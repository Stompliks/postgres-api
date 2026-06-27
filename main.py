from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

def init_db():
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            age INTEGER
        )
    """)
    conn.commit()
    cursor.close()

init_db()

class User(BaseModel):
    name: str
    age: int

@app.post("/users")
def create_user(user: User):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, age) VALUES (%s, %s)", (user.name, user.age))
    conn.commit()
    cursor.close()
    return {"message": f"Пользователь {user.name} создан!"}

@app.get("/users")
def get_users():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    return users
