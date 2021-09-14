# revlogdeltas.py - constant used for revlog logic
#
# Copyright 2005-2007 Olivia Mackall <olivia@selenic.com>
# Copyright 2018 Octobus <contact@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
"""Helper class to compute deltas stored inside revlogs"""

from __future__ import absolute_import

import struct

from ..interfaces import repository

### main revlog header

INDEX_HEADER = struct.Struct(b">I")

## revlog version
REVLOGV0 = 0
REVLOGV1 = 1
# Dummy value until file format is finalized.
REVLOGV2 = 0xDEAD

##  global revlog header flags
# Shared across v1 and v2.
FLAG_INLINE_DATA = 1 << 16
# Only used by v1, implied by v2.
FLAG_GENERALDELTA = 1 << 17
REVLOG_DEFAULT_FLAGS = FLAG_INLINE_DATA
REVLOG_DEFAULT_FORMAT = REVLOGV1
REVLOG_DEFAULT_VERSION = REVLOG_DEFAULT_FORMAT | REVLOG_DEFAULT_FLAGS
REVLOGV1_FLAGS = FLAG_INLINE_DATA | FLAG_GENERALDELTA
REVLOGV2_FLAGS = FLAG_INLINE_DATA

### individual entry

## index v0:
#  4 bytes: offset
#  4 bytes: compressed length
#  4 bytes: base rev
#  4 bytes: link rev
# 20 bytes: parent 1 nodeid
# 20 bytes: parent 2 nodeid
# 20 bytes: nodeid
INDEX_ENTRY_V0 = struct.Struct(b">4l20s20s20s")

## index v1
#  6 bytes: offset
#  2 bytes: flags
#  4 bytes: compressed length
#  4 bytes: uncompressed length
#  4 bytes: base rev
#  4 bytes: link rev
#  4 bytes: parent 1 rev
#  4 bytes: parent 2 rev
# 32 bytes: nodeid
INDEX_ENTRY_V1 = struct.Struct(b">Qiiiiii20s12x")
assert INDEX_ENTRY_V1.size == 32 * 2

#  6 bytes: offset
#  2 bytes: flags
#  4 bytes: compressed length
#  4 bytes: uncompressed length
#  4 bytes: base rev
#  4 bytes: link rev
#  4 bytes: parent 1 rev
#  4 bytes: parent 2 rev
# 32 bytes: nodeid
#  8 bytes: sidedata offset
#  4 bytes: sidedata compressed length
#  20 bytes: Padding to align to 96 bytes (see RevlogV2Plan wiki page)
INDEX_ENTRY_V2 = struct.Struct(b">Qiiiiii20s12xQi20x")
assert INDEX_ENTRY_V2.size == 32 * 3

# revlog index flags

# For historical reasons, revlog's internal flags were exposed via the
# wire protocol and are even exposed in parts of the storage APIs.

# revision has censor metadata, must be verified
REVIDX_ISCENSORED = repository.REVISION_FLAG_CENSORED
# revision hash does not match data (narrowhg)
REVIDX_ELLIPSIS = repository.REVISION_FLAG_ELLIPSIS
# revision data is stored externally
REVIDX_EXTSTORED = repository.REVISION_FLAG_EXTSTORED
# revision data contains extra metadata not part of the official digest
REVIDX_SIDEDATA = repository.REVISION_FLAG_SIDEDATA
# revision changes files in a way that could affect copy tracing.
REVIDX_HASCOPIESINFO = repository.REVISION_FLAG_HASCOPIESINFO
REVIDX_DEFAULT_FLAGS = 0
# stable order in which flags need to be processed and their processors applied
REVIDX_FLAGS_ORDER = [
    REVIDX_ISCENSORED,
    REVIDX_ELLIPSIS,
    REVIDX_EXTSTORED,
    REVIDX_SIDEDATA,
    REVIDX_HASCOPIESINFO,
]

# bitmark for flags that could cause rawdata content change
REVIDX_RAWTEXT_CHANGING_FLAGS = (
    REVIDX_ISCENSORED | REVIDX_EXTSTORED | REVIDX_SIDEDATA
)

SPARSE_REVLOG_MAX_CHAIN_LENGTH = 1000
