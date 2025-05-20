from sqlalchemy.sql import asc, desc

def get_ordering_function(order_by: str):
    if order_by.startswith('-'):
        return desc, order_by[1:]
    return asc, order_by