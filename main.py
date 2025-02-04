import asyncio
from playwright.async_api import async_playwright

async def run_test(file_path, input_text):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://vonsim.github.io")
        await asyncio.sleep(0.01)  # delay 10ms

        # Habilitar teclado y pantalla
        await page.click("button[title='Configuración']")
        await asyncio.sleep(0.01)

        keyboard = page.locator("p:has-text('Teclado y pantalla')")
        switch_button = keyboard.locator("xpath=../following-sibling::button")
        await switch_button.click()
        await asyncio.sleep(0.01)

        await page.evaluate("""
            const cursor = document.createElement('div');
            cursor.id = 'custom-cursor';
            cursor.style.position = 'absolute';
            cursor.style.width = '20px';
            cursor.style.height = '20px';
            cursor.style.borderRadius = '50%';
            cursor.style.backgroundColor = 'red';
            cursor.style.zIndex = '9999';
            cursor.style.pointerEvents = 'none';
            document.body.appendChild(cursor);
        """)
        await asyncio.sleep(0.01)

        await page.evaluate("""
            document.addEventListener('mousemove', (event) => {
                const cursor = document.getElementById('custom-cursor');
                cursor.style.left = event.clientX + 'px';
                cursor.style.top = event.clientY + 'px';
            });
        """)
        await asyncio.sleep(0.01)

        # Configurar velocidad de simulación
        speed_simulation = page.locator("p:has-text('Velocidad de simulación')")
        speed_span = speed_simulation.locator("xpath=../following-sibling::span").locator("role=slider")
        bbox = await speed_span.bounding_box()
        await asyncio.sleep(0.01)

        await speed_span.click()
        await asyncio.sleep(0.01)

        await page.mouse.down()
        await asyncio.sleep(0.01)

        # En este ejemplo, se mueve a x+300 (puedes ajustar según la posición que necesites)
        # Recuerda que si bbox["y"] no es 0, lo ideal es usar bbox["y"] + bbox["height"]/2
        await page.mouse.move(bbox["x"] + 300, bbox["y"] + bbox["height"] / 2)
        await asyncio.sleep(0.01)

        await page.mouse.up()
        await asyncio.sleep(0.01)

        await page.click("button[title='Configuración']")
        await asyncio.sleep(0.01)

        # Cargar código ensamblador en el panel de código
        textbox = page.locator("div[role='textbox']")
        with open(file_path, "r") as f:
            asm_code = f.read()
        await textbox.fill(asm_code)
        await asyncio.sleep(0.01)

        # Ejecutar el programa paso a paso
        await page.click("button:has-text('Iniciar')")
        await asyncio.sleep(0.01)
        await page.keyboard.press("F4")
        await asyncio.sleep(0.01)

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
