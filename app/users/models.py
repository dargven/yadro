from sqlalchemy.orm import Mapped

from app.database import Base, int_pk


class User(Base):
    id: Mapped[int_pk]
    gender: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[str]
    phone: Mapped[str]
    email: Mapped[str]
    location: Mapped[str]
    photo: Mapped[str]

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
