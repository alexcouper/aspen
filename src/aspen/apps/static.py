from os.path import isdir, isfile

from aspen import configuration, conf
from aspen.handlers.static import static as static_handler
from aspen.utils import find_default, translate


def static(environ, start_response):
    """This makes the static handler available as a full-blown application.
    """
    root = conf.statics.get('doc_root', environ['PATH_TRANSLATED'])
    
    environ['PATH_TRANSLATED'] = translate( root,
                                           environ['PATH_INFO']
                                           )
    fspath = find_default(configuration.defaults, environ)
    if isdir(fspath):
        start_response('403 Forbidden', [])
        return ['This directory has no index.']
    if not isfile(fspath) or fspath.endswith('README.aspen'):
        start_response('404 Not Found', [])
        return ['Resource not found.']
    return static_handler(environ, start_response)
