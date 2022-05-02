"""Tests for fine-grained incremental checking using the cache.

All of the real code for this lives in testfinegrained.py.
"""

# We can't "import FineGrainedSuite from ..." because that will cause pytest
# to collect the non-caching tests when running this file.
import extyper.test.testfinegrained


class FineGrainedCacheSuite(extyper.test.testfinegrained.FineGrainedSuite):
    use_cache = True
    test_name_suffix = '_cached'
    files = (
        extyper.test.testfinegrained.FineGrainedSuite.files + ['fine-grained-cache-incremental.test'])
