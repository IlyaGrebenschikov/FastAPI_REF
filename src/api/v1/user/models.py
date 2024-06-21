from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped

from src.database.base import Base


class UserModel(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    referred_by: Mapped[str] = mapped_column(nullable=True)
