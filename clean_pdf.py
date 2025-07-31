import fitz  # PyMuPDF
import polars as pl
import re
from doc_page_limiter import find_final_limiter_page

def extract_link_labes(page, label_texts_and_urls = set()):
    # Extract all links from the page
    links = page.get_links()
    
    # Loop through the links and check for URI
    for link in links:
        if "uri" in link:  # Ensure it is a URI link
            uri = link["uri"]  # Extract the URL
            
            # Extract the rectangle (coordinates) where the link is located
            link_rect = link["from"]
            
            # Extract the text in the rectangle area around the link
            link_text = page.get_text("text", clip=link_rect)
            
            link_text = link_text.strip()
            
            if link_text:
                label_texts_and_urls.add((link_text))
    
    return label_texts_and_urls

def extract_footer_headers(page, header_footer_texts=set()):
    # Define header and footer thresholds based on page height 
    header_threshold = 85  # Text blocks above this Y-position are considered part of the header
    footer_threshold = 45   # Text blocks below this Y-position are considered part of the footer

    # Get all text blocks from the page to identify header and footer content
    blocks = page.get_text("dict")["blocks"]
    
    for block in blocks:
        if block["type"] == 0:  # Only process text blocks
            # Iterate through the lines and spans inside the block
            for line in block["lines"]:
                line_text = ''
                for span in line["spans"]:
                    block_text = span["text"]
                    bbox = span["bbox"]
                    line_text += block_text
                    
                # Check if the block is part of the header (top of the page)
                if bbox[1] < header_threshold:  # Top part of the page
                    if line_text.strip():  # Avoid empty text blocks
                        header_footer_texts.add(line_text.strip())
                
                # Check if the block is part of the footer (bottom of the page)
                elif bbox[3] > page.rect.height - footer_threshold:  # Bottom part of the page
                    if line_text.strip():  # Avoid empty text blocks
                        header_footer_texts.add(line_text.strip())
    return header_footer_texts

def extract_cleaned_text_until_index_page(
    pdf_path: str,
    filename: str,
    logs_df: pl.DataFrame,
    find_limiter: str | None = None,
    min_pages: int | None = None,
) -> tuple[str | None, pl.DataFrame]:
    """
    Extracts cleaned text from a PDF up to a specific index page. Removes
    headers, footers, and link labels. Logs any files that don't have a valid index page.

    Parameters
    ----------
    pdf_path : str
        Full path to the PDF file.
    filename : str
        Name of the file (used for logging).
    logs_df : pl.DataFrame
        DataFrame containing logs of previously unprocessed files.

    Returns
    -------
    tuple[str | None, pl.DataFrame]
        - Cleaned text extracted from the document (or None if skipped).
        - Updated logs DataFrame.
    """
    doc = fitz.open(pdf_path)

    if find_limiter or min_pages:
        if min_pages is None:
            index_page, limiter = find_final_limiter_page(doc, find_limiter=find_limiter)
        elif find_limiter is None:
            index_page, limiter = find_final_limiter_page(doc, min_pages=min_pages)
        else:
            index_page, limiter = find_final_limiter_page(doc, find_limiter=find_limiter, min_pages=min_pages)

    else:
        index_page, limiter = find_final_limiter_page(doc)
                

    if index_page is None:
        if filename not in logs_df['name'].to_list():
            new_log_row = pl.DataFrame({'name': [filename]}, schema={'name': pl.Utf8})
            logs_df = pl.concat([logs_df, new_log_row], how="vertical")
        print(f"No index page found for {filename}")
        return None, logs_df

    clean_text = ''

    for page_num in range(doc.page_count):
        if page_num > index_page:
            break

        page = doc.load_page(page_num)
        link_labels = extract_link_labes(page, set())
        header_footers = extract_footer_headers(page, set())
        raw_text = page.get_text()

        if page_num == index_page and limiter:
            limiter_index = raw_text.lower().find(limiter.lower())
            if limiter_index != -1:
                raw_text = raw_text[:limiter_index]

        for unwanted in link_labels | header_footers:
            raw_text = raw_text.replace(unwanted, '')

        clean_text += raw_text

    clean_text = re.sub(r'\s+', ' ', clean_text)
    clean_text = re.sub(r'\n+', '\n', clean_text)
    clean_text = clean_text.strip()

    return clean_text, logs_df

if __name__ == '__main__':

    name = 'Systematic literature reviews in software engineering – A systematic literature review Kitchenham B. (2009).pdf'
    
    doc = fitz.open(name)
    
    test_set = set()
    for page_num in range(doc.page_count):
        extract_link_labes(doc[page_num], test_set)
    
    for like_label in test_set:
        print(f"Link Label: {like_label}")

    print("Header and Footer Content")
    result = extract_footer_headers(doc[0])
    for h_f_content in result:
        print(h_f_content)

    # Create an empty Polars DataFrame for logs
    logs_df = pl.DataFrame(schema={'name': pl.Utf8})
    
    # Call the function
    result_text, updated_logs = extract_cleaned_text_until_index_page(
        pdf_path=name,
        filename=name.replace(".pdf", ""),
        logs_df=logs_df,
        min_pages=9
    )

    # Print results
    print("\n--- Cleaned Text ---\n")
    print(result_text[1000])  # Print only the first 1000 characters to avoid overload
    print("\n--- Logs DataFrame ---\n")
    print(updated_logs)