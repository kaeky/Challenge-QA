import asyncio
from src.execute_test import run_test
from tests.test_cases import test_cases

async def main():
    for file_path, text in test_cases:
        await run_test(file_path, text)

asyncio.run(main())
