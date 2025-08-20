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

    pass