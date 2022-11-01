import os
from abc import ABC, abstractmethod
from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import Generic, Type, TypeVar, Union
from zipfile import ZipFile

from fastapi import File, UploadFile
from fastapi.responses import FileResponse, StreamingResponse
from loguru import logger
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.engine import ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession

from models.models import Base, User

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)


class Repository(ABC):

    @abstractmethod
    def get(self, *args, **kwargs):
        pass

    @abstractmethod
    def create(self, *args, **kwargs):
        raise NotImplementedError


class RepositoryDB(Repository, Generic[ModelType, CreateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self._model = model

    async def get(
            self,
            db: AsyncSession,
            user: User
    ):
        statement = (
            select(self._model)
            .where(
                self._model.author == user.id
            )
        )
        result: ScalarResult = await db.scalars(statement=statement)
        logger.info(result)
        return result.all()

    async def get_path_by_id(self, db, user, id):
        statement = select(self._model).where(self._model.id == id)
        file = await db.scalar(statement=statement)
        full_path = f'{user.username}/{file.path}/{file.name}'
        logger.info(file.name)
        return full_path

    async def get_file_by_id(self, db, user: User, id: int) -> File:
        path = await self.get_path_by_id(db=db, id=id, user=user)
        return FileResponse(path=path)

    @staticmethod
    async def get_file_by_path(user: User, path: Path) -> File:
        logger.info(path)
        full_path = f'{user.username}/{path}'
        response = FileResponse(path=full_path)
        return response

    async def download_file(
            self,
            db: AsyncSession,
            user: User,
            identifier: Union[str, int],
    ):
        try:
            int(identifier)
            logger.info(f'{identifier} is int')
            file = await self.get_file_by_id(
                db=db,
                user=user,
                id=int(identifier),
            )
        except ValueError:
            logger.info(identifier)
            file = await self.get_file_by_path(
                user=user,
                path=Path(identifier),
            )
        except FileNotFoundError:
            return {'Exception': 'No such file'}
        return file

    @staticmethod
    def zip_folder(file_list):
        io = BytesIO()
        zip_name = f'{str(datetime.now())}.zip'
        with ZipFile(zip_name, 'w') as zip:
            for file in file_list:
                zip.write(file)
        return StreamingResponse(
            iter([io.getvalue()]),
            media_type='application/x-zip-compressed',
            headers={'Content-Disposition': f'attachment;filename={zip_name}'}
        )

    async def download_folder(
            self,
            user: User,
            path: str,
    ):
        full_path = f'{user.username}/{path}'
        file_list = [f'{full_path}/{file}' for file in os.listdir(full_path)]
        archive = self.zip_folder(file_list)
        return archive

    async def create_in_db(
            self,
            size: int,
            db: AsyncSession,
            user: User,
            path: str,
            file: UploadFile = File(),
    ):
        logger.info(file)
        logger.info(await file.read())
        db_obj = self._model(
            name=file.filename,
            path=path,
            size=size,
            is_downloadable=True,
            author=user.id
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    @staticmethod
    async def write_file(
            user: User,
            path: str,
            file: UploadFile = File(),
    ):
        content = file.file.read()
        user_path = f'{user.username}/{path}'
        if not path:
            p = Path(f'{user.username}')
        else:
            p = Path(user_path)
        try:
            if not Path.exists(p):
                os.makedirs(p)
                logger.info(f'mkdir {user_path}')
            with open(os.path.join(f'{p}/{file.filename}'), 'wb') as f:
                logger.info(f)
                f.write(content)
        except Exception as ex:
            return ex

    async def create(
            self,
            db: AsyncSession,
            user: User,
            path: str,
            file: UploadFile = File(),
    ):
        file_size = len(file.file.read())
        result = await self.write_file(
            user=user,
            path=path,
            file=file,
        )
        logger.info(str(result))
        if not isinstance(result, Exception):
            await self.create_in_db(
                db=db,
                user=user,
                path=path,
                file=file,
                size=file_size,
            )
            return {
                'Ready': f'Successfully uploaded {file.filename}',
                'Size': f'{"{:.1f}".format(file_size/1000000)}mb',
                    }
        else:
            return {'Error': str(result)}

    async def search_files(
            self,
            db: AsyncSession,
            user: User,
            path: str,
            extension: str,
            limit: int
    ):
        if path and extension:
            statement = (
                select(self._model)
                .where(self._model.author == user.id)
                .where(self._model.path == path)
                .where(self._model.name.endswith(f'.{extension}'))
                .limit(limit)
            )
            file_list = await db.scalars(statement=statement)
            return file_list.all()
