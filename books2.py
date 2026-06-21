from fastapi import FastAPI, Body
from pydantic import BaseModel, Field

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


BOOKS = [
    Book(1, "Computer Science Pro", "codingwithroby", "a very nice book!", 5),
    Book(2, "BE Fast with FastAPI", "codingwithroby", "a great book!", 5),
    Book(3, "Master Endpoints", "codingwithroby", "a awesome book!", 5),
    Book(4, "HP1 ", "Author1", "Book Description", 2),
    Book(5, "HP2 ", "Author2", "Book Description", 3),
    Book(6, "HP3 ", "Author3", "Book Description", 1),
]


class BookRequest(BaseModel):
    id: int
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=5)


@app.get("/books")
async def read_all_books():
    return BOOKS


@app.post("/create-book")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(new_book)
