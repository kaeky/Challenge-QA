import asyncio
import sys
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

if __name__ == "__main__":
    try:
        asyncio.run(main())
        print("Todas las pruebas han finalizado.")
        sys.exit(0)
    except KeyboardInterrupt:
        print("Ejecución interrumpida por el usuario (Ctrl + C).")
        sys.exit(1)
    except Exception as e:
        print(f"Error fatal durante la ejecución: {e}")
        sys.exit(1)

