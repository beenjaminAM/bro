import fitz  # PyMuPDF

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
                label_texts_and_urls.add((link_text, uri))
    
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

if __name__ == '__main__':

    name = 'Systematic literature reviews in software engineering – A systematic literature review Kitchenham B. (2009).pdf'
    
    doc = fitz.open(name)
    
    result = extract_link_labes(doc[0])
    for like_label, link in result:
        print(f"{like_label} , url = {link}")