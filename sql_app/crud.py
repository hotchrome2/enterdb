import os
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile

from sqlalchemy.orm import Session
from fastapi import File, Form, UploadFile
from azure.storage.blob import BlobServiceClient, ContentSettings, BlobClient, ContainerClient

from . import models, schemas

"""
main.py のroutes処理（各API処理）の中がFATにならないよう、DBクエリ関係はここに書く。
"""


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(title=item.title, description=item.description, owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def create_user_item_with_upload(db: Session, user_id: int, uploadfile: UploadFile):
    tmp_path: Path = ""
    filename = uploadfile.filename
    filesize = 0
    try:
        connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        container_name = "april27"
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=uploadfile.filename)

        suffix = Path(uploadfile.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(uploadfile.file, tmp)
            tmp_path = Path(tmp.name)
            filesize = os.stat(tmp_path).st_size
            content_settings = ContentSettings(content_type=uploadfile.content_type)

            with open(tmp_path, "rb") as data:
                blob_client.upload_blob(data, content_settings=content_settings)

    finally:
        uploadfile.file.close()

    db_item = models.Item(title=filename, description=str(filesize), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
