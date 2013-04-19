#!/usr/bin/env python
import os
import sys
import subprocess
import shutil

pwd = os.path.abspath(os.path.dirname(__file__))
vedir = os.path.abspath(os.path.join(pwd,"ve"))

clear = True
if len(sys.argv) > 1:
    if sys.argv[1] == "--fast":
        clear = False
if clear and os.path.exists(vedir):
    shutil.rmtree(vedir)

virtualenv_support_dir = os.path.abspath(os.path.join(pwd, "requirements", "virtualenv_support"))

ret = subprocess.call(["python", "virtualenv.py", 
                       "--extra-search-dir=%s" % virtualenv_support_dir,
                       "--never-download",
                       vedir])
if ret: exit(ret)

ret = subprocess.call([os.path.join(vedir, 'bin', 'pip'), "install",
                       "-E", vedir,
                       "--enable-site-packages",
                       "--index-url=''",
                       "--requirement",os.path.join(pwd,"requirements/apps.txt")])
if ret: exit(ret)

if sys.version_info < (2, 7, 0):
    ret = subprocess.call(
        [os.path.join(vedir, 'bin', 'pip'), "install",
         "-E", vedir,
         os.path.join(pwd,"requirements/src/importlib-1.0.1.tar.gz")])

ret = subprocess.call(["python","virtualenv.py","--relocatable",vedir])
# --relocatable always complains about activate.csh, which we don't really
# care about. but it means we need to ignore its error messages
