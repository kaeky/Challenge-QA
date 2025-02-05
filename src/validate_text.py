import asyncio

async def validate_text(page, expected_text):
    """Valida que el texto esperado esté presente en la página"""
    await page.wait_for_function(
        f"""() => document.querySelector("pre").textContent.trim() === '{expected_text}'"""
    )