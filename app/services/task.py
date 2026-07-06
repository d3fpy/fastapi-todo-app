from sqlalchemy.orm import Session
from app.repositories.task import TaskRepository
from app.schemas.task import TaskSchema, TaskCreateSchema,TaskUpdateSchema 

class TaskNotFound(Exception):
    """Задача не найдена в БД"""


class TaskService:
    def __init__(self,db: Session) -> None:
        self.db = db
        self.task_repository = TaskRepository(db)

    def list_tasks(self) -> list[TaskSchema]:
        tasks_orm = self.task_repository.get_all()
        return [TaskSchema.model_validate(task) for task in tasks_orm] 

    def create_task(self, task_create: TaskCreateSchema) -> TaskSchema:
      task_orm = self.task_repository.create(title=task_create.title)
      self.db.commit()
      return TaskSchema.model_validate(task_orm)

    def update_task(self, task_id: TaskUpdateSchema) -> TaskSchema:
        tasks_for_update = self.task_repository.get_by_id(task_id=task_id)
        if not tasks_for_update:

            raise TaskNotFound(f"Задача c {task_id} не найдена")
        if tasks_for_update.title:
            tasks_for_update.title = tasks_for_update.title
        if tasks_for_update.completed:
            tasks_for_update.completed = tasks_for_update.completed
        self.db.commit()
        return TaskSchema.model_validate(tasks_for_update)

    def delete_task(self, task_id: str) -> TaskSchema:
        task_for_delete = self.task_repository.get_by_id(task_id=task_id)
        if not task_for_delete:
            raise TaskNotFound(f"Задача c {task_id} не найдена")
        
        self.task_repository.delete(task_for_delete)