.. _getting_started:

Getting Started
===============

Installation
------------

Install ditto using ``pip``::

   pip install ditto

Or using ``uv``::

   uv add ditto

For development, clone the repository and sync the environment::

   git clone https://github.com/nolmacdonald/ditto.git
   cd ditto
   uv sync

``uv sync`` provisions the interpreter pinned in ``.python-version``, creates
``.venv``, and installs ditto together with the ``dev`` dependency group.

For building documentation, add the ``docs`` group::

   uv sync --group docs

Requirements
------------

ditto requires Python 3.12 or newer and is tested against 3.12, 3.13 and 3.14.

Quick Start
-----------

.. code-block:: python

   from ditto.example import ExampleClass, example_function
   from ditto.logging_config import configure_logging
   import logging

   # Configure logging for your application
   configure_logging(level=logging.INFO)

   # Create an instance
   obj = ExampleClass("my_object", value=2.5)

   # Compute a result
   result = obj.compute(factor=4.0)
   print(result)  # 10.0

   # Compute mean of a list
   mean = example_function([1.0, 2.0, 3.0, 4.0])
   print(mean)  # 2.5
