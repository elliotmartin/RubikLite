from __future__ import (
    absolute_import,
    division,
)

import os
import time


# work around check-code complains
#
# This is a simple log level module doing simple test related work, we can't
# import more things, and we do not need it.
environ = getattr(os, 'environ')


def _timeout_factor():
    """return the current modification to timeout"""
    default = int(environ.get('HGTEST_TIMEOUT_DEFAULT', 1))
    current = int(environ.get('HGTEST_TIMEOUT', default))
    return current / float(default)


def wait_file(path, timeout=10):
    timeout *= _timeout_factor()
    start = time.time()
    while not os.path.exists(path):
        if time.time() - start > timeout:
            raise RuntimeError(b"timed out waiting for file: %s" % path)
        time.sleep(0.01)


def write_file(path, content=b''):
    with open(path, 'wb') as f:
        f.write(content)
