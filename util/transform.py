import pandas as pd
import yake

def removing_posts_by_mods (df):
    i = df[df['author'] == 'AutoModerator'].index
    return df.drop(i)

def cleaner (x):
    clean_list = []

    for i in x:
        if type(i) == tuple:
            clean_list.append(i[0])

    return clean_list

def extract_keywords (df):
    df['text'] = df['text'].fillna('<NA>')

    lang = "en"
    max_ngram_size = 1
    deduplication_threshold = 0.9
    num_keywords = 10

    kw = yake.KeywordExtractor(
        lan=lang,
        n=max_ngram_size,
        dedupLim=deduplication_threshold,
        top=num_keywords,
        features=None)

    keywords_text = df['text'].apply(
        lambda x: cleaner(kw.extract_keywords(x)))

    keywords_title = df['title'].apply(
        lambda x: cleaner(kw.extract_keywords(x)))

    df['keywords'] = keywords_text + keywords_title
    df['keywords'] = df['keywords'].apply(lambda x: set(x))

    return df

def transform (input_path, output_path):
    df = pd.read_csv(input_path)

    df = removing_posts_by_mods(df)

    # Changing 'created' column
    df['created'] = pd.to_datetime(df['created'], unit='s')

    df = extract_keywords(df)

    df.to_csv(output_path, index=False)

if __name__ == '__main__':
    input_path = '../output/extracted.csv'
    output_path = '../output/transformed.csv'

    transform(input_path, output_path)
    print('Finished transforming')