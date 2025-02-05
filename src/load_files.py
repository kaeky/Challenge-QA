import asyncio
async def load_file(page, file_path):
    """Carga el código ensamblador en el panel de código"""
    textbox = page.locator("div[role='textbox']")
    await textbox.clear()

    with open(file_path, "r") as f:
        asm_code = f.read()

    await textbox.fill(asm_code)
    await asyncio.sleep(0.5)
