"""
Renderer service for capturing browser screenshots.
Manages headless browser automation to render the frontend as PNG.
"""
import asyncio
from playwright.async_api import async_playwright
from pathlib import Path
from config import Config


class Renderer:
    """Handles headless browser rendering to PNG."""
    
    def __init__(self, config: Config):
        self.config = config
        self.url = f"http://localhost:{config.server_port}/"
        self.width = config.render_width
        self.height = config.render_height
    
    async def render_to_png(self, output_path: str = "output.png", max_retries: int = 5) -> Path:
        """
        Open headless browser, wait for page load, and capture screenshot.
        
        Args:
            output_path: Path where the PNG should be saved
            max_retries: Number of times to retry if page fails to load
            
        Returns:
            Path object pointing to the saved PNG file
        """
        for attempt in range(max_retries):
            try:
                async with async_playwright() as p:
                    browser = await p.chromium.launch(headless=True)
                    
                    page = await browser.new_page(
                        viewport={"width": self.width, "height": self.height}
                    )
                    
                    print(f"Attempting to load {self.url} (attempt {attempt + 1}/{max_retries})...")
                    await page.goto(self.url, wait_until="domcontentloaded", timeout=30000)
                    
                    print("Page loaded, waiting for content to render...")
                    await asyncio.sleep(3)
                    
                    output_file = Path(output_path)
                    await page.screenshot(path=str(output_file), full_page=False)
                    print(f"Screenshot saved successfully")
                    
                    await browser.close()
                    
                    return output_file
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 5
                    print(f"Retrying in {wait_time} seconds...")
                    await asyncio.sleep(wait_time)
                else:
                    raise Exception(f"Failed to render after {max_retries} attempts: {e}")  