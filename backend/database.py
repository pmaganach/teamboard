from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy import inspect, text

import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=False)


def create_db():
    SQLModel.metadata.create_all(engine)
    try:
        inspector = inspect(engine)
        if "trabajo" in inspector.get_table_names():
            columns = [col["name"] for col in inspector.get_columns("trabajo")]
            if "responsables_ids" not in columns:
                with Session(engine) as session:
                    session.exec(text("ALTER TABLE trabajo ADD COLUMN responsables_ids VARCHAR;"))
                    session.commit()
                print("Database migrated: added column 'responsables_ids' to table 'trabajo'.")
    except Exception as e:
        print(f"Error checking/migrating database schema: {e}")


def get_session():
    with Session(engine) as session:
        yield session
