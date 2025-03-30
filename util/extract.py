import praw
import os
from dotenv import load_dotenv
import pandas as pd
from praw.models import Subreddit

def setup_praw () -> praw.Reddit:
    """
    Establishes a connection with reddit.
    Utilizes client_id, client_secret and user_agent from .env

    returns:
        praw.Reddit: Instance connected to reddit
    """
    load_dotenv()

    return praw.Reddit(client_id = os.getenv("client_id"),
                       client_secret = os.getenv("client_secret"),
                       user_agent = os.getenv("user_agent"))

def get_data (subreddit: Subreddit) -> pd.DataFrame:
    """
    Collect posts from the hot section of a subreddit.
    The info gathered: Post's author, title,
    score (thumbs up - thumbs down), url, body
    (written text), num. of comments, flair and
    time created

    param:
        subreddit (Subreddit): The chosen subreddit
    returns:
        pd.DataFrame: Data collected
    """
    list_author = []
    list_title = []
    list_score = []
    list_url = []
    list_text = []
    list_num_comments = []
    list_flair_text = []
    list_created = []

    for submission in subreddit.hot(limit=5000):
        list_author.append(submission.author)
        list_title.append(submission.title)
        list_score.append(submission.score)
        list_url.append(submission.url)
        list_text.append(submission.selftext.replace('\n', ' '))
        list_num_comments.append(submission.num_comments)
        list_flair_text.append(submission.link_flair_text)
        list_created.append(submission.created_utc)

    data = {
        'author': list_author,
        'title': list_title,
        'score' : list_score,
        'url' : list_url,
        'text': list_text,
        'num_comments' : list_num_comments,
        'flair' : list_flair_text,
        'created' : list_created
    }

    return pd.DataFrame(data)

def extract (output_path: str) -> None:
    """
    Starts a praw instance with setup_praw() and
    uses it to extract data with get_data(). At
    the end saves the data collected on a csv file

    param:
        output_path (str): String with a file path
    """
    reddit = setup_praw()
    subreddit = reddit.subreddit('explainlikeimfive')

    df = get_data(subreddit)
    df.to_csv(output_path, index=False)

if __name__ == '__main__':
    output_file = '../output/extracted.csv'
    extract(output_file)
    print('Finished extracting')