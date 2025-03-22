from util.extract import extract
from util.transform import transform
from util.load import load

if __name__ == '__main__':
    extracted_path = 'output/extracted.csv'
    transformed_path = 'output/transformed.csv'

    extract(extracted_path)
    transform(extracted_path, transformed_path)
    load(transformed_path)

    print('Finished.')