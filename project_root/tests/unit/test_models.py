from src.schemas import TaskCreate
import pytest

def test_create_task_schema():
    task = TaskCreate(title='Задача', status='в работе', priority=1)
    assert task.title == 'Задача'
    assert task.status == 'в работе'
    assert task.priority == 1

def test_invalid_task_status_type():
    with pytest.raises(ValueError):
        TaskCreate(title='Ошибка', status=123)