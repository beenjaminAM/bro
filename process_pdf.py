from loggings import create_logging_errors, create_logging_pdf_list
import os
import polars as pl
from embedding_model import get_embedding
from chunks import chunk_text
from clean_pdf import extract_cleaned_text_until_index_page
from embedding_db import insert_in_collection, create_vector_collection, create_vector_db

def process_pdf_to_embedding(pdf_path, collection_name ,logs_errors_df, logs_pdfs_list):

    result_text, _ = extract_cleaned_text_until_index_page(
        pdf_path=pdf_path,
        filename= os.path.basename(pdf_path).replace(".pdf", ""),
        logs_df=logs_errors_df,
        find_start_limiter = "Introduction",
        start_max_pages=2,
        final_min_pages=8
    )

    if result_text is None:
        raise Exception('pdf limiters error')

    id = 0

    pdf_df = logs_pdfs_list
    if len(pdf_df) > 0:
        id = pdf_df['id'].max()
    
    text_chunks = chunk_text(result_text)
    vectors = get_embedding(text_chunks)
    ids = [f"{id}-{i}" for i in range(len(vectors))]
    metadatas = [{"article": id} for _ in range(len(vectors))]

    insert_in_collection(collection_name, text_chunks, metadatas, ids, vectors)

    filename = os.path.basename(pdf_path).replace(".pdf", "")
    if filename not in logs_pdfs_list['name'].to_list():
        id = id
        description = f"{filename}"
        new_log_row = pl.DataFrame({'id': [id], 'name': [f"{description}"]}, schema={'id': pl.Int64, 'name': pl.Utf8})
        pl.concat([logs_pdfs_list, new_log_row], how="vertical")

if __name__ == '__main__':

    name = 'Systematic literature reviews in software engineering – A systematic literature review Kitchenham B. (2009).pdf'
    
    pdf_path = os.path.join(os.getcwd(), name)
    vector_db = create_vector_db(db_name="vector_db", db_path=os.getcwd())
    test_collection = create_vector_collection(vector_db, "test_collection")

    loggin_df = create_logging_errors("logging_errors", os.path.join(os.getcwd(), "logs"))
    loggin_pdf_df = create_logging_pdf_list("logging_pdf_list", os.path.join(os.getcwd(), "logs"))

    pdf_df = loggin_pdf_df
    
    print('boy 1', len(pdf_df))
    print(len(pdf_df))
    print('boy 2 ', len(pdf_df))
    process_pdf_to_embedding(pdf_path, test_collection, loggin_df, loggin_pdf_df)