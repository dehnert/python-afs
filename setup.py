#!/usr/bin/env python

import sys
if sys.hexversion < 0x020600f0:
    sys.exit("Python 2.6 or higher is required.")

from setuptools import Extension, setup
from Cython.Distutils import build_ext
import os

for root in ['/Library/OpenAFS/Tools',
             '/usr/local',
             '/usr/afsws',
             '/usr']:
    if os.path.exists('%s/include/afs/afs.h' % root):
        break

include_dirs = [os.path.join(os.path.dirname(__file__), 'afs'),
                '%s/include' % root]
library_dirs = ['%s/lib' % root,
                '%s/lib/afs' % root]
if os.path.exists('%s/lib/libafsauthent_pic.a' % root):
    suffix = '_pic'
else:
    suffix = ''
libraries = ['afsauthent%s' % suffix, 'afsrpc%s' % suffix, 'resolv']
define_macros = [('AFS_PTHREAD_ENV', None)]

def PyAFSExtension(module, *args, **kwargs):
    kwargs.setdefault('libraries', []).extend(libraries)
    kwargs.setdefault('include_dirs', []).extend(include_dirs)
    kwargs.setdefault('library_dirs', []).extend(library_dirs)
    kwargs.setdefault('define_macros', []).extend(define_macros)
    return Extension(module,
                     ["%s.pyx" % module.replace('.', '/')],
                     *args,
                     **kwargs)

setup(
    name="PyAFS",
    version="0.2.2",
    description="PyAFS - Python bindings for AFS",
    author="Evan Broder",
    author_email="broder@mit.edu",
    maintainer="Debathena Project",
    maintainer_email="debathena@mit.edu",
    url="http://github.com/ebroder/pyafs/",
    license="GPL",
    requires=['Cython'],
    packages=['afs', 'afs.tests'],
    ext_modules=[
        PyAFSExtension("afs._util"),
        PyAFSExtension("afs._acl"),
        PyAFSExtension("afs._fs"),
        PyAFSExtension("afs._pts", libraries=['krb5']),
        ],
    cmdclass= {"build_ext": build_ext}
)
