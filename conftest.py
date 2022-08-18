"""
Injects m_layer in to the doctest namespace for pytest and uses
`sybil <https://pypi.org/project/sybil/>`_ to test ".. code-block:: python"
examples in the documentation.
"""
import sys
import pytest
from doctest import NORMALIZE_WHITESPACE, ELLIPSIS

from sybil import Sybil
from sybil.parsers.codeblock import CodeBlockParser
from sybil.parsers.doctest import DocTestParser

from m_layer import *

@pytest.fixture(autouse=True)
def add_m_layer(doctest_namespace):
    for key, val in globals().items():
        if key.startswith('_'):
            continue
        doctest_namespace[key] = val
        
    # if sys.version_info.major > 2:
        # doctest_namespace['xrange'] = range

pytest_collect_file = Sybil(
    parsers=[
        DocTestParser(optionflags=NORMALIZE_WHITESPACE | ELLIPSIS)
    ],
    pattern='*.rst',
    fixtures=['add_m_layer']
).pytest()