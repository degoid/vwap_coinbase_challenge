import os

import pytest

from src.utils.config_utils import get_configuration


def test_var_env_not_defined():
    with pytest.raises(ValueError):
        get_configuration(None, None)

    with pytest.raises(ValueError):
        get_configuration(None, False)


