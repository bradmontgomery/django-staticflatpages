from django.urls import include, path
from django.contrib.sitemaps import views
from staticflatpages.sitemaps import StaticFlatpageSitemap


sitemaps = {
    'staticflatpages': StaticFlatpageSitemap,
}


urlpatterns = [
    path(
        'sitemap-<section>.xml',
        views.sitemap,
        {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'
    ),
    path(
        'sitemap.xml',
        views.index,
        {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'
    ),

]
