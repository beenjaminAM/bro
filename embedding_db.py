import chromadb
import chromadb.utils.embedding_functions as embedding_functions
import os


def create_vector_db(db_name, db_path):

    db_path = os.path.join(db_path, db_name)
    chroma_client = chromadb.PersistentClient(path=db_path)
    return chroma_client

