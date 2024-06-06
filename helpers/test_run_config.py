import json
import os


class TestRunConfig:

    __test_config_name = "test-run-config.json"
    test_config = None

    def __init__(self, config_path: str):
        self.config_path = config_path

    @classmethod
    async def init(cls):
        config_path = cls.__get_test_run_config_path()
        instance = cls(config_path=config_path)
        await instance.__read_config()
        return instance

    async def __read_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path) as f:
                self.test_config = json.load(f)
        else:
            raise Exception(f"Could not find file. Path: {self.config_path}")

    @staticmethod
    def __get_test_run_config_path():
        current_dir = os.path.abspath(os.path.dirname(__file__))
        while not os.path.isfile(os.path.join(current_dir, TestRunConfig.__test_config_name)):
            parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
            if parent_dir == current_dir:
                raise Exception(f"Unable to find {TestRunConfig.__test_config_name} in root")
            current_dir = parent_dir
        return os.path.join(current_dir, TestRunConfig.__test_config_name)
