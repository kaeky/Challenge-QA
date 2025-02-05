import asyncio
from playwright.async_api import async_playwright

async def get_browser():
    """Inicia el navegador y abre una nueva página"""
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=False)
    page = await browser.new_page()
    await page.goto("https://vonsim.github.io")
    await asyncio.sleep(0.1)
    return browser, page
