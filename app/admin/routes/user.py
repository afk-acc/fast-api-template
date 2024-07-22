from fastapi import APIRouter, Depends

from app.admin.schemas.user import SGUser, SUUser
from app.repository.tools import get_list_data
from app.users.dependencies import has_perm, get_current_user
from app.users.models import User
from app.users.schemas import SCurrentUser

router = APIRouter(
    prefix="/users",
    tags=["Пользователи"],
)


# TODO required permissions [user, user.read]
@router.get('/')
@has_perm('all, user, user.read')
async def get_user_list(page: int = 1, limit: int = 15, user: User = Depends(get_current_user)) -> SGUser:
    return await get_list_data(User, page, limit)


@router.get('/{user_id}')
@has_perm('all, user, user.read')
async def get_user_detail(user_id: int, user: User = Depends(get_current_user)) -> SCurrentUser:
    return await User.find_by_id_or_fail(model_id=user_id)


# TODO requured permissions [user.update]
@router.post('/{user_id}')
@has_perm('all, user, user.update')
async def update_user(user_id: int, data: SUUser, user: User = Depends(get_current_user)) -> SCurrentUser:
    await User.update(model_id=user_id, role_id=data.role_id)
    return await User.find_by_id_or_fail(model_id=user_id)


@router.post('/block/{user_id}')
@has_perm('all, user, user.block')
async def block_user(user_id: int, page: int = 1, limit: int = 15, user: User = Depends(get_current_user)) -> SGUser:
    await User.update(model_id=user_id, is_active=False)
    return await get_list_data(User, page, limit)


@router.post('/unblock/{user_id}')
@has_perm('all, user, user.block')
async def unblock_user(user_id: int, page: int = 1, limit: int = 15, user: User = Depends(get_current_user)) -> SGUser:
    await User.update(model_id=user_id, is_active=True)
    return await get_list_data(User, page, limit)


@router.post('/restart/server')
@has_perm('all')
async def restart_server(user=Depends(get_current_user)):
    import subprocess
    try:
        # result = subprocess.run(['mkdir', 'tmepa'], check=True,
        #                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = subprocess.run(['supervisorctl', 'restart', 'api-tripzone'], check=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout.decode())
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e.stderr.decode()}")
    return {'status': 200}
