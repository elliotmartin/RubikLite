# sidedata.py - Logic around store extra data alongside revlog revisions
#
# Copyright 2019 Pierre-Yves David <pierre-yves.david@octobus.net)
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
"""core code for "sidedata" support

The "sidedata" are stored alongside the revision without actually being part of
its content and not affecting its hash. It's main use cases is to cache
important information related to a changesets.

The current implementation is experimental and subject to changes. Do not rely
on it in production.

Sidedata are stored in the revlog itself, thanks to a new version of the
revlog. The following format is currently used::

    initial header:
        <number of sidedata; 2 bytes>
    sidedata (repeated N times):
        <sidedata-key; 2 bytes>
        <sidedata-entry-length: 4 bytes>
        <sidedata-content-sha1-digest: 20 bytes>
        <sidedata-content; X bytes>
    normal raw text:
        <all bytes remaining in the rawtext>

This is a simple and effective format. It should be enough to experiment with
the concept.
"""

from __future__ import absolute_import

import struct

from .. import error
from ..utils import hashutil

## sidedata type constant
# reserve a block for testing purposes.
SD_TEST1 = 1
SD_TEST2 = 2
SD_TEST3 = 3
SD_TEST4 = 4
SD_TEST5 = 5
SD_TEST6 = 6
SD_TEST7 = 7

# key to store copies related information
SD_P1COPIES = 8
SD_P2COPIES = 9
SD_FILESADDED = 10
SD_FILESREMOVED = 11
SD_FILES = 12

# internal format constant
SIDEDATA_HEADER = struct.Struct('>H')
SIDEDATA_ENTRY = struct.Struct('>HL20s')


def serialize_sidedata(sidedata):
    sidedata = list(sidedata.items())
    sidedata.sort()
    buf = [SIDEDATA_HEADER.pack(len(sidedata))]
    for key, value in sidedata:
        digest = hashutil.sha1(value).digest()
        buf.append(SIDEDATA_ENTRY.pack(key, len(value), digest))
    for key, value in sidedata:
        buf.append(value)
    buf = b''.join(buf)
    return buf


def deserialize_sidedata(blob):
    sidedata = {}
    offset = 0
    (nbentry,) = SIDEDATA_HEADER.unpack(blob[: SIDEDATA_HEADER.size])
    offset += SIDEDATA_HEADER.size
    dataoffset = SIDEDATA_HEADER.size + (SIDEDATA_ENTRY.size * nbentry)
    for i in range(nbentry):
        nextoffset = offset + SIDEDATA_ENTRY.size
        key, size, storeddigest = SIDEDATA_ENTRY.unpack(blob[offset:nextoffset])
        offset = nextoffset
        # read the data associated with that entry
        nextdataoffset = dataoffset + size
        entrytext = bytes(blob[dataoffset:nextdataoffset])
        readdigest = hashutil.sha1(entrytext).digest()
        if storeddigest != readdigest:
            raise error.SidedataHashError(key, storeddigest, readdigest)
        sidedata[key] = entrytext
        dataoffset = nextdataoffset
    return sidedata
