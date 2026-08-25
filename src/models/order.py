from datetime import datetime

from sqlalchemy import Integer, Numeric, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from src.database.database import Base


class Order(Base):

    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        nullable=False
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    total_price: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="confirmed"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )