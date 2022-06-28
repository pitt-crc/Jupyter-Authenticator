"""Define the semantic version number for the parent application"""

# Add 'dev' to the end of the tuple if desired
version_info = (0, 3, 0,)
__version__ = '.'.join(map(str, version_info[:3]))

if len(version_info) > 3:
    __version__ = '%s-%s' % (__version__, version_info[3])
