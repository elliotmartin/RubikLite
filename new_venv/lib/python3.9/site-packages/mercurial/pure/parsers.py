# parsers.py - Python implementation of parsers.c
#
# Copyright 2009 Olivia Mackall <olivia@selenic.com> and others
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.

from __future__ import absolute_import

import struct
import zlib

from ..node import nullid, nullrev
from .. import (
    pycompat,
    util,
)

from ..revlogutils import nodemap as nodemaputil
from ..revlogutils import constants as revlog_constants

stringio = pycompat.bytesio


_pack = struct.pack
_unpack = struct.unpack
_compress = zlib.compress
_decompress = zlib.decompress

# Some code below makes tuples directly because it's more convenient. However,
# code outside this module should always use dirstatetuple.
def dirstatetuple(*x):
    # x is a tuple
    return x


def gettype(q):
    return int(q & 0xFFFF)


def offset_type(offset, type):
    return int(int(offset) << 16 | type)


class BaseIndexObject(object):
    # Format of an index entry according to Python's `struct` language
    index_format = revlog_constants.INDEX_ENTRY_V1
    # Size of a C unsigned long long int, platform independent
    big_int_size = struct.calcsize(b'>Q')
    # Size of a C long int, platform independent
    int_size = struct.calcsize(b'>i')
    # An empty index entry, used as a default value to be overridden, or nullrev
    null_item = (0, 0, 0, -1, -1, -1, -1, nullid)

    @util.propertycache
    def entry_size(self):
        return self.index_format.size

    @property
    def nodemap(self):
        msg = b"index.nodemap is deprecated, use index.[has_node|rev|get_rev]"
        util.nouideprecwarn(msg, b'5.3', stacklevel=2)
        return self._nodemap

    @util.propertycache
    def _nodemap(self):
        nodemap = nodemaputil.NodeMap({nullid: nullrev})
        for r in range(0, len(self)):
            n = self[r][7]
            nodemap[n] = r
        return nodemap

    def has_node(self, node):
        """return True if the node exist in the index"""
        return node in self._nodemap

    def rev(self, node):
        """return a revision for a node

        If the node is unknown, raise a RevlogError"""
        return self._nodemap[node]

    def get_rev(self, node):
        """return a revision for a node

        If the node is unknown, return None"""
        return self._nodemap.get(node)

    def _stripnodes(self, start):
        if '_nodemap' in vars(self):
            for r in range(start, len(self)):
                n = self[r][7]
                del self._nodemap[n]

    def clearcaches(self):
        self.__dict__.pop('_nodemap', None)

    def __len__(self):
        return self._lgt + len(self._extra)

    def append(self, tup):
        if '_nodemap' in vars(self):
            self._nodemap[tup[7]] = len(self)
        data = self.index_format.pack(*tup)
        self._extra.append(data)

    def _check_index(self, i):
        if not isinstance(i, int):
            raise TypeError(b"expecting int indexes")
        if i < 0 or i >= len(self):
            raise IndexError

    def __getitem__(self, i):
        if i == -1:
            return self.null_item
        self._check_index(i)
        if i >= self._lgt:
            data = self._extra[i - self._lgt]
        else:
            index = self._calculate_index(i)
            data = self._data[index : index + self.entry_size]
        r = self.index_format.unpack(data)
        if self._lgt and i == 0:
            r = (offset_type(0, gettype(r[0])),) + r[1:]
        return r


class IndexObject(BaseIndexObject):
    def __init__(self, data):
        assert len(data) % self.entry_size == 0
        self._data = data
        self._lgt = len(data) // self.entry_size
        self._extra = []

    def _calculate_index(self, i):
        return i * self.entry_size

    def __delitem__(self, i):
        if not isinstance(i, slice) or not i.stop == -1 or i.step is not None:
            raise ValueError(b"deleting slices only supports a:-1 with step 1")
        i = i.start
        self._check_index(i)
        self._stripnodes(i)
        if i < self._lgt:
            self._data = self._data[: i * self.entry_size]
            self._lgt = i
            self._extra = []
        else:
            self._extra = self._extra[: i - self._lgt]


class PersistentNodeMapIndexObject(IndexObject):
    """a Debug oriented class to test persistent nodemap

    We need a simple python object to test API and higher level behavior. See
    the Rust implementation for  more serious usage. This should be used only
    through the dedicated `devel.persistent-nodemap` config.
    """

    def nodemap_data_all(self):
        """Return bytes containing a full serialization of a nodemap

        The nodemap should be valid for the full set of revisions in the
        index."""
        return nodemaputil.persistent_data(self)

    def nodemap_data_incremental(self):
        """Return bytes containing a incremental update to persistent nodemap

        This containst the data for an append-only update of the data provided
        in the last call to `update_nodemap_data`.
        """
        if self._nm_root is None:
            return None
        docket = self._nm_docket
        changed, data = nodemaputil.update_persistent_data(
            self, self._nm_root, self._nm_max_idx, self._nm_docket.tip_rev
        )

        self._nm_root = self._nm_max_idx = self._nm_docket = None
        return docket, changed, data

    def update_nodemap_data(self, docket, nm_data):
        """provide full block of persisted binary data for a nodemap

        The data are expected to come from disk. See `nodemap_data_all` for a
        produceur of such data."""
        if nm_data is not None:
            self._nm_root, self._nm_max_idx = nodemaputil.parse_data(nm_data)
            if self._nm_root:
                self._nm_docket = docket
            else:
                self._nm_root = self._nm_max_idx = self._nm_docket = None


