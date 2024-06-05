import pytest
from playwright.async_api import async_playwright


class Fixtures:
    @pytest.fixture(scope="session", autouse=True)
    async def one_time_setup_page(self):
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("http://awoha.xyz/")
        yield page
        await browser.close()
        await playwright.stop()


class TestExample(Fixtures):
    @pytest.mark.asyncio
    async def test_example(self, one_time_setup_page):
        print("Hello World!")

