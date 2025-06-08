import yaml


class Config:
    def __init__(self, path: str = "config.yaml"):
        with open(path, "r") as f:
            self._cfg = yaml.safe_load(f)

    def get(self, *keys, default=None):
        value = self._cfg
        for key in keys:
            value = value.get(key)
            if value is None:
                return default
        return value


config = Config()
