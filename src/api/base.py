from fastapi import APIRouter, Depends, File, UploadFile
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_session
from models.models import User
from services.files import files_crud
from users.manager import current_user

router = APIRouter()


@router.get('/ping')
async def get_ping(
        db: AsyncSession = Depends(get_session),
        user: User = Depends(current_user),
) -> any:
    logger.info(f'Current user {user.username}')
    return {
        'db_is_active': db.is_active,
        'username': user.username
    }


@router.get('/list')
async def get_files_list(
        db: AsyncSession = Depends(get_session),
        user: User = Depends(current_user),
) -> list[File]:
    files = await files_crud.get(db=db, user=user)
    return files


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
