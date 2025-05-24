from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    place: Mapped[str] = mapped_column(String(100))  # Изменили location на place
    phone: Mapped[str] = mapped_column(String(20))
    gender: Mapped[str] = mapped_column(String(10))
    photo: Mapped[str] = mapped_column(String(100))

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"

    def to_dict(self):
        return {
            'id': self.id,
            'gender': self.gender,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'email': self.email,
            'location': self.location,
            'photo': self.photo,
        }
