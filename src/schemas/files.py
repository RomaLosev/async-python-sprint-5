from datetime import datetime

from pydantic import BaseModel


class FileBase(BaseModel):
    name: str


class FileCreate(FileBase):
    pass


class FileInDBBase(FileBase):
    id: int
    name: str
    created_at: datetime
    path: str
    size: int
    is_downloadable: bool

    class Config:
        orm_mode = True


class File(FileInDBBase):
    pass


class FileInDB(FileInDBBase):
    pass
