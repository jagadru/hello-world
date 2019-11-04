from app.domain.price import (
    MAX_OFFSET,
    MAX_PAGE,
    PAGE,
)

def valid_offset(offset):
    if offset < 0 or \
        offset > MAX_OFFSET or \
        type(offset) is type(int):
            return False
    return True

def valid_page(page):
    if not page or page == 0 or \
        page < 0 or \
        page > MAX_PAGE or \
        type(page) is type(int):
            return False
    return True

def validate_offset_page(offset, page):
    if not offset and not page:
        offset = MAX_OFFSET
        page = PAGE
    elif offset or page:
        if not valid_offset(offset):
            offset = MAX_OFFSET

        if not valid_page(page):
            page = PAGE

    elif not offset or page:
        offset = MAX_OFFSET
        if not valid_page(page):
                page = PAGE

    elif offset or not page:
        if not valid_offset(offset):
            offset = MAX_OFFSET

        page = PAGE

    return offset, page
