from sqlmodel import SQLModel, Field
from pydantic import BaseModel
from typing import Annotated

# Базовый класс товаров, опираясь на который будут выполняться любые операции в коде
class ItemBase(SQLModel):
    name: str
    description: str | None = None
    price: float
    tax: float | float = 0.30

# Класс, на основе которого будет создана таблица в нашеё БД с идентичным имени классу названием
class Item(ItemBase, table=True):
    id: int = Field(primary_key=True)

# Класс, используемый для POST-запросов
class ItemCreate(ItemBase):
    pass

# Класс, используемый для PATCH-запросов
class ItemUpdate(ItemBase):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    tax: float | float = 0.30