class InlinedIndexObject(BaseIndexObject):
    def __init__(self, data, inline=0):
        self._data = data
        self._lgt = self._inline_scan(None)
        self._inline_scan(self._lgt)
        self._extra = []

    def _inline_scan(self, lgt):
        off = 0
        if lgt is not None:
            self._offsets = [0] * lgt
        count = 0
        while off <= len(self._data) - self.entry_size:
            start = off + self.big_int_size
            (s,) = struct.unpack(
                b'>i',
                self._data[start : start + self.int_size],
            )
            if lgt is not None:
                self._offsets[count] = off
            count += 1
            off += self.entry_size + s
        if off != len(self._data):
            raise ValueError(b"corrupted data")
        return count

    def __delitem__(self, i):
        if not isinstance(i, slice) or not i.stop == -1 or i.step is not None:
            raise ValueError(b"deleting slices only supports a:-1 with step 1")
        i = i.start
        self._check_index(i)
        self._stripnodes(i)
        if i < self._lgt:
            self._offsets = self._offsets[:i]
            self._lgt = i
            self._extra = []
        else:
            self._extra = self._extra[: i - self._lgt]

    def _calculate_index(self, i):
        return self._offsets[i]


def parse_index2(data, inline, revlogv2=False):
    if not inline:
        cls = IndexObject2 if revlogv2 else IndexObject
        return cls(data), None
    cls = InlinedIndexObject2 if revlogv2 else InlinedIndexObject
    return cls(data, inline), (0, data)


class Index2Mixin(object):
    index_format = revlog_constants.INDEX_ENTRY_V2
    null_item = (0, 0, 0, -1, -1, -1, -1, nullid, 0, 0)

    def replace_sidedata_info(self, i, sidedata_offset, sidedata_length):
        """
        Replace an existing index entry's sidedata offset and length with new
        ones.
        This cannot be used outside of the context of sidedata rewriting,
        inside the transaction that creates the revision `i`.
        """
        if i < 0:
            raise KeyError
        self._check_index(i)
        sidedata_format = b">Qi"
        packed_size = struct.calcsize(sidedata_format)
        if i >= self._lgt:
            packed = _pack(sidedata_format, sidedata_offset, sidedata_length)
            old = self._extra[i - self._lgt]
            new = old[:64] + packed + old[64 + packed_size :]
            self._extra[i - self._lgt] = new
        else:
            msg = b"cannot rewrite entries outside of this transaction"
            raise KeyError(msg)


class IndexObject2(Index2Mixin, IndexObject):
    pass


class InlinedIndexObject2(Index2Mixin, InlinedIndexObject):
    def _inline_scan(self, lgt):
        sidedata_length_pos = 72
        off = 0
        if lgt is not None:
            self._offsets = [0] * lgt
        count = 0
        while off <= len(self._data) - self.entry_size:
            start = off + self.big_int_size
            (data_size,) = struct.unpack(
                b'>i',
                self._data[start : start + self.int_size],
            )
            start = off + sidedata_length_pos
            (side_data_size,) = struct.unpack(
                b'>i', self._data[start : start + self.int_size]
            )
            if lgt is not None:
                self._offsets[count] = off
            count += 1
            off += self.entry_size + data_size + side_data_size
        if off != len(self._data):
            raise ValueError(b"corrupted data")
        return count


def parse_index_devel_nodemap(data, inline):
    """like parse_index2, but alway return a PersistentNodeMapIndexObject"""
    return PersistentNodeMapIndexObject(data), None


def parse_dirstate(dmap, copymap, st):
    parents = [st[:20], st[20:40]]
    # dereference fields so they will be local in loop
    format = b">cllll"
    e_size = struct.calcsize(format)
    pos1 = 40
    l = len(st)

    # the inner loop
    while pos1 < l:
        pos2 = pos1 + e_size
        e = _unpack(b">cllll", st[pos1:pos2])  # a literal here is faster
        pos1 = pos2 + e[4]
        f = st[pos2:pos1]
        if b'\0' in f:
            f, c = f.split(b'\0')
            copymap[f] = c
        dmap[f] = e[:4]
    return parents


def pack_dirstate(dmap, copymap, pl, now):
    now = int(now)
    cs = stringio()
    write = cs.write
    write(b"".join(pl))
    for f, e in pycompat.iteritems(dmap):
        if e[0] == b'n' and e[3] == now:
            # The file was last modified "simultaneously" with the current
            # write to dirstate (i.e. within the same second for file-
            # systems with a granularity of 1 sec). This commonly happens
            # for at least a couple of files on 'update'.
            # The user could change the file without changing its size
            # within the same second. Invalidate the file's mtime in
            # dirstate, forcing future 'status' calls to compare the
            # contents of the file if the size is the same. This prevents
            # mistakenly treating such files as clean.
            e = dirstatetuple(e[0], e[1], e[2], -1)
            dmap[f] = e

        if f in copymap:
            f = b"%s\0%s" % (f, copymap[f])
        e = _pack(b">cllll", e[0], e[1], e[2], e[3], len(f))
        write(e)
        write(f)
    return cs.getvalue()
