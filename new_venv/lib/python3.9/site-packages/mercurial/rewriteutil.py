# rewriteutil.py - utility functions for rewriting changesets
#
# Copyright 2017 Octobus <contact@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.

from __future__ import absolute_import

import re

from .i18n import _
from .node import (
    hex,
    nullrev,
)

from . import (
    error,
    obsolete,
    obsutil,
    revset,
    scmutil,
)


NODE_RE = re.compile(br'\b[0-9a-f]{6,64}\b')


def precheck(repo, revs, action=b'rewrite'):
    """check if revs can be rewritten
    action is used to control the error message.

    Make sure this function is called after taking the lock.
    """
    if nullrev in revs:
        msg = _(b"cannot %s null changeset") % action
        hint = _(b"no changeset checked out")
        raise error.InputError(msg, hint=hint)

    if len(repo[None].parents()) > 1:
        raise error.StateError(_(b"cannot %s while merging") % action)

    publicrevs = repo.revs(b'%ld and public()', revs)
    if publicrevs:
        msg = _(b"cannot %s public changesets") % action
        hint = _(b"see 'hg help phases' for details")
        raise error.InputError(msg, hint=hint)

    newunstable = disallowednewunstable(repo, revs)
    if newunstable:
        raise error.InputError(_(b"cannot %s changeset with children") % action)


def disallowednewunstable(repo, revs):
    """Checks whether editing the revs will create new unstable changesets and
    are we allowed to create them.

    To allow new unstable changesets, set the config:
        `experimental.evolution.allowunstable=True`
    """
    allowunstable = obsolete.isenabled(repo, obsolete.allowunstableopt)
    if allowunstable:
        return revset.baseset()
    return repo.revs(b"(%ld::) - %ld", revs, revs)


def skip_empty_successor(ui, command):
    empty_successor = ui.config(b'rewrite', b'empty-successor')
    if empty_successor == b'skip':
        return True
    elif empty_successor == b'keep':
        return False
    else:
        raise error.ConfigError(
            _(
                b"%s doesn't know how to handle config "
                b"rewrite.empty-successor=%s (only 'skip' and 'keep' are "
                b"supported)"
            )
            % (command, empty_successor)
        )


def update_hash_refs(repo, commitmsg, pending=None):
    """Replace all obsolete commit hashes in the message with the current hash.

    If the obsolete commit was split or is divergent, the hash is not replaced
    as there's no way to know which successor to choose.

    For commands that update a series of commits in the current transaction, the
    new obsolete markers can be considered by setting ``pending`` to a mapping
    of ``pending[oldnode] = [successor_node1, successor_node2,..]``.
    """
    if not pending:
        pending = {}
    cache = {}
    hashes = re.findall(NODE_RE, commitmsg)
    unfi = repo.unfiltered()
    for h in hashes:
        fullnode = scmutil.resolvehexnodeidprefix(unfi, h)
        if fullnode is None:
            continue
        ctx = unfi[fullnode]
        if not ctx.obsolete():
            successors = pending.get(fullnode)
            if successors is None:
                continue
            # obsutil.successorssets() returns a list of list of nodes
            successors = [successors]
        else:
            successors = obsutil.successorssets(repo, ctx.node(), cache=cache)

        # We can't make any assumptions about how to update the hash if the
        # cset in question was split or diverged.
        if len(successors) == 1 and len(successors[0]) == 1:
            successor = successors[0][0]
            if successor is not None:
                newhash = hex(successor)
                commitmsg = commitmsg.replace(h, newhash[: len(h)])
            else:
                repo.ui.note(
                    _(
                        b'The stale commit message reference to %s could '
                        b'not be updated\n(The referenced commit was dropped)\n'
                    )
                    % h
                )
        else:
            repo.ui.note(
                _(
                    b'The stale commit message reference to %s could '
                    b'not be updated\n'
                )
                % h
            )

    return commitmsg
