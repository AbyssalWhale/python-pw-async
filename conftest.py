import pytest
import os
from helpers.test_run_config import TestRunConfig
from playwright.async_api import async_playwright


class Fixtures:
    __test_run_config = None
    __page = None
    test_results_dir = None

    @pytest.fixture(scope="session", autouse=True)
    async def one_time_setup(self):
        self.__test_run_config = await TestRunConfig.init()
        self.test_results_dir = await self.__create_test_results_folder()

        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context()
        self.__page = await context.new_page()
        await self.__page.goto(await self.__test_run_config.get_url())

        yield self

        await browser.close()
        await playwright.stop()

    async def __create_test_results_folder(self):
        current_dir = os.path.abspath(os.path.dirname(__file__))
        test_results_dir = os.path.join(current_dir, "test_results")
        if not os.path.exists(test_results_dir):
            os.makedirs(test_results_dir, exist_ok=True)
        return test_results_dir


class TestExample(Fixtures):
    @pytest.mark.asyncio
    async def test_example(self, one_time_setup):
        print(f"Hello world {await one_time_setup.test_run_config.get_url()}")
