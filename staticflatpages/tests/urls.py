from django.conf.urls import url
from staticflatpages.sitemaps import StaticFlatpageSitemap


sitemaps = {
    'staticflatpages': StaticFlatpageSitemap,
}


urlpatterns = [
    url(
        r'^sitemap\.xml$',
        'index',
        {'sitemaps': sitemaps},
        name="sitemap"
    ),
    url(
        r'^sitemap-(?P<section>.+)\.xml$',
        'sitemap',
        {'sitemaps': sitemaps},
        name="sitemap_section"
    ),
]
