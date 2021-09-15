from pkg_resources import get_distribution

import kirlent.docutils


def test_installed_version_should_match_tested_version():
    assert get_distribution("kirlent_docutils").version == kirlent.docutils.__version__
