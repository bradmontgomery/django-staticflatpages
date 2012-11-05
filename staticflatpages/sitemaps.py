from django.contrib.sitemaps import Sitemap
from django.conf import settings

from .util import url_objects_from_file_tree


class StaticFlatpageSitemap(Sitemap):
    changefreq = getattr(settings, 'STATICFLATPAGES_CHANGEFREQ', 'never')
    priority = getattr(settings, 'STATICFLATPAGES_PRIORITY', '0.5')

    def items(self):
        urls = []
        for directory in settings.TEMPLATE_DIRS:
            urls += url_objects_from_file_tree(directory)
        return urls
