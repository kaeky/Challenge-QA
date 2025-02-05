import asyncio

ACCENTED_VOWELS = {"á", "é", "í", "ó", "ú", "Á", "É", "Í", "Ó", "Ú"}
DIAERESIS_VOWELS = {"ü", "Ü"}

async def type_text(page, input_text):
    print("Inicia la escritura de texto", input_text)
    """Escribe un texto en el teclado virtual del simulador"""
    for char in input_text:
        tab = page.locator("div[data-skbtn='{tab}']").first
        await tab.click(force=True)
        await page.wait_for_function(
            """() => document.querySelector("span.mt-4").textContent.trim() === 'Esperando tecla...'"""
        )
        is_upper = char.isupper()
        is_space = char == " "
        is_accented = char in ACCENTED_VOWELS
        is_diaeresis = char in DIAERESIS_VOWELS

        # Manejo del espacio
        if is_space:
            space_button = page.locator("div[data-skbtn='{space}']").first
            await space_button.click()
            await asyncio.sleep(0.1)
            continue

        # Manejo de caracteres con tilde
        if is_accented:
            accent_button = page.locator('div[data-skbtnuid="es-r1b11"]').first  # Botón de tilde
            await accent_button.click(force=True)
            await asyncio.sleep(0.1)

        # Manejo de diéresis
        if is_diaeresis:
            caps_lock_btn = page.locator('div[data-skbtn="{lock}"]').first
            await caps_lock_btn.click(force=True)
            await asyncio.sleep(0.1)
            diaeresis_button = page.locator('div[data-skbtnuid="es-shift-r1b11"]').first
            await diaeresis_button.click(force=True)
            await asyncio.sleep(0.1)
            char = char.upper()

        key_button = page.locator(f'div[data-skbtn="{char}"]').first
        key_exists = await key_button.count() > 0

        if not key_exists:
            caps_lock_btn = page.locator('div[data-skbtn="{lock}"]').first
            await caps_lock_btn.click(force=True)
            await asyncio.sleep(0.1)

            key_button = page.locator(f'div[data-skbtn="{char}"]').first
            key_exists = await key_button.count() > 0

            if not key_exists:
                print(f"Caracter no encontrado: {char}")
                continue

        await key_button.click(force=True)
        await asyncio.sleep(0.1)

        if is_upper or is_diaeresis:
            caps_lock_btn = page.locator('div[data-skbtn="{lock}"]').first
            await caps_lock_btn.click(force=True)
            await asyncio.sleep(0.1)

    await page.wait_for_function(
        """() => document.querySelector("span.mt-4").textContent.trim() === 'Esperando tecla...'""",
    )
    await page.locator("div[data-skbtn='{enter}']").first.click(force=True)

