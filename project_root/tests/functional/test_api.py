import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.main import app, get_db
from src.models import Base


TEST_DB_URL = 'sqlite:///./test.db'
engine = create_engine(TEST_DB_URL, connect_args={'check_same_thread': False})
TestingSession = sessionmaker(bind=engine)

def override_get_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(autouse=True)
def setup():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def test_create_task():
    response = client.post('/tasks', json={
        'title': 'Тест',
        'description': 'Описание',
        'status': 'в работе',
        'priority': 1
    })
    assert response.status_code == 200
    assert response.json()['title'] == 'Тест'
    assert response.json()['status'] == 'в работе'

def test_get_task():
    r = client.post('/tasks', json={'title': 'Получить'})
    task_id = r.json()['id']
    get_r = client.get(f'/tasks/{task_id}')
    assert get_r.status_code == 200
    assert get_r.json()['title'] == 'Получить'

def test_get_all_tasks():
    client.post('/tasks', json={'title': 'Task1', 'priority': 2})
    client.post('/tasks', json={'title': 'Task2', 'priority': 1})
    response = client.get('/tasks')
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_get_top5_tasks():
    for i in range(10):
        client.post('/tasks', json={
            'title': f'Task{i}',
            'description': 'Description{i}',
            'status': 'в ожидании',
            'priority': i
        })
    response = client.get('/tasks/top5')
    assert response.status_code == 200
    assert len(response.json()) == 5
    assert response.json()[0]['priority'] == 0


def test_update_task():
    response = client.post('/tasks', json={'title': 'Old', 'status': 'в ожидании'})
    task_id = response.json()['id']
    upd = client.put(f'/tasks/{task_id}', json={'title': 'New', 'status': 'в работе', 'description': 'update', 'priority': 1})
    assert upd.status_code == 200
    assert upd.json()['title'] == 'New'
    assert upd.json()['status'] == 'в работе'


def test_delete_task():
    response = client.post('/tasks', json={'title': 'Delete'})
    task_id = response.json()['id']
    del_resp = client.delete(f'/tasks/{task_id}')
    assert del_resp.status_code == 200
    assert del_resp.json()['message'] == 'Задача удалена'


def test_invalide_sort_field():
    response = client.get('/tasks?order_by=unknown')
    assert response.status_code == 400
    assert response.json()['detail'] == 'Данное поле не доступно для сортировки'


def test_get_task_not_found():
    response = client.get('/tasks/999')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Задача не найдена'


def test_update_task_not_found():
    response = client.put('/tasks/999', json={'title': 'X', 'status': 'в работе', 'description': '', 'priority': 1})
    assert response.status_code == 404
    assert response.json()['detail'] == 'Задача не найдена'


def test_delete_task_not_found():
    response = client.delete('/tasks/999')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Задача не найдена'