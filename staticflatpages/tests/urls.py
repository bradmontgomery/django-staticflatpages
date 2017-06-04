from django.conf.urls import url
from django.contrib.sitemaps import views

from staticflatpages.sitemaps import StaticFlatpageSitemap


sitemaps = {
    'staticflatpages': StaticFlatpageSitemap,
}


urlpatterns = [
    url(
        r'^sitemap\.xml$',
        views.index,
        {'sitemaps': sitemaps},
        name="test-sitemap-index"
    ),
    url(
        r'^sitemap-(?P<section>.+)\.xml$',
        views.sitemap,
        {'sitemaps': sitemaps},
        name="test-sitemap-section"
    ),
]
