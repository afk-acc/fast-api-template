import os
import asyncio
import importlib.util


async def load_and_run_seeder_async(module_path):
    spec = importlib.util.spec_from_file_location("module.name", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    await module.Seeder.run()


async def main():
    tasks = []
    for root, dirs, files in os.walk('.'):  # Идем по всем директориям в текущей директории
        if 'seed.py' in files:
            path = os.path.join(root, 'seed.py')
            print(f"Running Seeder from {path}")
            task = asyncio.create_task(load_and_run_seeder_async(path))
            tasks.append(task)
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
