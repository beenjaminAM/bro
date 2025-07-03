
def chunk_text(text, chunk_size=200, overlap_size=10):
    # List to store the chunks
    chunks = []
    
    # Start the initial chunk
    start = 0
    end = chunk_size
    
    while start < len(text):
        # Ensure that we don't break words by checking if the chunk ends in the middle of a word
        if end < len(text) and text[end] != ' ':
            # Move `end` back to the nearest space to avoid breaking words
            end = text.rfind(' ', start, end) + 1
            
        # Add the chunk
        chunks.append(text[start:end])
        
        # Set the next chunk's start and end points considering overlap
        start = max(0, end - overlap_size)
        end = start + chunk_size
        
        # If the next chunk goes beyond the text, stop
        if start >= len(text):
            break
    
    return chunks
