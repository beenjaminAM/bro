import chromadb.utils.embedding_functions as embedding_functions

openai_key = "secret"

def get_embedding(texts):
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                    api_key=f"{openai_key}",
                    model_name="text-embedding-3-large"
                )
    vectors = openai_ef(texts)
    return vectors

if __name__ == "__main__":
    # Test the function
    vectors = get_embedding(['peru', 'papa', 'altura'])
    for vector in vectors:
        print(vector)
        print(type(vector))
        print(vector.shape)
        print()

    # The vector is one-dimensional in terms of how the data is stored, but it actually represents a point or direction in a space with 3072 dimensions.
    # [-0.02918763 -0.00644085  0.00512822 ...  0.02002369  0.00507522 0.01474057]
    # <class 'numpy.ndarray'>
    # (3072,)