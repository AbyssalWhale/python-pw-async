import pytest
from playwright.async_api import async_playwright
import json
import os

from helpers.test_run_config import TestRunConfig


class Fixtures:

    __test_config_name = "test-run-config.json"
    test_config = None

    @pytest.fixture(scope="session", autouse=True)
    async def one_time_setup_page(self):
        # config_path = await self.get_test_run_config_path()
        # await self.read_config(path=config_path)
        config = await TestRunConfig.init()


        #
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(config.test_config.get("url"))
        yield page
        await browser.close()
        await playwright.stop()

    async def read_config(self, path: str):
        if os.path.exists(path):
            with open(path) as f:
                self.test_config = json.load(f)
        else:
            raise Exception(f"Could not find file. Path: {path}")

    async def get_test_run_config_path(self):
        current_dir = os.path.abspath(os.path.dirname(__file__))
        while not os.path.isfile(os.path.join(current_dir, self.__test_config_name)):
            parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
            if parent_dir == current_dir:
                raise Exception(f"Unable to find {self.__test_config_name} in root")
            current_dir = parent_dir
        return os.path.join(current_dir, self.__test_config_name)



class TestExample(Fixtures):
    @pytest.mark.asyncio
    async def test_example(self, one_time_setup_page):
        print("Hello World!")

