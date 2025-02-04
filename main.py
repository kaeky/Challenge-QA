import asyncio
from playwright.async_api import async_playwright


async def run_test():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://vonsim.github.io")

        # Habilitar teclado y pantalla
        await page.click("button[title='Configuración']")
        keyboard = page.locator("p:has-text('Teclado y pantalla')")
        switch_button = keyboard.locator("xpath=../following-sibling::button")
        await switch_button.click()

        await page.wait_for_timeout(10000)


asyncio.run(run_test())

