import pytest
from src.utils import get_ordering_function
from sqlalchemy.sql import asc, desc

def test_get_ordering_function_ascending():
    func, field = get_ordering_function('priority')
    assert func == asc
    assert field == 'priority'

def test_get_ordering_function_descending():
    func, field = get_ordering_function('-created_at')
    assert func == desc
    assert field == 'created_at'
    