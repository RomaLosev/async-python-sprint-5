import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi_pagination import add_pagination

from api import base
from core.config import app_settings
from users.manager import fastapi_users, jwt_backend
from users.shemas import UserCreate, UserRead, UserUpdate

app = FastAPI(
    title=app_settings.app_title,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)
app.include_router(
    base.router,
    prefix='/file',
    tags=['Files']
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['Auth'],
)
app.include_router(
    fastapi_users.get_auth_router(jwt_backend),
    prefix='/auth/jwt',
    tags=['Auth'],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix='/users',
    tags=['users'],
)
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080, log_level='info')

add_pagination(app)
