from fastapi import APIRouter
from fastapi import FastAPI,Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient

MONGO_URI="mongodb+srv://ishija:6nd2r9gi6BuNivhs@cluster0.5okgi.mongodb.net/Testing"
conn = MongoClient(MONGO_URI)

note=APIRouter()

from pydantic import BaseModel
class NameModel(BaseModel):
    name:str
    author:str 
    genre:str
    copies:int


templates = Jinja2Templates(directory="templates")
@note.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    docs = conn.Testing.Testing.find()  
    newdocs = []
    for doc in docs:
        newdocs.append({
            "id": doc["_id"],
            "name": doc["name"],
            "author": doc["author"],  
            "copies": doc["copies"]   
        })
    return templates.TemplateResponse("index.html", {"request": request, "newdocs": newdocs})


@note.post('/')
async def add_item(request: Request):
    form = await request.form()  
    name = form.get('name')
    author = form.get('author')
    genre = form.get('genre')
    copies = form.get('copies')

    # Insert book details in MongoDB
    new_book = {
        "name": name,
        "author": author,
        "genre": genre,
        "copies": int(copies)  
    }
    conn.Testing.Testing.insert_one(new_book)
    return {"message": "Book added successfully"}

@note.delete('/')
def delete_item(name:str):
   item=conn.Testing.Testing.find_one_and_delete({"name":name})
   return "deleted successfully"

