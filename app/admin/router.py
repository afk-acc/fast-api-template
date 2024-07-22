from fastapi import APIRouter, Depends

from app.users.dependencies import has_perm, get_current_user
from app.users.models import User
from .routes.role import router as role_router
from .routes.user import router as user_router
router = APIRouter(
    prefix='/admin',
    tags=['Администрирование']
)
router.include_router(role_router)
router.include_router(user_router)

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
