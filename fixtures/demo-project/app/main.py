"""Pantry API: a deliberately small FastAPI + SQLite app."""
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

from . import db


def _clean_name(value):
    value = value.strip()
    if not value:
        raise ValueError("name must not be empty")
    return value


class ItemCreate(BaseModel):
    name: str
    quantity: int = Field(ge=0)
    unit: str = "pcs"

    _check_name = field_validator("name")(_clean_name)


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    quantity: Optional[int] = None
    unit: Optional[str] = None

    @field_validator("name")
    @classmethod
    def _check_name(cls, value):
        return None if value is None else _clean_name(value)


def create_app(db_path):
    app = FastAPI(title="Pantry API")
    db.init_db(db_path)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.post("/items", status_code=201)
    def create_item(body: ItemCreate):
        return db.create_item(db_path, body.name, body.quantity, body.unit)

    @app.get("/items")
    def list_items():
        return db.list_items(db_path)

    @app.get("/items/{item_id}")
    def get_item(item_id: int):
        item = db.get_item(db_path, item_id)
        if item is None:
            raise HTTPException(status_code=404, detail="item not found")
        return item

    @app.patch("/items/{item_id}")
    def patch_item(item_id: int, body: ItemUpdate):
        fields = body.model_dump(exclude_unset=True)
        if fields.get("quantity") is not None and fields["quantity"] < 0:
            raise HTTPException(status_code=422, detail="quantity must be >= 0")
        if any(v is None for v in fields.values()):
            raise HTTPException(status_code=422, detail="fields may not be null")
        item = db.update_item(db_path, item_id, fields)
        if item is None:
            raise HTTPException(status_code=404, detail="item not found")
        return item

    @app.delete("/items/{item_id}", status_code=204)
    def delete_item(item_id: int):
        if not db.delete_item(db_path, item_id):
            raise HTTPException(status_code=404, detail="item not found")

    return app
