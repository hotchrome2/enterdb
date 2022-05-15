import os
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import Depends, FastAPI, HTTPException, File, Form, UploadFile
from sqlalchemy.orm import Session

from azure.storage.blob import BlobServiceClient, ContentSettings, BlobClient, ContainerClient, __version__


from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


@app.post("/upload/")
async def create_file(uploadfile: UploadFile):
    tmp_path: Path = ""
    try:
        connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        container_name = "april27"
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=uploadfile.filename)

        suffix = Path(uploadfile.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(uploadfile.file, tmp)
            tmp_path = Path(tmp.name)
            size = os.stat(tmp_path).st_size
            content_settings = ContentSettings(content_type=uploadfile.content_type)

            with open(tmp_path, "rb") as data:
                blob_client.upload_blob(data, content_settings=content_settings)

    finally:
        uploadfile.file.close()

    return {"upload_filename": uploadfile.filename, "uploadfile_content_type": uploadfile.content_type, "size": size}
