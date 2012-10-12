from django.template import RequestContext
from django.template.loader import TemplateDoesNotExist
from django.http import Http404
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response


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
        return render_to_response(path, {},
            context_instance=RequestContext(request))
    except TemplateDoesNotExist:
        raise Http404
