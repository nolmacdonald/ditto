"""Unit tests for ditto.example module."""

from __future__ import annotations

import pytest

from ditto.example import ExampleClass, example_function


class TestExampleClass:
    """Tests for ExampleClass."""

    def test_init_default_value(self):
        """ExampleClass initialises with default value of 1.0."""
        obj = ExampleClass("test")
        assert obj.name == "test"
        assert obj.value == 1.0

    def test_init_custom_value(self):
        """ExampleClass stores the provided value."""
        obj = ExampleClass("demo", value=3.5)
        assert obj.value == 3.5

    def test_init_empty_name_raises(self):
        """Empty name raises ValueError."""
        with pytest.raises(ValueError, match="non-empty"):
            ExampleClass("")

    def test_compute_basic(self):
        """compute returns value * factor."""
        obj = ExampleClass("test", value=4.0)
        assert obj.compute(2.5) == 10.0

    def test_compute_zero_factor(self):
        """compute with factor=0 returns 0."""
        obj = ExampleClass("test", value=5.0)
        assert obj.compute(0) == 0.0

    def test_compute_negative_factor_raises(self):
        """Negative factor raises ValueError."""
        obj = ExampleClass("test", value=1.0)
        with pytest.raises(ValueError, match="non-negative"):
            obj.compute(-1.0)


class TestExampleFunction:
    """Tests for example_function."""

    def test_mean_of_list(self):
        """Returns correct mean of a numeric list."""
        assert example_function([1.0, 2.0, 3.0]) == pytest.approx(2.0)

    def test_single_element(self):
        """Single-element list returns that element."""
        assert example_function([42.0]) == pytest.approx(42.0)

    def test_empty_list_raises(self):
        """Empty list raises ValueError."""
        with pytest.raises(ValueError, match="non-empty"):
            example_function([])
