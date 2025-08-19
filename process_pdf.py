from loggings import create_logging_errors
import os
from vectorize_text import vectorize_text
from clean_pdf import extract_cleaned_text_until_index_page
from vector_db import insert_in_collection


def process_pdf_to_embedding(pdf_path, collection_name ,logs_errors_df, logs_pdfs_list):

    # Call the function
    result_text, updated_logs = extract_cleaned_text_until_index_page(
        pdf_path=pdf_path,
        filename= os.path.basename(pdf_path).replace(".pdf", ""),
        logs_df=logs_errors_df,
        find_start_limiter = "Introduction",
        start_max_pages=2,
        final_min_pages=8
    )

    if result_text is None:
        raise Exception('pdf limiters error')
    
    vectors = vectorize_text(result_text)



if __name__ == '__main__':

    pass