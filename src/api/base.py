import time

from fastapi import APIRouter, Depends, File, UploadFile
from fastapi_pagination import Page, paginate
from fastapi_pagination.ext.sqlalchemy import AbstractPage
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_session
from models.models import User
from schemas.files import FileInDB
from services.files import files_crud
from users.manager import current_user

router = APIRouter()


# Не нашёл как достать время отклика базы данных, будем замерять запрос))
# Буду признателен за подсказку, как можно было сделать правильно)
@router.get('/ping')
async def get_ping(
        db: AsyncSession = Depends(get_session),
        user: User = Depends(current_user),
) -> any:
    start_time = time.time()
    await files_crud.get(db=db, user=user)
    ping = time.time() - start_time
    return {
        'ping': "{:.4f}".format(ping),
        'user': {'username': user.username, 'email': user.email},
    }


@router.get('/list', response_model=Page[FileInDB])
async def get_files_list(
        db: AsyncSession = Depends(get_session),
        user: User = Depends(current_user),
) -> AbstractPage:
    files = await files_crud.get(db=db, user=user)
    return paginate(files)


@router.post('/upload')
async def upload_file(
        db: AsyncSession = Depends(get_session),
        user: User = Depends(current_user),
        file: UploadFile = File(),
        path: str = None,
) -> File:
    file_upload = await files_crud.create(db=db, file=file, user=user, path=path)
    return file_upload


@router.get('/download/')
async def download_file(
        *,
        db: AsyncSession = Depends(get_session),
        user: User = Depends(current_user),
        identifier: str | int = None,
        download_folder: bool = False,
) -> File:
    if download_folder:
        file = await files_crud.download_folder(user=user, path=identifier)
    else:
        file = await files_crud.download_file(db=db, user=user, identifier=identifier)
    return file


@router.get('/search')
async def search_files(
        *,
        db: AsyncSession = Depends(get_session),
        user: User = Depends(current_user),
        path: str = None,
        extension: str = None,
        file_name: str = None,
        limit: int = 100,
) -> list[File]:
    result = await files_crud.search_files(
        db=db,
        user=user,
        path=path,
        extension=extension,
        file_name=file_name,
        limit=limit,
    )
    return result
