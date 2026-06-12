from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import Depends, FastAPI, status
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, sessionmaker, mapped_column

DATABASE_URL = "_"

engine = create_engine(DATABASE_URL)
Sessionlocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(
        primary_key=True, default=lambda: str(uuid4()))


class TaskORM(Base):
    __tablename__ = 'tasks'

    title: Mapped[str]
    completed: Mapped[bool] = mapped_column(default=False)


class CategoriesORM(Base):
    __tablename__ = 'categories'

    name: Mapped[str]


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=["*"]
)


class TaskSchema(BaseModel):
    id: str
    title: str
    completed: bool


class TaskCreateSchema(BaseModel):
    title: str


class TaskUpdateSchema(BaseModel):
    title: str | None = None
    completed: bool | None = None


class CategorySchema(BaseModel):
    id: str
    name: str


class CategoryCreateSchema(BaseModel):
    name: str


class CategoryUpdateSchema(BaseModel):
    name: str

tasks: list[TaskSchema] = []
categories: list[CategorySchema] = []

def get_db():
    db = Sessionlocal()
    
    try:
        yield db
    finally:
        db.close()

def task_orm_to_model(task_orm: TaskORM) -> TaskSchema:
    return TaskSchema(id=task_orm.id,title= task_orm.title, completed=task_orm.completed)


def categories_orm_to_model(categories_orm: CategoriesORM) -> CategorySchema:
    return CategorySchema(id=categories_orm.id, name=categories_orm.name)


@app.get("/tasks")
def read_tasks(db: Session = Depends(get_db)) -> list[TaskSchema]:
   tasks_from_db = db.scalars(select(TaskORM)).all()
   return [task_orm_to_model(task) for task in tasks_from_db]


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreateSchema, db: Session = Depends(get_db)) -> TaskSchema:
    new_task = TaskORM(title=payload.title, completed=False)
    db.add(new_task)
    db.commit()

    tasks.append(new_task)
    return task_orm_to_model(new_task)


@app.patch("/tasks/{task_id}")
def update_task(task_id: str, payload: TaskUpdateSchema, db: Session = Depends(get_db)) -> TaskSchema:
    task_for_update = db.get(TaskORM,task_id)
    if payload.title:
        task_for_update.title = payload.title
    if payload.completed:
        task_for_update.completed = payload.completed

    db.commit()
    return task_for_update

# e94e841d-8e15-491f-aac0-21957bf8d018
@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id, db: Session = Depends(get_db)) -> None:
    task_for_delete = db.get(TaskORM,task_id)
    db.delete(task_for_delete)
    db.commit()


#### categories

@app.get("/categories")
def read_categories(db: Session = Depends(get_db)) -> list[CategorySchema]:
   category_from_db = db.scalars(select(CategoriesORM)).all()
   return [categories_orm_to_model(category) for category in category_from_db]


@app.post("/categories", status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreateSchema, db: Session = Depends(get_db)) -> CategorySchema:
    new_category = CategoriesORM(name=payload.name)
    db.add(new_category)
    db.commit()

    categories.append(new_category)
    return categories_orm_to_model(new_category)



@app.patch("/categories/{id}")
def update_category(id: str, payload: CategoryUpdateSchema, db: Session = Depends(get_db)) -> CategorySchema:
    category_for_update = db.get(CategoriesORM, id)
    if payload.name:
        category_for_update.name = payload.name

    db.commit()
    return category_for_update

# de75b240-5e2c-4037-ba8c-0e58a856fd7b
@app.delete("/categories/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(id, db: Session = Depends(get_db)) -> None:
    category_for_delete = db.get(CategoriesORM, id)
    db.delete(category_for_delete)
    db.commit()
