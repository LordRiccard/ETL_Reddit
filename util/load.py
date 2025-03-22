from sqlalchemy import Column, Date, Float, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.types import Text, DateTime
from dotenv import load_dotenv
import os
import pandas as pd
import csv

base = declarative_base()
class Posts(base):
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

def get_engine ():
    load_dotenv()
    return create_engine(os.getenv("sql_connection_string")
                           + 'redditdb')

def create_table (engine):
    base.metadata.create_all(engine)

def load_from_file (engine, input_path):
    #df = pd.read_csv('../output/transformed.csv')
    Session = sessionmaker(bind=engine)

    with open(input_path, encoding='utf-8', newline='\n') as csv_file:
        csvreader = csv.DictReader(csv_file, quotechar='"')

        posts = [Posts(**row) for row in csvreader]

        session = Session()
        session.add_all(posts)
        session.commit()

def load (input_path):
    engine = get_engine()
    create_table(engine)
    load_from_file(engine, input_path)

if __name__ == '__main__':
    input_path = '../output/transformed.csv'

    load(input_path)