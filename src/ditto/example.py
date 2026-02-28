"""Example module demonstrating code style conventions for ditto.

This module provides example classes and functions that showcase:
- NumPy-style docstring formatting
- Inline commenting conventions
- Logging configuration
- Type annotations
- pint unit registry usage
"""

from __future__ import annotations

import logging

import numpy as np
import pint

# Configure module-level logger following Python logging best practices.
# Using __name__ ensures the logger name reflects the module hierarchy.
logger = logging.getLogger(__name__)

# Shared module-level UnitRegistry; one registry per process is recommended
# by pint to avoid unit-compatibility issues between Quantity instances.
_ureg = pint.UnitRegistry()


class ExampleClass:
    """A demonstration class showing code style and documentation conventions.

    This class illustrates how to structure Python classes within the ditto
    template, including proper docstring formatting, type annotations, logging,
    and unit-aware computations using pint.

    Parameters
    ----------
    name : str
        A human-readable identifier for this instance.
    value : float, optional
        The base numeric value, by default 1.0.

    Attributes
    ----------
    name : str
        The instance identifier set during initialization.
    value : float
        The base numeric value used for computations.

    Examples
    --------
    >>> obj = ExampleClass("demo", value=2.5)
    >>> obj.compute(factor=3.0)
    7.5
    """

    def __init__(self, name: str, value: float = 1.0) -> None:
        # Validate that name is a non-empty string for meaningful identification.
        if not name:
            raise ValueError("name must be a non-empty string")

        # Store the instance name for logging and identification purposes.
        self.name = name

        # Store the base value that will be used in computations.
        self.value = value

        # Represent the base value as a dimensionless pint Quantity using the
        # module-level registry so unit arithmetic is consistent across instances.
        self._quantity = _ureg.Quantity(value)

        logger.debug("ExampleClass instance '%s' created with value=%s", name, value)

    def compute(self, factor: float) -> float:
        """Multiply the base value by a scaling factor.

        Performs a unit-aware multiplication using pint, demonstrating how
        unit handling, logging, and return value documentation conventions
        work together in practice.

        Parameters
        ----------
        factor : float
            The multiplier applied to the instance's base value.

        Returns
        -------
        float
            The product of ``self.value`` and ``factor``.

        Raises
        ------
        ValueError
            If ``factor`` is negative, since negative scaling is not supported.

        Examples
        --------
        >>> obj = ExampleClass("test", value=4.0)
        >>> obj.compute(2.5)
        10.0
        """
        # Guard against negative factors which are unsupported in this context.
        if factor < 0:
            raise ValueError(f"factor must be non-negative, got {factor}")

        # Use pint for unit-aware multiplication, then extract the numeric magnitude.
        # This demonstrates how pint can be used to enforce unit consistency in
        # more complex scientific calculations within a real project.
        result = float((self._quantity * factor).magnitude)

        logger.debug(
            "ExampleClass '%s': compute(factor=%s) -> %s",
            self.name,
            factor,
            result,
        )

        return result


def example_function(data: list[float]) -> float:
    """Compute the arithmetic mean of a list of numeric values.

    A simple utility function demonstrating function-level documentation,
    input validation, numpy usage, and debug logging conventions.

    Parameters
    ----------
    data : list of float
        A non-empty sequence of numeric values.

    Returns
    -------
    float
        The arithmetic mean of the provided data.

    Raises
    ------
    ValueError
        If ``data`` is empty.

    Examples
    --------
    >>> example_function([1.0, 2.0, 3.0])
    2.0
    >>> example_function([10.0])
    10.0
    """
    # Validate that data is non-empty before attempting to compute the mean.
    if not data:
        raise ValueError("data must be a non-empty list")

    # Convert to a numpy array for efficient vectorized computation.
    arr = np.asarray(data, dtype=float)

    # Compute the arithmetic mean using numpy's optimized implementation.
    mean_value = float(np.mean(arr))

    logger.debug("example_function: mean of %d values = %s", len(data), mean_value)

    return mean_value
