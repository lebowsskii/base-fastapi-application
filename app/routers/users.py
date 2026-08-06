import uuid

from fastapi import APIRouter

from app.crud import users as users_crud
from app.dependencies import DBSessionDep
from app.schemas.user import User
from app.utils.exceptions import NotFoundError
from app.utils.response import BaseResponse

router = APIRouter(prefix="/v1/users", tags=["users"])


@router.get("/")
async def list_users(session: DBSessionDep) -> BaseResponse[list[User]]:
    users = await users_crud.get_all(session)
    return BaseResponse(success=True, msg="ok", data=users)


@router.get("/{user_id}")
async def get_user(user_id: uuid.UUID, session: DBSessionDep) -> BaseResponse[User]:
    user = await users_crud.get_by_id(session, user_id)
    if not user:
        raise NotFoundError("User not found")
    return BaseResponse(success=True, msg="ok", data=user)
