import asyncio
from src.execute_test import run_test
from tests.test_cases import test_cases

# Definir un semáforo para limitar a 5 navegadores simultáneos
semaphore = asyncio.Semaphore(5)


async def run_limited_test(file_path, text):
    async with semaphore:
        await run_test(file_path, text)


async def main():
    tasks = []
    for file_path, texts in test_cases:
        for text in texts:
            tasks.append(run_limited_test(file_path, text))

    await asyncio.gather(*tasks)


asyncio.run(main())
