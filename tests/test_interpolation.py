"""Independent tests for the project's interpolation functions."""
import pathlib
import sys
import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from interpolation import linear_interpolation, cubic_interpolation, prepare_interpolation

# Turns numbers into timestamps for testing
def times(seconds):
    return pd.to_datetime(seconds, unit="s", origin="2025-01-01")
# Checks that linear interpolation gives the correct answer using a straight line
def test_linear_matches_known_straight_line_with_irregular_time():
    y = np.array([10., np.nan, 40., 70.])
    result = linear_interpolation(y, times([0, 5, 15, 30]))
    np.testing.assert_allclose(result, [10., 20., 40., 70.])
# Checks the spline against a cubic equation where we know the answer
def test_cubic_matches_known_cubic_polynomial():
    t = np.array([0, 1, 2, 3, 4, 5], dtype=float)
    y = t**3 - 2*t**2 + t + 7
    masked = y.copy()
    masked[2] = np.nan
    result = cubic_interpolation(masked, times(t))
    np.testing.assert_allclose(result, y, atol=1e-9)
# Makes sure the original measurements dont get changed
def test_known_values_preserved():
    y = np.array([1., 2., np.nan, 4., 5.])
    ts = times([0, 1, 2, 3, 4])
    for method in (linear_interpolation, cubic_interpolation):
        result = method(y, ts)
        np.testing.assert_array_equal(result[~np.isnan(y)], y[~np.isnan(y)])
        assert np.isfinite(result).all()
# Checks that the code rejects two measurements with the same time
def test_rejects_duplicate_timestamps():
    with pytest.raises(ValueError, match="unique"):
        linear_interpolation([1., np.nan, 3.], times([0, 0, 2]))
# Checks that the first and last measurements are available
def test_rejects_missing_endpoints():
    with pytest.raises(ValueError, match="endpoints"):
        linear_interpolation([np.nan, 2., 3.], times([0, 1, 2]))
# Makes sure there are enough measurements to calculate a cubic spline
def test_cubic_requires_four_known_values():
    with pytest.raises(ValueError, match="four"):
        cubic_interpolation([1., np.nan, 3., 4.], times([0, 1, 2, 3]))
# Checks the number of timestamps matches the number of measurements
def test_rejects_mismatched_lengths():
    with pytest.raises(ValueError, match="equal"):
        prepare_interpolation([1., 2.], times([0]))
# Checks that missing timestamps are rejected
def test_rejects_missing_timestamp():
    with pytest.raises(ValueError, match="NaT"):
        prepare_interpolation([1., 2.], pd.to_datetime(["2025-01-01", None]))
