from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# --- schemas ---
class Book(BaseModel):
    name: str
    price: float
    in_stock: bool = True

class BookUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    in_stock: Optional[bool] = None

class BookOut(BaseModel):
    id: int
    name: str
    price: float
    in_stock: bool

# --- fake db ---
db = {}
counter = 0

# --- CREATE ---
@app.post("/books", response_model=BookOut, status_code=201)
def create_item(item: Book):
    global counter
    counter += 1
    db[counter] = {"id": counter, **item.dict()}
    return db[counter]

# --- READ ---
@app.get("/books", response_model=list[BookOut])
def list_items(skip: int = 0, limit: int = 10):
    return list(db.values())[skip: skip + limit]

@app.get("/books/{item_id}", response_model=BookOut)
def get_item(item_id: int):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Book not found")
    return db[item_id]

# --- UPDATE ---
@app.put("/books/{item_id}", response_model=BookOut)
def update_item(item_id: int, item: Book):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Book not found")
    db[item_id] = {"id": item_id, **item.dict()}
    return db[item_id]

@app.patch("/books/{item_id}", response_model=BookOut)
def partial_update_item(item_id: int, item: BookUpdate):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    stored = db[item_id]
    updates = item.dict(exclude_unset=True)
    stored.update(updates)
    db[item_id] = stored
    return db[item_id]

# --- DELETE ---
@app.delete("/books/{item_id}", status_code=204)
def delete_item(item_id: int):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Book not found")
    del db[item_id]