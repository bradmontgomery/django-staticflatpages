from os import walk
from os.path import join
from re import sub


def _format_as_url(path):
    path = sub("\.html$", '', path)  # remove any ending .html

    # Make sure it starts/ends with a slash.
    if not path.startswith("/"):
        path = "/{0}".format(path)
    if not path.endswith("/"):
        path = "{0}/".format(path)

    return path


def urls_from_file_tree(template_dir):
    """Generates a list of URLs that would match each staticflatpage."""
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
