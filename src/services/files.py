from models.models import FileModel
from schemas.files import FileCreate

from .base import RepositoryDB


class RepositoryFile(RepositoryDB[FileModel, FileCreate]):
    pass


files_crud = RepositoryFile(FileModel)
