import asyncio
from playwright.async_api import async_playwright


async def run_test(file_path, input_text):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://vonsim.github.io")

        # Habilitar teclado y pantalla
        await page.click("button[title='Configuración']")
        keyboard = page.locator("p:has-text('Teclado y pantalla')")
        switch_button = keyboard.locator("xpath=../following-sibling::button")
        await switch_button.click()
        await page.click("button[title='Configuración']")
        textbox = page.locator("div[role='textbox']")
        await textbox.fill(open(file_path, "r").read())
        await page.evaluate("el => el.style.border = '2px solid red'", await textbox.element_handle())

        await page.wait_for_timeout(3000)
test_cases = [
    ("files/challenge-qa-01.asm", "Hola Mundo"),
    ("files/challenge-qa-02.asm", "Hola Mundo2"),
    ("files/challenge-qa-03.asm", "Hola Mundo3"),
    ("files/challenge-qa-04.asm", "Hola Mundo4"),
    ("files/challenge-qa-05.asm", "Hola Mundo5")
]

async def main():
    for file_path, text in test_cases:
        await run_test(file_path, text)

asyncio.run(main())


