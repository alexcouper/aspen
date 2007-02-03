"""Define a handler that serves static files.
"""
import datetime
import mimetypes
import rfc822
import os
import stat
import time
from os.path import isdir, isfile

from aspen import mode, conf
from aspen.exceptions import ConfigError


# import-time configuration
# =========================

# CHUNK_SIZE
# ----------

val = conf.static.get('chunk_size', 8192)
if not str(val).isdigit() or (val < 1):
    raise ConfigError( "chunk_size must be an integer greater than 0"
                     , "__/etc/aspen.conf"
                     , "<?>" # lineno
                      )
CHUNK_SIZE = int(val)


# AUTOINDEX
# ---------

val = conf.static.get('autoindex', None)
if val is None:
    val = True # default
else:
    if val.lower() == 'yes':
        val = True
    elif val.lower() == 'no':
        val = False
    else:
        raise ConfigError( "autoindex must be 'yes' or 'no'"
                         , "__/etc/aspen.conf"
                         , "<?>" # lineno
                          )
AUTOINDEX = val


# WSGI return iterable
# ====================

class Resource(object):
    """Wrap a file object into an interable.

    The value here is in:

      - closing the file when we're done done with it
      - logging

    """

    def __init__(self, filename):
        self._fp = open(filename, 'rb')
        if mode.debdev:
            print "static resource called"
            self._start = datetime.datetime.now()

    def __iter__(self):
        return self

    def next(self):
        chunk_ = self._fp.read(CHUNK_SIZE)
        if not chunk_:
            raise StopIteration
        return chunk_

    def close(self):
        try:
            #os.close(self._fp)
            if mode.debdev:
                elapsed = datetime.datetime.now() - self._start
                print "static content delivered in %s sec" % str(elapsed)
            self._fp.close()
        except Exception, why:
            if mode.debdev:
                print "error closing fp: %s" % str(why)


# WSGI callable
# =============

def static(environ, start_response):
    """Serve a static file off of the filesystem.

    In staging and deployment modes, we honor any 'If-Modified-Since'
    header, an HTTP header used for caching.

    XXX: look at Luke Arno's ACK GPL and some others ... Etags? Iteration?

    """

    path = environ['PATH_TRANSLATED']
    if isdir(path):
        raise NotImplementedError
    else:
        assert isfile(environ['PATH_TRANSLATED']) # sanity check


    # Get basic info from the filesystem and start building a response.
    # =================================================================

    stats = os.stat(path)
    mtime = stats[stat.ST_MTIME]
    size = stats[stat.ST_SIZE]
    content_type = mimetypes.guess_type(path)[0] or 'text/plain'


    # Support 304s, but only in staging and production modes.
    # =======================================================

    status = '200 OK'
    if mode.stprod:
        ims = environ.get('HTTP_IF_MODIFIED_SINCE', '')
        if ims:
            mod_since = rfc822.parsedate(ims)
            last_modified = time.gmtime(mtime)
            if last_modified[:6] <= mod_since[:6]:
                status = '304 Not Modified'


    # Set up the response.
    # ====================

    headers = []
    headers.append(('Last-Modified', rfc822.formatdate(mtime)))
    headers.append(('Content-Type', content_type))
    headers.append(('Content-Length', str(size)))

    start_response(status, headers)
    if status == '304 Not Modified':
        return []
    else:
        return Resource(path)
