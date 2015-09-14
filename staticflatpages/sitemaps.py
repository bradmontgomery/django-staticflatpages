from django.contrib.sitemaps import Sitemap
from django.conf import settings

from .util import get_template_directories, url_objects_from_file_tree


class StaticFlatpageSitemap(Sitemap):
    changefreq = getattr(settings, 'STATICFLATPAGES_CHANGEFREQ', 'never')
    priority = getattr(settings, 'STATICFLATPAGES_PRIORITY', '0.5')

    def items(self):
        urls = []
        for directory in get_template_directories():
            urls += url_objects_from_file_tree(directory)
        return urls
