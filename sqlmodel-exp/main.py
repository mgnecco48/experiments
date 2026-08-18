from sqlmodel import SQLModel, Field, Session, create_engine, select
from datetime import date

# TODO: Place the url in a .env file and use python-dotenv to load it
database_url = "postgresql+psycopg://martin@localhost:5432/sqlmodel_db"


class Person(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    last_name: str
    birthday: date


engine = create_engine(database_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# TODO: Make this interactive, for now in the terminal.
def insert_people():
    person_1 = Person(name="Martin", last_name="Gnecco", birthday=date(1997, 9, 26))
    session = Session(engine)
    session.add(person_1)
    session.commit()
    session.refresh(person_1)
    return print(person_1)


def main():
    print("Hello from sqlmodel-exp!")
    create_db_and_tables()
    insert_people()


if __name__ == "__main__":
    main()
