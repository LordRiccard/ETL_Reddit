from sqlalchemy import Column, Integer, String, create_engine, Engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.types import Text, DateTime
from dotenv import load_dotenv
import os
import csv

base = declarative_base()

class Posts(base):
    """
    Object Relational Mapping used to create the
    'posts' table inside MySQL database
    """
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    author = Column(String(50))
    title = Column(String(300))
    score = Column(Integer)
    url = Column(String(300))
    text = Column(Text)
    num_comments = Column(Integer)
    flair = Column(String(50))
    created = Column(DateTime)
    keywords = Column(Text)

def get_engine () -> Engine:
    """
    Creates an engine instance using
    "sql_connection_string" from .env.
    The engine is tied to redditdb
    returns:
        Engine: The engine instance
    """
    load_dotenv()
    return create_engine(os.getenv("sql_connection_string")
                           + 'redditdb')

def create_table (engine: Engine) -> None:
    """
    Creates 'posts' table inside MySQL database
    param:
        engine (Engine): The engine linked to a
                         MySQL database
    """
    base.metadata.create_all(engine)

def insert_from_file (engine: Engine, input_path: str) -> None:
    """
    Insert rows from a csv into a database

    param:
        engine (Engine): The engine used
        input_path (str): The path to the file
    """
    with open(input_path, encoding='utf-8', newline='\n') as csv_file:
        csvreader = csv.DictReader(csv_file, quotechar='"')

        posts = [Posts(**row) for row in csvreader]

        Session = sessionmaker(bind=engine)
        session = Session()
        session.add_all(posts)
        session.commit()

def load (input_path: str) -> None:
    """
    Creates an engine instance with get_engine()
    Creates the table needed using create_table()
    Insert the data in the db with insert_from_file()
    """
    engine = get_engine()
    create_table(engine)
    insert_from_file(engine, input_path)

if __name__ == '__main__':
    input_file = '../output/transformed.csv'

    load(input_file)
    print('Finished Loading')