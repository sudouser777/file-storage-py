import logging
import os
from typing import Any, Mapping

import yaml

from constants import CONFIG_FILE_PATH
from exceptions import ConfigFileNotFoundError, ConfigMissingError

logger = logging.getLogger(__name__)


def read_config_yaml(name: str) -> Mapping[str, Any]:
    config_file_path = os.getenv(CONFIG_FILE_PATH, 'config.yml')

    logger.debug(f'Using the configuration file path: {config_file_path}')
    if not config_file_path:
        raise ConfigFileNotFoundError('Configuration file not found')

    with open(config_file_path) as fp:
        config: dict[str, Any] = yaml.safe_load(fp)

    if config_data := config.get(name):
        return config_data

    raise ConfigMissingError(f'Configuration not found for the provider: {name}')
