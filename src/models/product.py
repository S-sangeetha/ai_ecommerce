from datetime import datetime

from sqlalchemy import String, Text, Numeric, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from pgvector.sqlalchemy import Vector
from src.database.database import Base


class Product(Base):

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    brand: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    category: Mapped[str] = mapped_column(
            String(100),
            nullable=False
        )
    price: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    stock: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )
    embedding: Mapped[list[float] | None] = mapped_column(
    Vector(768),
    nullable=True
)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )