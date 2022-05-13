from sqlalchemy import Boolean, Column, ForeignKey, Integer, MetaData, String, Table
# from sqlalchemy.orm import relationship
from sqlalchemy.ext.automap import automap_base

# from .database import Base
from .database import engine

"""
SQLAlchemy が提供する Columnと各種型によって各カラムを定義するとそれがテーブル作成時の型になる。

"""

"""
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")
"""

metadata = MetaData()
metadata.reflect(
    engine,
    only=["users", "phones",],
)
Table('phones', metadata, Column("ower_id", ForeignKey("users.id")),extend_existing=True,)
Base = automap_base(metadata=metadata)
Base.prepare()
User, Phone = (Base.classes.users, Base.classes.phones)
