def handle(doc, find_limiter, min_pages, direction='backward' ,debbug = False):

        found_page = None

        # Decide the page range based on the direction
        if direction == 'forward':
            page_range = range(doc.page_count)  # From first to last
        else:
            page_range = range(doc.page_count - 1, -1, -1)  # From last to first

        for page_num in page_range:
            page = doc.load_page(page_num)
            text = page.get_text()
            # Debbug purpss
            # print("val ", doc.page_count)
            # print(text)
            if debbug and page_num == min_pages - 1:
                print('Text Context at the page: {min_pages}:', text[:200])
            if find_limiter.lower() in text.lower():
                found_page = page_num + 1  # human-readable page number
                break

        if found_page and found_page >= min_pages:
            return found_page - 1  # return 0-based index
        else:
            return None