import os


PROCESSED_DIR = os.path.join(os.path.dirname(__file__), 'processed')


def get_processed_data_file(name):
    return os.path.join(PROCESSED_DIR, name)
