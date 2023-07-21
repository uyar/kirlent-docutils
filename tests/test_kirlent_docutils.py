from importlib import metadata

import kirlent_docutils


def test_installed_version_should_match_tested_version():
    assert metadata.version("kirlent_docutils") == kirlent_docutils.__version__
