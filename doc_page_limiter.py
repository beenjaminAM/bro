import fitz

def handle(doc, find_limiter, min_pages, direction='backward' ,debug = False):

        found_index_page = None

        # Decide the page range based on the direction
        if direction == 'forward':
            # Iterate pages from (min_pages - 1) to the last page (inclusive)
            page_range = range(min_pages - 1, doc.page_count)
        else:
            # Iterate pages in reverse from the last page to (min_pages - 1) (inclusive)
            page_range = range(doc.page_count - 1, min_pages - 2, -1)

        for page_num in page_range:
            page = doc.load_page(page_num)
            text = page.get_text()
            # Debug purpss
            # print("val ", doc.page_count)
            # print(text)
            if debug and page_num == min_pages - 1:
                print(f'Text Context at the page: {min_pages}:', text[:200])
            if find_limiter.lower() in text.lower():
                found_index_page = page_num
                break

        if found_index_page is not None and found_index_page >= min_pages - 1:
            return found_index_page# return 0-based index
        else:
            return None
        
if __name__ == '__main__':
    name = 'Systematic literature reviews in software engineering – A systematic literature review Kitchenham B. (2009).pdf'
    doc = fitz.open(name)

    # --- Test 1: Search for "References" from page 9 backward ---
    find_limiter = "References"
    min_pages = 9
    direction = 'backward'
    debug = True

    print(f"\nRunning test: '{find_limiter}' | Direction: {direction} | From page: {min_pages}")
    limiter_page_index = handle(doc, find_limiter, min_pages, direction=direction, debug=debug)
    print(f"Page limiter for '{find_limiter}': {limiter_page_index} (0-based index)")

    # --- Test 2: Search for "introduction" from page 1 forward ---
    find_limiter = "introduction"
    min_pages = 1
    direction = 'forward'
    debug = True

    print(f"\nRunning test: '{find_limiter}' | Direction: {direction} | From page: {min_pages}")
    limiter_page_index = handle(doc, find_limiter, min_pages, direction=direction, debug=debug)
    print(f"Page limiter for '{find_limiter}': {limiter_page_index} (0-based index)")
