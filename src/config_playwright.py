import asyncio
async def configure_simulation(page):
    """Configura el simulador antes de cargar el código"""
    # Hacer zoom out
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
    await page.mouse.move(bbox["x"] + 300, bbox["y"] + bbox["height"] / 2)
    await asyncio.sleep(0.1)
    await page.mouse.up()
    await asyncio.sleep(0.1)

    await page.click("button[title='Configuración']")
    await asyncio.sleep(0.1)
