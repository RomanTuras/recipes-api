from typing import Optional, List, TYPE_CHECKING

# from typing import Any
from sqlmodel import Field, SQLModel, Relationship
from src.domain.neon_models.recipe_ingredient_link import RecipeIngredientLink
# from sqlalchemy import Column
# from sqlalchemy.dialects.postgresql import TSVECTOR
# from sqlalchemy.event import listen
# from sqlalchemy.schema import DDL

if TYPE_CHECKING:
    from src.domain.neon_models.category import Category
    from src.domain.neon_models.ingredient import Ingredient
    from src.domain.neon_models.user import User


class Recipe(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True, nullable=False)
    text: str = Field(default=None, nullable=True)
    image: str = Field(default=None, nullable=True)
    is_favorite: bool = Field(default=False)
    cook_it: bool = Field(default=False)

    user_id: Optional[int] = Field(default=None, foreign_key="user.id")  # FK
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")  # FK

    # Нове поле для повнотекстового пошуку
    # Воно буде автоматично генеруватися базою даних
    # search_vector: Any = Field(
    #     sa_column=Column(
    #         TSVECTOR,
    #         # Використовуємо to_tsvector для генерації вектора з полів title та text
    #         server_default="to_tsvector('ukrainian', '')",
    #         server_onupdate=
    #         "to_tsvector('ukrainian', coalesce(title, '') || ' ' || coalesce(text, ''))",
    #         nullable=False
    #     )
    # )

    category: Optional["Category"] = Relationship(back_populates="recipes")
    user: Optional["User"] = Relationship(back_populates="recipes")
    ingredients: List["Ingredient"] = Relationship(
        back_populates="recipes", link_model=RecipeIngredientLink
    )


# Додатковий код для створення GIN індексу
# SQLAlchemy/SQLModel не підтримує GIN індекси "з коробки",
# тому їх потрібно створювати вручну.
# listen(
#     Recipe.__table__,
#     "after_create",
#     DDL("CREATE INDEX ix_recipe_search ON recipe USING GIN(search_vector);")
# )


# Usage
# Приклад пошукового запиту
# query_term = "борщ"
# with Session(engine) as session:
#     # Використовуємо text() для SQL виразу
#     stmt = select(Recipe).where(
#         sa_text(f"search_vector @@ to_tsquery('ukrainian', '{query_term}')")
#     )
#     results = session.exec(stmt).all()
