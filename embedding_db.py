import chromadb
import chromadb.utils.embedding_functions as embedding_functions
import os


def create_vector_db(db_name, db_path):

    db_path = os.path.join(db_path, db_name)
    chroma_client = chromadb.PersistentClient(path=db_path)
    return chroma_client

def create_vector_collection(vector_db, collection_name):
    try:
        collection = vector_db.get_collection(name=collection_name)
        print(f"Collection '{collection_name}' loaded successfully.")
    except chromadb.errors.NotFoundError:
        collection = vector_db.create_collection(name=collection_name)
        print(f"Collection '{collection_name}' created successfully.")

    return collection

def insert_in_collection(collection, texts_list, metadatas, ids, vectors):
    collection.add(
        documents=texts_list,
        metadatas=metadatas,
        ids=ids,
        embeddings=vectors
    )


if __name__ == "__main__":
    # Test the function
    vector_db = create_vector_db(db_name="vector_db", db_path=os.getcwd())
    test_collection = create_vector_collection(vector_db, "test_collection")