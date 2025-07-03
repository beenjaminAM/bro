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

if __name__ == '__main__':

    name = 'Systematic literature reviews in software engineering – A systematic literature review Kitchenham B. (2009).pdf'
    
    doc = fitz.open(name)
    
    result = extract_link_labes(doc[0])
    for like_label, link in result:
        print(f"{like_label} , url = {link}")