from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.docs.load_docs import BOOKS_DOCS
from app.database import get_db
from app.models import Book
from app.schemas.books import BookCreate, BookResponse, BookUpdate, BookListResponse

router = APIRouter(prefix='/books', tags=["books"])


@router.get("/", tags=["books"], response_model=BookListResponse, **BOOKS_DOCS['get_books'])
async def get_books(
        db: AsyncSession = Depends(get_db),
        page: int = Query(1, ge=1, alias="page", description="Page number"),
        per_page: int = Query(10, ge=1, le=20, alias="per_page", description="Page size"),
        search: str = Query(None, description="Search by title"),
        author: str = Query(None, description="Search by author"),
        category: str = Query(None, description="Search by category"),

):
    query = select(Book)
    if search:
        search_filter = f"%{search}%"
        query = query.where(Book.title.ilike(f"%{search_filter}%"))

    if author:
        query = query.where(Book.author == author)

    if category:
        query = query.where(Book.category == category)

    count_query = select(func.count()).select_from(query.subquery())

    total_results = await db.execute(count_query)
    total = total_results.scalar()

    offset = (page - 1) * per_page
    query = query.offset(offset).limit(per_page)

    result = await db.execute(query)
    books = result.scalars().all()

    book_items = [BookResponse.model_validate(book, from_attributes=True) for book in books]
    return BookListResponse(
        books=book_items,
        total=total,
        page=page,
        per_page=per_page,
        pages=(total + per_page - 1) // per_page,
        has_next=offset + per_page < total,
        has_prev=page > 1
    )


@router.get("/{book_id}", tags=["books"], response_model=BookResponse, **BOOKS_DOCS['get_book'])
async def get_book(book_id: str, db: AsyncSession = Depends(get_db)):
    try:
        book_uuid = UUID(book_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid book id")

    result = await db.execute(select(Book).where(Book.id == book_uuid))
    book = result.scalars().first()

    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


@router.post("/", tags=["books"], status_code=201, response_model=BookResponse, **BOOKS_DOCS['create_book'])
async def create_book(book: BookCreate, db: AsyncSession = Depends(get_db)):
    existing_book = await db.execute(select(Book).where(Book.isbn == book.isbn))
    if existing_book.scalars().first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book already exist")

    new_book = Book(
        title=book.title,
        author=book.author,
        isbn=book.isbn,
        category=book.category,

    )
    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)

    return new_book


@router.patch("/{book_id}", tags=["books"], response_model=BookResponse, **BOOKS_DOCS['update_book'])
async def update_book(book_id: str, book_update: BookUpdate, db: AsyncSession = Depends(get_db)):
    try:
        book_uuid = UUID(book_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid book id")

    result = await db.execute(select(Book).where(Book.id == book_uuid))
    book = result.scalars().first()

    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    update_data = book_update.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No data to update")

    if "isbn" in update_data and update_data["isbn"]:
        new_isbn = update_data["isbn"]

        isbn_check = await db.execute(
            select(Book).where(
                and_(
                    Book.isbn == new_isbn,
                    Book.id != book_uuid
                )
            )
        )
        existing_book_with_isbn = isbn_check.scalars().first()

        if existing_book_with_isbn:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Book with ISBN '{new_isbn}' already exist"
            )

    for key, value in update_data.items():
        setattr(book, key, value)

    await db.commit()
    await db.refresh(book)

    return book


@router.delete("/{book_id}", tags=["books"], status_code=204, **BOOKS_DOCS['delete_book'])
async def delete_book(book_id: str, db: AsyncSession = Depends(get_db)):
    try:
        book_uuid = UUID(book_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid book id")

    result = await db.execute(select(Book).where(Book.id == book_uuid))
    book = result.scalars().first()

    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    await db.delete(book)
    await db.commit()
    return None
