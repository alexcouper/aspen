try:
    from setuptools import setup
except:
    from distutils.core import setup


classifiers = [
    'Development Status :: 3 - Alpha'
  , 'Environment :: Console'
  , 'Intended Audience :: Developers'
  , 'License :: OSI Approved :: MIT License'
  , 'Natural Language :: English'
  , 'Operating System :: MacOS :: MacOS X'
  , 'Operating System :: Microsoft :: Windows'
  , 'Operating System :: POSIX'
  , 'Programming Language :: Python'
  , 'Topic :: Internet :: WWW/HTTP :: HTTP Servers'
  , 'Topic :: Internet :: WWW/HTTP :: WSGI'
  , 'Topic :: Internet :: WWW/HTTP :: WSGI :: Application'
  , 'Topic :: Internet :: WWW/HTTP :: WSGI :: Server'
   ]

setup( name = 'aspen'
     , version = '~~VERSION~~'
     , packages = [ 'aspen'
                   ]
     , scripts = ['bin/aspen']
     , description = 'Aspen is a Python webserver.'
     , author = 'Chad Whitacre'
     , author_email = 'chad@knotbird.com'
     , url = 'http://www.zetadev.com/software/aspen/'
     , classifiers = classifiers
      )
