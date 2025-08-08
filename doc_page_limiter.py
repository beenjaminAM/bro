import fitz

def handlerigth(doc, find_limiter, max_pages, direction='backward' ,debug = False):

        matched_page_index = None

        # Decide the page range based on the direction
        if direction == 'forward':
            # Range from first page to the max page (max_pages - 1) (inclusive)
            page_range = range(0, max_pages)
        else:
            # Range in reverse from the max page (max_pages - 1) to the first page 0 (inclusive)
            page_range = range(max_pages - 1, -1, -1)

        for page_num in page_range:
            page = doc.load_page(page_num)
            text = page.get_text()
            if debug and page_num == max_pages - 1:
                print(f'Text Context at the page: {max_pages}:', text[:200])
            if find_limiter.lower() in text.lower():
                matched_page_index = page_num
                break

        if matched_page_index is not None and matched_page_index <= max_pages - 1:
            return matched_page_index# return 0-based index
        else:
            return None


def handleleft(doc, find_limiter, min_pages, direction='backward' ,debug = False):
        matched_page_index = None

        # Decide the page range based on the direction
        if direction == 'forward':
            # Range from (min_pages - 1) to the last page n
            page_range = range(min_pages - 1, doc.page_count)
        else:
            # Range in reverse from the last page (n -1) to (min_pages - 1) (inclusive)
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
                matched_page_index = page_num
                break

        if matched_page_index is not None and matched_page_index >= min_pages - 1:
            return matched_page_index# return 0-based index
        else:
            return None
        
def find_start_limiter_page(doc, find_limiter='introduction', max_pages = 3):

    limiter = find_limiter
    result = None
    if find_limiter == 'introduction':
        result = handlerigth(doc, find_limiter, max_pages)
        if result is not None:
            limiter = 'introduction'
    else:
        # Custom cleaning
        result = handlerigth(doc, find_limiter, max_pages, True)
        if result:
            limiter = find_limiter.replace('\n', '').strip()
    return result, limiter


def find_final_limiter_page(doc, find_limiter='\nreferences', min_pages = 10):
    limiter = find_limiter
    result = None
    if find_limiter == '\nreferences':
        result_ref = handleleft(doc, find_limiter, min_pages)
        result_app = handleleft(doc, 'Appendix A', min_pages)
        
        if result_ref and result_app:
            result = min(result_ref, result_app)
            limiter = 'Appendix A' if result == result_app else 'references'
        elif result_app:
            result, limiter = result_app, 'Appendix A'
        elif result_ref:
            result, limiter = result_ref, 'references'
    else:
        # Custom cleaning using a word delimiter such as 5. References, 10. Literatur, or Appendix 1
        # The delimiter should appear on or after the page number specified by min_pages (min_pages, min_pages + 1, min_pages + 2)
        result = handleleft(doc, find_limiter, min_pages, 'forward', True)
        if result:
            limiter = find_limiter.replace('\n', '').strip()
    return result, limiter
        
if __name__ == '__main__':
    name = 'Systematic literature reviews in software engineering – A systematic literature review Kitchenham B. (2009).pdf'
    doc = fitz.open(name)

    # --- Test 1: Search for "References" from page 9 backward ---
    find_limiter = "References"
    min_pages = 9
    direction = 'backward'
    debug = True

    print(f"\n1 Running handleleft test: '{find_limiter}' | Direction: {direction} | From page: {min_pages}")
    limiter_page_index = handleleft(doc, find_limiter, min_pages, direction=direction, debug=debug)
    print(f"Page limiter for '{find_limiter}': {limiter_page_index} (0-based index)")

    # --- Test 2: Search for "introduction" from page 1 backward ---
    find_limiter = "Introduction"
    max_pages = 3
    direction = 'backwards'
    debug = True

    print(f"\n2 Running handlerigth test: '{find_limiter}' | Direction: {direction} | From page: {max_pages}")
    limiter_page_index = handlerigth(doc, find_limiter, max_pages, direction=direction, debug=debug)
    print(f"Page limiter for '{find_limiter}': {limiter_page_index} (0-based index)")

    # --- Test 3: find_final_limiter_page(doc, find_limiter='\nreferences', min_pages = 9)
    find_limiter = "\nreferences"
    min_pages = 9

    print(f"\n3 Running find_final_limiter_page test: '{find_limiter}' | From page: {min_pages}")
    index_page, limiter = find_final_limiter_page(doc, find_limiter=find_limiter, min_pages=min_pages)
    print(f"Limiter '{limiter}' found on page index: {index_page}")

    # --- Test 4: find_limiter_page(doc)
    find_limiter = "\nreferences"
    min_pages = 10
    print(f"\n4 Running find_final_limiter_page test: '{find_limiter}' | From default option page: {min_pages}")
    index_page, limiter = find_final_limiter_page(doc)
    print(f"Limiter '{limiter}' found on page index: {index_page}")
    
    # --- Test 5: find_start_limiter_page(doc)
    find_limiter = "Introduction"
    max_pages = 3
    direction = 'backwards'
    debug = True
    print(f"\n5 Running find_start_limiter_page default test: '{find_limiter}' | From page: {max_pages}")
    index_page, limiter = find_start_limiter_page(doc)
    print(f"Limiter '{limiter}' found on page index: {index_page}")

    # --- Test 6: find_start_limiter_page(doc, find_limiter='Method', max_pages = 2)
    find_limiter = "Method"
    max_pages = 2
    direction = 'backwards'
    debug = True
    print(f"\n5 Running find_start_limiter_page test: '{find_limiter}' | From page: {max_pages}")
    index_page, limiter = find_start_limiter_page(doc, find_limiter=find_limiter)
    print(f"Limiter '{limiter}' found on page index: {index_page}")
