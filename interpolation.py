
"""
This code has two methods for filling in missing sensor readings.

Linear interpolation uses straight lines between known readings.
Cuubic sline interpolation uses curves between known readings.

Both methods use the actual time of each reading.
"""

import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline

def prepare_interpolation(values, timestamps):
    """
    Gets the sensor data raedy for interpolation.

    values: The sensor measurements, including missing values.
    timestamps: The time each measurement was taken.

    Returns the time in seconds, sensor readigns and which
    readings are still available.
    """
    # Turn the sensor readigns into numbers Python can work with
    y = np.asarray(values, dtype=float)

    # Turn the mesurement times into a format Python understands
    dt = pd.DatetimeIndex(timestamps)

    # Check that eery reading has a time and that we have data
    if len(y) != len(dt) or not len(y):
        raise ValueError("Sensor values and timestamps must have equal nonzero lengths")

    # Stop if any of the timestamps are missing
    if dt.hasnans:
        raise ValueError("Timestamps must not contain NaT")
    
    # Chsnge the timestamps into seconds from the fiirst measurement
    # This makes it esier to calculaet the time between readings
    x = (dt.asi8 - dt.asi8[0]).astype(np.float64) / 1e9

    # Make sure the timestamps are in order and none are repeated
    if not np.all(np.diff(x) > 0):
        raise ValueError("Timestamps must be unique and strictly increasing")

    # Work out which readings we have and which ones are missing
    return x, y, np.isfinite(y)


def linear_interpolation(values, timestamps):
    """
    Fills in mising sensor readigns using straight lines.

    It uses the known readigns on either side of a gap
    to estimmate what the mising value should be.
    """

    # Get the sensor readings and timestamps ready
    x, y, known = prepare_interpolation(values, timestamps)

    # We need at least two known readings to draw a line
    # The first and last readings also need to be available
    if known.sum() < 2 or not known[0] or not known[-1]:
        raise ValueError("Linear interpolation needs two known values and known endpoints")

    # Make a copy so we dont change the original readings
    out = y.copy()

    # Find which measurements are missing
    missing = ~known

    # Use a straight line between known readings to fill the gaps
    out[missing] = np.interp(x[missing], x[known], y[known])

    # Give back the data with the mising readings filled in
    return out


def cubic_interpolation(values, timestamps):
    """
    Fills in missing sensor readings using curved lines.

    Instead of a straght line, this method creates a smooth
    curve through the known readigns to estimate mising values.

    It needs at least four known readings to work.
    """
    # Get the sensor readings and timestamps ready
    x, y, known = prepare_interpolation(values, timestamps)

    # Make sure we have enough readings to creaet the curve
    # We also need the first and last readings to be aailable
    if known.sum() < 4 or not known[0] or not known[-1]:
        raise ValueError("Cubic spline needs four known values and known endpoints")

    # Copy the original data so it stays unchanged
    out = y.copy()

    # Find the readings that need to be estmated
    missing = ~known

    # Only do the interpolation if there are missing readings
    if missing.any():
        # Create a smooth curve through the known measurements
        model = CubicSpline(x[known], y[known], bc_type="not-a-knot")
        # Use the curve to estimate the missing measurements
        out[missing] = model(x[missing])

        # Return the data with the missing readings filled in
    return out

