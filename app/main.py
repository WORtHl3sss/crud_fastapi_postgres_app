from fastapi import FastAPI, HTTPException, Depends, Query
import sqlalchemy
from sqlmodel import Session
from typing import Annotated
from json import dumps


from models import *
from db import *

app = FastAPI()
init_db()


#FIXME
# Ручка для получения списка имеющихся в БД товаров
@app.get("/items",
         response_model=list[Item],
         description="Запрос на получение списка имеющихся в БД товаров",)
async def read_items(
    session: Annotated[Session, Depends(get_session)],
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    statement = sqlalchemy.select(Item).offset(offset).limit(limit)
    results = session.exec(statement)
    items = [result[0] for result in results] #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!FTW
    return items


# Ручка для получения товара из БД
@app.get("/items/{item_id}",
         response_model=Item,
         description="Запрос на получение товара из БД")
def get_item_by_id(*,
              session: Session = Depends(get_session),
              item_id: int): 
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return item

# Ручка для добавления товара в БД
@app.post("/items",
          response_model=Item,
          description="Запрос на добавление товара в БД")
def create_item(*, 
                session: Session = Depends(get_session),
                item: ItemCreate):
    validated_item = ItemCreate.model_validate(item)
    item_data = validated_item.model_dump(exclude_unset=True)
    add_item = Item()
    for key, val in item_data.items():
        setattr(add_item, key, val)
    session.add(add_item)
    session.commit()
    session.refresh(add_item)
    return add_item


# Ручка для удаления товара из БД
@app.delete("/item/{item_id}",
            description="Запрос на удаление товара из БД")
def delete_item_by_id(*, 
                session: Session = Depends(get_session),
                item_id: int):
    item_instance = session.get(Item, item_id)
    if not item_instance:
        raise HTTPException(status_code=404, detail="Товар не найден")
    session.delete(item_instance)
    session.commit()
    return {"Удалено" : "Да"}


# Ручка для редактирования информации о товаре
@app.patch("/item/{item_id}",
           description="Запрос на редактирования информации о товаре в БД")
def update_item_by_id(*,
                      session: Session = Depends(get_session),
                      item_id: int,
                      item: ItemUpdate):
    item_instance = session.get(Item, item_id)

    if not item_instance:
        raise HTTPException(status_code=404, detail="Товар не найден")
    
    validated_item = ItemCreate.model_validate(item)
    item_data = validated_item.model_dump(exclude_unset=True)
    for key, val in item_data.items():
        setattr(item_instance, key, val)
    session.add(item_instance)
    session.commit()
    session.refresh(item_instance)
    return item_instance