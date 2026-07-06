from sqlalchemy.orm import Session
from app.repositories.category import CategoriesRepository
from app.schemas.category import CategorySchema, CategoryCreateSchema,CategoryUpdateSchema


class CategoryNotFound(Exception):
    """Категория не найдена в БД"""



class CategoryService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.category_repository = CategoriesRepository(db)

    def list_catigories(self) -> list[CategorySchema]:
        categories_orm = self.category_repository.get_all()
        return [CategorySchema.model_validate(category) for category in categories_orm]

    def create_category(self, category_create: CategoryCreateSchema) -> CategorySchema:
      category_orm = self.category_repository.create(title=category_create.title)
      self.db.commit()
      return CategorySchema.model_validate(category_orm)

    def update_category(self, category_id: CategoryUpdateSchema) -> CategorySchema:
        categories_for_update = self.category_repository.get_by_id(
            category_id=category_id)
        if not categories_for_update:
            raise CategoryNotFound(f"Категория c {category_id} не найдена")

        if categories_for_update.title:
            categories_for_update.title = categories_for_update.title
        if categories_for_update.completed:
            categories_for_update.completed = categories_for_update.completed
        self.db.commit()

        return CategorySchema.model_validate(categories_for_update)

    def delete_category(self, category_id: str) -> CategorySchema:
        categories_for_delete = self.category_repository.get_by_id(
            category_id=category_id)
        if not categories_for_delete:
            raise CategoryNotFound(f"Категория c {category_id} не найдена")
        
        self.category_repository.delete(categories_for_delete)