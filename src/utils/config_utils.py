from src.handlers.configuration import ConfigurationHandler


def get_configuration(config_file: str, is_local: bool) -> ConfigurationHandler:
    if config_file:
        config = ConfigurationHandler(config_file, is_local)
        config.setup()

        return config

    raise ValueError("CONFIG_FILE environment variable is not defined.")
