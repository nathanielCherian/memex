import os

dirname = os.path.dirname(__file__)
def remove_db():
    os.remove( os.path.join(dirname, 'example.db'))