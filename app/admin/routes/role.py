from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import and_

from app.admin.schemas.role import SGRole, SCRole, SURole, SRole
from app.repository.tools import get_list_data
from app.users.dependencies import get_current_user, has_perm
from app.users.models import User, Role, Permission, RolePermission
from app.users.schemas import SPermission

router = APIRouter(prefix='/role', tags=['Роли'])


@router.get('/permissions')
@has_perm('all, permissions')
async def get_permission_list(user: User = Depends(get_current_user)) -> List[SPermission]:
    return await Permission.get_all()


# TODO required permissions [user, role.read]
@router.get('/')
@has_perm('all, role, role.read')
async def get_roles(page: int = 1, limit: int = 15, user: User = Depends(get_current_user)) -> SGRole:
    return await get_list_data(Role, page, limit)


@router.get('/{role_id}')
@has_perm('all, role, role.read')
async def get_role(role_id: int, user: User = Depends(get_current_user)) -> SRole:
    return await Role.find_by_id_or_fail(model_id=role_id)


# TODO required permissions [user, role.create]
@router.post('/')
@has_perm('all, role, role.create')
async def create_role(data: SCRole, page: int = 1, limit: int = 15, user: User = Depends(get_current_user)) -> SGRole:
    permissions = await Permission.get_all(filter=Permission.id.in_(data.permission_ids))
    new_role = await Role.create(names=dict(data.names))
    await RolePermission.insert(
        [RolePermission(role_id=new_role.id, permission_id=permission_id) for permission_id in data.permission_ids])
    return await get_list_data(Role, page, limit)


# TODO required permissions [user, role.update]
@router.put('/{role_id}')
@has_perm('all, role, role.update')
async def update_role(role_id: int, data: SURole, page: int = 1, limit: int = 15,
                      user: User = Depends(get_current_user)) -> SGRole:
    role = await Role.find_by_id_or_fail(model_id=role_id)
    await Role.update(model_id=role_id, names=dict(data.names))
    await RolePermission.delete(filter=and_(
        RolePermission.role_id == role.id, RolePermission.permission_id.in_(data.remove_permission_ids)
    ))
    await RolePermission.insert(
        [RolePermission(role_id=role.id, permission_id=permission_id) for permission_id in data.new_permission_ids])

    return await get_list_data(Role, page, limit)


# TODO required permissions [user, role.delete]
@router.delete('/{role_id}')
@has_perm('all, role, role.delete')
async def delete_role(role_id: int, page: int = 1, limit: int = 15, user: User = Depends(get_current_user)) -> SGRole:
    await Role.delete(filter=and_(Role.id == role_id, Role.system_role == False))
    return await get_list_data(Role, page, limit)
