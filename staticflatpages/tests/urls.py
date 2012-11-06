from django.conf.urls import patterns, url
from staticflatpages.sitemaps import StaticFlatpageSitemap

sitemaps = {
    'staticflatpages': StaticFlatpageSitemap,
}

urlpatterns = patterns('django.contrib.sitemaps.views',
    url(r'^sitemap\.xml$', 'index', {'sitemaps': sitemaps}, name="sitemap"),
    url(r'^sitemap-(?P<section>.+)\.xml$', 'sitemap', {'sitemaps': sitemaps},
        name="sitemap_section"),
)
