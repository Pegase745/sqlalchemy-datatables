"""Markdown to RST doc conversion before registering on PyPi."""
import pandoc
import os

pandoc.core.PANDOC_PATH = '/usr/bin/path'


doc = pandoc.Document()
doc.markdown = open('README.md').read()
f = open('README.rst', 'w+')
f.write(doc.rst)
f.close()
os.system('setup.py register')
os.remove('README.rst')
