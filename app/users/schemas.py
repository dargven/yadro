from pydantic import BaseModel, Field, EmailStr


class SUserCreate(BaseModel):
    phone: str = Field(..., description="Номер телефона в международном формате, начинающийся с '+'")
    email: EmailStr = Field(..., description="Электронная почта")
    first_name: str = Field(..., min_length=3, max_length=50, description="Имя, от 3 до 50 символов")
    last_name: str = Field(..., min_length=3, max_length=50, description="Фамилия, от 3 до 50 символов")
    gender: str = Field(..., min_length=3, max_length=50, description="Пол, от 3 до 50 символов")
    location: str = Field(..., min_length=3, max_length=50, description="Местоположение, от 3 до 50 символов")
    photo: str = Field(..., min_length=3, max_length=50, description="фото, от 3 до 50 символов")


class SUserResponse(SUserCreate):
    pass