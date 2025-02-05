import asyncio
from src.browser_setup import get_browser
from src.config_playwright import configure_simulation
from src.text_input import type_text
from src.load_files import load_file
from src.validate_text import validate_text

async def run_test(file_path, input_text):
    """Ejecuta la prueba para un archivo ensamblador y entrada de texto"""
    browser, page = await get_browser()

    await configure_simulation(page)
    await load_file(page, file_path)
    await page.click("button:has-text('Iniciar')")
    await asyncio.sleep(0.5)

    await page.keyboard.press("F4")
    await asyncio.sleep(0.5)

    await type_text(page, input_text)

    await validate_text(page, input_text)
    await browser.close()
