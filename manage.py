import os
import sys


def create_module(module_name):
    # Путь к папке модуля
    module_path = os.path.join('app', module_name)

    # Создаем директорию, если она не существует
    os.makedirs(module_path, exist_ok=True)

    # Создаем и заполняем файл models.py
    models_content = "from app.repository.base import Base\n"
    with open(os.path.join(module_path, 'models.py'), 'w') as models_file:
        models_file.write(models_content)

    # Создаем и заполняем файл router.py
    router_content = f"""from fastapi import APIRouter
router = APIRouter(prefix="/{module_name}", tags=["{module_name}"])
"""
    with open(os.path.join(module_path, 'router.py'), 'w') as router_file:
        router_file.write(router_content)

    # Создаем и заполняем файл schemas.py
    schemas_content = "from pydantic import BaseModel\n"
    with open(os.path.join(module_path, 'schemas.py'), 'w') as schemas_file:
        schemas_file.write(schemas_content)

    # Создаем и заполняем файл seed.py
    seed_content = f"""class Seeder:
    @staticmethod
    async def run():
        print('{module_name} seed')
        
"""
    with open(os.path.join(module_path, 'seed.py'), 'w') as seed_file:
        seed_file.write(seed_content)

        update_main_py(module_name)
        update_env_py(module_name)
        print(f"Module {module_name} created successfully with models.py, router.py, schemas.py, and seed.py.")


def update_env_py(module_name):
    env_py_path = os.path.join('app', 'migrations', 'env.py')
    with open(env_py_path, 'r+') as env_py:
        content = env_py.read()
        env_py.seek(0, 0)
        env_py.write(f"from app.{module_name}.models import *\n" + content)


def update_main_py(module_name):
    main_py_path = os.path.join('app', 'main.py')
    with open(main_py_path, 'a') as main_py:
        main_py.write(f"from app.{module_name}.router import router as router_{module_name}\n")
        main_py.write(f"app.include_router(router_{module_name})\n")


def handle_commands(args):
    if args[0] == "startapp":
        if len(args) != 2:
            print("Usage: python script.py startapp <module_name>")
            sys.exit(1)
        create_module(args[1])
    else:
        print(f"Command {args[0]} not recognized.")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <command> <args>")
        sys.exit(1)

    handle_commands(sys.argv[1:])
