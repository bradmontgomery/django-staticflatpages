from views import staticflatpage
from django.http import Http404
from django.conf import settings


class StaticFlatpageFallbackMiddleware(object):
    def process_response(self, request, response):
        # Only check if there's a 404 for the original response
        if response.status_code != 404:
            return response
        try:
            return staticflatpage(request, request.path_info)
        # Return the original response if any errors happened. Because this
        # is a middleware, we can't assume the errors will be caught elsewhere.
        except Http404:
            return response
        except:
            if settings.DEBUG:
                raise
            return response
