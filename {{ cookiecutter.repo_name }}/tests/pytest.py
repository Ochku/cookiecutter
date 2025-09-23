import pytest


def test_code_is_tested():
    """This is an example function for testing."""
    assert 0.1 + 0.2 == pytest.approx(0.3) # nosec B101