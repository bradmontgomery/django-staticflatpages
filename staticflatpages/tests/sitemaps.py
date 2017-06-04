from __future__ import unicode_literals

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.test import TestCase, modify_settings, override_settings
from django.test.utils import skipUnless

from .tests import TEST_TEMPLATES


@override_settings(SITE_ID=1)
@override_settings(ROOT_URLCONF='staticflatpages.tests.urls')
@override_settings(TEMPLATES=TEST_TEMPLATES)
@modify_settings(INSTALLED_APPS={'append': 'django.contrib.sites'})
@modify_settings(INSTALLED_APPS={'append': 'django.contrib.sitemaps'})
@modify_settings(MIDDELWARE={
    'append': 'staticflatpages.middleware.StaticFlatpageFallbackMiddleware'
})
class StaticFlatpageSitemapTest(TestCase):
    urls = 'staticflatpages.tests.urls'

    def setUp(self):
        protocol = 'http'
        domain = 'example.com' if Site._meta.installed else 'testserver'
        self.base_url = '%s://%s' % (protocol, domain)

    @skipUnless("staticflatpages" in settings.INSTALLED_APPS,
                "staticflatpages app not installed.")
    def test_sitemap(self):
        """Basic StaticFlatPage sitemap test"""
        url = reverse('test-sitemap-index')  # default sitemap
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        loc = '<loc>{0}{1}</loc>'.format(
            self.base_url,
            reverse('test-sitemap-section', args=['staticflatpages'])
        )
        self.assertContains(response, loc)

    @skipUnless("staticflatpages" in settings.INSTALLED_APPS,
                "staticflatpages app not installed.")
    def test_sitemap_staticflatpages(self):
        """Test that sitesmaps exist for installed staticflatpges"""
        url = reverse('test-sitemap-section', args=['staticflatpages'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Should contain something like the following for every staticflatpage
        #
        # <url>
        #   <loc>http://example.com/about/bar/</loc>
        #   <changefreq>never</changefreq>
        #   <priority>0.5</priority>
        # </url>

        loc = '<loc>{0}{1}</loc>'.format(self.base_url, "/about/bar/")
        self.assertContains(response, loc)
        loc = '<loc>{0}{1}</loc>'.format(self.base_url, "/about/bar/baz/")
        self.assertContains(response, loc)
        loc = '<loc>{0}{1}</loc>'.format(self.base_url, "/about/foo/")
        self.assertContains(response, loc)
