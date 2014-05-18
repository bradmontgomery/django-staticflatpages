from os import walk
from os.path import join
from re import sub


def _format_as_url(path):
    """Make sure ``path`` takes the form of ``/some/url/``."""
    path = sub(r"\.html$", '', path)  # remove any ending .html

    # Make sure it starts/ends with a slash.
    if not path.startswith("/"):
        path = "/{0}".format(path)
    if not path.endswith("/"):
        path = "{0}/".format(path)

    return path


def urls_from_file_tree(template_dir):
    """Generates a list of URL strings that would match each staticflatpage."""
    urls = []  # keep a list of of all the files/paths

    # Should be somethign like:
    # /path/to/myproject/templates/staticflatpages
    root_dir = join(template_dir, 'staticflatpages')

    for root, dirs, files in walk(template_dir):
        # Only do this for the ``staticflatpages`` directory or sub-directories
        if "staticflatpages" in root:
            root = root.replace(root_dir, '')
            for f in files:
                path = join(root, f)
                path = _format_as_url(path)
                urls.append(path)
    return urls


class Url(object):
    """A light-weight class whose instances are accessed via a Sitemap's
    ``items`` method.

    """
    def __init__(self, *args, **kwargs):
        self.url = ''
        if len(args) > 0:
            self.url = args[0]
        elif "url" in kwargs:
            self.url = kwargs['url']

    def get_absolute_url(self):
        return self.url


def url_objects_from_file_tree(template_dir):
    """Generates a list of ``Url`` instances for each url returned by
    ``urls_from_file_tree``."""
    return [Url(u) for u in urls_from_file_tree(template_dir)]
