from typing import List

from pydantic import BaseModel, UUID4, ConfigDict


class BookBase(BaseModel):
    title: str
    author: str
    isbn: str
    category: str


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    isbn: str | None = None
    category: str | None = None


class BookResponse(BookBase):
    id: UUID4


class BookListResponse(BaseModel):
    books: List[BookResponse]
    total: int
    page: int
    per_page: int
    pages: int
    has_next: bool
    has_prev: bool

    model_config = ConfigDict(from_attributes=True)
