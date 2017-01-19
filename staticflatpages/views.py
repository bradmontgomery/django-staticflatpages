from django.template.loader import TemplateDoesNotExist
from django.http import Http404
from django.shortcuts import render


def staticflatpage(request, path):
    """Load/render a template corresponding to the path (a URL)"""
    # Don't render a base.html template.
    if path.replace("/", '').lower() == "base":
        raise Http404

    if not path.startswith('/'):
        path = "/{0}".format(path)
    if path.endswith('/'):
        path = path[:-1]

    # paths should be in the format: staticflatpages/path/from/url.html
    path = "staticflatpages{0}.html".format(path)
    try:
        return render(request, path)
    except TemplateDoesNotExist:
        raise Http404

