"""Basic tests for the template."""

import czech_ozone_historical_analysis


def test_version():
    """Test that version is defined."""
    assert hasattr(czech_ozone_historical_analysis, "__version__")
    assert czech_ozone_historical_analysis.__version__ == "0.1.0"


def test_import():
    """Test that package can be imported."""
    assert czech_ozone_historical_analysis is not None
