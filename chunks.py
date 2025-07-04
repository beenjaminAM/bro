
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


if __name__ == "name":
    # Test the function
    input_text = "there is no comprehensive review for a holistic understanding of how NLP is being adopted by governments. In this regard, we present a systematic literature review on NLP applications in governments by following the Preferred Reporting Items for Systematic Reviews and Meta-Analyses (PRISMA) protocol. there is no comprehensive review for a holistic understanding of how NLP is being adopted by governments. In this regard, we present a systematic literature review on NLP applications in governments by following the Preferred Reporting Items for Systematic Reviews and Meta-Analyses (PRISMA) protocol. there is no comprehensive review for a holistic understanding of how NLP is being adopted by governments. In this regard, we present a systematic literature review on NLP applications in governments by following the Preferred Reporting Items for Systematic Reviews and Meta-Analyses (PRISMA) protocol. there is no comprehensive review for a holistic understanding of how NLP is being adopted by governments. In this regard, we present a systematic literature review on NLP applications in governments by following the Preferred Reporting Items for Systematic Reviews and Meta-Analyses (PRISMA) protocol. "
    chunks = chunk_text(input_text)
    for chunk in chunks:
        print(f"'{chunk}'\n")