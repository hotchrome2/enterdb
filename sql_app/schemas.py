from typing import Optional

from pydantic import BaseModel


class PhoneBase(BaseModel):
    title: str
    description: Optional[str] = None

# class ItemBase(BaseModel):
#     title: str
#     description: Optional[str] = None


# class ItemCreate(ItemBase):
#     pass

class PhoneCreate(PhoneBase):
    pass


class Phone(PhoneBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

# class Item(ItemBase):
#     id: int
#     owner_id: int

#     class Config:
#         orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


# class User(UserBase):
#     id: int
#     is_active: bool
#     items: list[Item] = []

#     class Config:
#         orm_mode = True

class User(UserBase):
    id: int
    is_active: bool
    Phones: list[Phone] = []

    class Config:
        orm_mode = True
