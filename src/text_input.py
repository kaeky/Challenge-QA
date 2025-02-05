import asyncio
async def type_text(page, input_text):
    print(input_text)
    """Escribe un texto en el teclado virtual del simulador"""
    for char in input_text:
        tab = page.locator("div[data-skbtn='{tab}']").first
        await tab.click(force=True)
        await page.wait_for_function(
            """() => document.querySelector("span.mt-4").textContent.trim() === 'Esperando tecla...'"""
        )
        is_upper = char.isupper()
        is_space = char == " "

        if is_upper:
            caps_lock_btn = page.locator('div[data-skbtn="{lock}"]').first
            await caps_lock_btn.click(force=True)
            await asyncio.sleep(0.1)

        if is_space:
            space_button = page.locator("div[data-skbtn='{space}']").first
            await space_button.click()
            await asyncio.sleep(0.1)
            continue

        key_button = page.locator(f'div[data-skbtn="{char}"]').first
        await key_button.click(force=True)
        await asyncio.sleep(0.1)

        if is_upper:
            await caps_lock_btn.click(force=True)
            await asyncio.sleep(0.1)

    await page.wait_for_function(
        """() => document.querySelector("span.mt-4").textContent.trim() === 'Esperando tecla...'"""
    )
    await page.locator("div[data-skbtn='{enter}']").first.click(force=True)
