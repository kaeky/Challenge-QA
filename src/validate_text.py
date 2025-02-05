import asyncio

async def validate_text(page, expected_text):
    """Valida que el texto esperado esté presente en la página"""
    try:
        await asyncio.wait_for(
            page.wait_for_function(
                """() => document.querySelector("span.mt-4")?.textContent.trim() === 'Detenido'""",
            ),
            timeout=30
        )
    except asyncio.TimeoutError:
        print(f"Timeout: No se encontró el texto 'Detenido' en {expected_text}, validar posible bucle infinito.")
        return

    start_button = page.locator("button:has-text('Iniciar')")
    pre_element = await page.locator("pre").inner_text()
    if pre_element.strip() == expected_text:
        print(f"Prueba exitosa, se encontró {expected_text}")
        return
    if start_button and pre_element.strip() == "":
        print(f"Error En la ejecucion de la prueba, fallo {expected_text}")
        return
