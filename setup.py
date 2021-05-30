from distutils.core import setup
import py2exe, sys, os

sys.argv.append('py2exe')

setup(
    options = {'py2exe': {'includes': ["pygame", "easygui", "sys", "random", "ast"], 'bundle_files': 1, 'compressed': True}},
    console = [{'script': "tictactoe.py"}],
)
