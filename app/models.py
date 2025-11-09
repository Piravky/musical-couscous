import uuid

from sqlalchemy import Column, String, UUID

from app.database import Base


class Book(Base):
    __tablename__ = "books"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, comment='Book ID')
    title = Column(String(500), nullable=False, comment='Book title')
    author = Column(String(500), nullable=False, comment='Book author')
    isbn = Column(String(20), nullable=False, unique=True, comment='Book ISBN')
    category = Column(String(100), nullable=False, comment='Book category')
