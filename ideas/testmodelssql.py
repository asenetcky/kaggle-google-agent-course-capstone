import os

from dotenv import load_dotenv
from sqlmodel import Session, SQLModel, create_engine

from toddle_ops.models.projects import Material, Project

load_dotenv()


db_url = os.getenv("SUPABASE_CONN_STRING")

sqlite_url = db_url

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def creates_projects():
    with Session(engine) as session:
        test_material01 = Material(
            name="test_material01", quantity=6, units="test_units"
        )
        test_material02 = Material(
            name="test_material01", quantity=6, units="test_units"
        )

        test_project = Project(
            name="test_project01",
            description="this project isn't real, nothing is real.",
            duration_minutes=90,
            instructions="1. step 1, step 2. step 2, 3. step 3",
        )

        session.add(test_material01)
        session.add(test_material02)
        session.commit()

        session.refresh(test_material01)
        session.refresh(test_material02)

        test_material01.project = test_project
        test_material02.project = test_project
        session.add(test_material01)
        session.add(test_material02)
        session.commit()
        session.refresh(test_material01)
        session.refresh(test_material02)

        session.add(test_project)
        session.commit()
        session.refresh(test_project)


def main():
    create_db_and_tables()
    creates_projects()


main()
