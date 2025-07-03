import fitz  # PyMuPDF

def extract_link_labes(page, label_texts_and_urls = set()):
    links = page.get_links()
    
    for link in links:
        if "uri" in link:  
            uri = link["uri"]  
            
            link_rect = link["from"]
            
            link_text = page.get_text("text", clip=link_rect)
            
            link_text = link_text.strip()
            
            if link_text:
                label_texts_and_urls.add((link_text, uri))
    
    return label_texts_and_urls