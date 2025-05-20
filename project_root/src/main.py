from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql import desc, asc
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager
from src.models import Base, TaskDB
from src.schemas import TaskCreate, TaskResponse
from src.utils import get_ordering_function

database_url = 'sqlite:///./tasks.db'
engine = create_engine(database_url, connect_args={'check_same_thread': False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print('Создание таблиц в БД...')
    Base.metadata.create_all(bind=engine)
    yield
    print('Выключение приложения')

app = FastAPI(lifespan=lifespan)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/tasks', response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = TaskDB(**task.dict())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@app.get('/tasks/{task_id}', response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail='Задача не найдена')
    return task


@app.put('/tasks/{task_id}', response_model=TaskResponse)
def update_task(task_id: int, updated_task: TaskCreate, db: Session = Depends(get_db)):
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail='Задача не найдена')

    task.title = updated_task.title
    task.description = updated_task.description
    task.status = updated_task.status
    db.commit()
    db.refresh(task)
    return task


@app.delete('/tasks/{task_id}')
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail='Задача не найдена')

    db.delete(task)
    db.commit()
    return {'message': 'Задача удалена'}


@app.get('/tasks', response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db),
              order_by: str = Query('priority', description='Выберите поле для сортировки (поставьте перед названием поля "-", если хотите отсортировать в порядке убывания)')):
    order_func, field_name = get_ordering_function(order_by)

    if not hasattr(TaskDB, field_name):
        raise HTTPException(status_code=400, detail='Данное поле не доступно для сортировки')

    tasks = db.query(TaskDB).order_by(order_func(getattr(TaskDB, field_name))).all()
    return tasks

@app.get('/tasks/top5', response_model=list[TaskResponse])
def get_top5_tasks(db: Session = Depends(get_db)):
    tasks = db.query(TaskDB).order_by(asc(TaskDB.priority), desc(TaskDB.created_at)).limit(5).all()
    return tasks