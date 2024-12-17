from sqlmodel import create_engine, SQLModel, Session

DB_URL = "postgresql+psycopg2://postgres:password@localhost/dbname"

engine = create_engine(DB_URL, echo=True)

# Создание всех таблиц из models.py
def init_db():
    SQLModel.metadata.create_all(engine)

# Генератор, возвращающий сессию с БД
def get_session():
    with Session(engine) as session:
        yield session