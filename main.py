import asyncio
from playwright.async_api import async_playwright

async def run_test(file_path, input_text):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://vonsim.github.io")
        await asyncio.sleep(0.1)

        #hacer zoom out
        for _ in range(5):
            await page.click("button[title='Alejar']")
            await asyncio.sleep(0.5)

        # Habilitar teclado y pantalla
        await page.click("button[title='Configuración']")
        await asyncio.sleep(0.1)

        keyboard = page.locator("p:has-text('Teclado y pantalla')")
        switch_button = keyboard.locator("xpath=../following-sibling::button")
        await switch_button.click()
        await asyncio.sleep(0.1)

        # Configurar velocidad de simulación
        speed_simulation = page.locator("p:has-text('Velocidad de simulación')")
        speed_span = speed_simulation.locator("xpath=../following-sibling::span").locator("role=slider")
        bbox = await speed_span.bounding_box()
        await asyncio.sleep(0.1)

        await speed_span.click()
        await asyncio.sleep(0.1)

        await page.mouse.down()
        await asyncio.sleep(0.1)

        # Mover el control deslizante a la derecha
        await page.mouse.move(bbox["x"] + 300, bbox["y"] + bbox["height"] / 2)
        await asyncio.sleep(0.1)

        await page.mouse.up()
        await asyncio.sleep(0.1)

        await page.click("button[title='Configuración']")
        await asyncio.sleep(0.1)

        # Cargar código ensamblador en el panel de código
        textbox = page.locator("div[role='textbox']")
        await textbox.clear()

        with open(file_path, "r") as f:
            asm_code = f.read()
        await textbox.fill(asm_code)
        await asyncio.sleep(0.5)

        # Ejecutar el programa paso a paso
        await page.click("button:has-text('Iniciar')")
        await asyncio.sleep(0.5)
        await page.keyboard.press("F4")
        await asyncio.sleep(0.5)
        keyboard_html = await page.locator("div[data-skbtn]").all_inner_texts()
        print("Teclas encontradas en el teclado virtual:", keyboard_html)
        await page.pause()
        for char in input_text:
            tab = page.locator("div[data-skbtn='{tab}']").first
            await tab.click(force=True)
            await page.wait_for_function(
                """() => document.querySelector("span.mt-4").textContent.trim() === 'Esperando tecla...'"""
            )
            is_upper = char.isupper()
            is_space = char == " "

            if is_upper:
                print(f"Presionando mayúscula")
                # Presionar el botón de "Bloq Mayús" antes de la letra mayúscula
                caps_lock_btn = page.locator('div[data-skbtn="{lock}"]').first
                await caps_lock_btn.scroll_into_view_if_needed()
                await asyncio.sleep(0.1)

                await caps_lock_btn.click(force=True)
                await asyncio.sleep(0.1)

            # Desactivar Bloq Mayús después de una mayúscula

            if is_space:
                # Presionar la tecla de espacio en el teclado virtual
                space_button = page.locator("div[data-skbtn='{space}']").first
                if await space_button.count() > 0:
                    await space_button.click()
                    await asyncio.sleep(0.1)
                    continue

            print(f"Buscando tecla '{char}'")
            key_button = page.locator(f'div[data-skbtn="{char}"]').first
            await key_button.scroll_into_view_if_needed()
            await key_button.click(force=True)
            print(f"Presiono tecla '{char}'")

            if is_upper:
                print(f"Desactivando mayúscula")
                await caps_lock_btn.scroll_into_view_if_needed()
                await caps_lock_btn.click(force=True)
                await asyncio.sleep(0.1)
        await page.wait_for_function(
            """() => document.querySelector("span.mt-4").textContent.trim() === 'Esperando tecla...'"""
        )
        intro = page.locator("div[data-skbtn='{enter}']").first
        await intro.scroll_into_view_if_needed()
        await intro.click(force=True)

        await page.wait_for_timeout(30000000)

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
