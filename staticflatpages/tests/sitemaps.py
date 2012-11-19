from __future__ import unicode_literals

import os

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.unittest import skipUnless


class StaticFlatpageSitemapTest(TestCase):
    protocol = 'http'
    domain = 'example.com' if Site._meta.installed else 'testserver'
    urls = 'staticflatpages.tests.urls'

    def setUp(self):
        self.old_MIDDLEWARE_CLASSES = settings.MIDDLEWARE_CLASSES
        m = 'staticflatpages.middleware.StaticFlatpageFallbackMiddleware'
        if m not in settings.MIDDLEWARE_CLASSES:
            settings.MIDDLEWARE_CLASSES += (m)
        self.old_TEMPLATE_DIRS = settings.TEMPLATE_DIRS
        settings.TEMPLATE_DIRS = (
            os.path.join(
                os.path.dirname(__file__),
                'templates'
            ),
        )
        self.base_url = '%s://%s' % (self.protocol, self.domain)

    def tearDown(self):
        settings.MIDDLEWARE_CLASSES = self.old_MIDDLEWARE_CLASSES
        settings.TEMPLATE_DIRS = self.old_TEMPLATE_DIRS

    @skipUnless("staticflatpages" in settings.INSTALLED_APPS,
                "staticflatpages app not installed.")
    def test_sitemap(self):
        """Basic StaticFlatPage sitemap test"""
        url = reverse('sitemap')  # default sitemap
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        loc = '<loc>{0}{1}</loc>'.format(
            self.base_url,
            reverse('sitemap_section', args=['staticflatpages'])
        )
        self.assertContains(response, loc)

    @skipUnless("staticflatpages" in settings.INSTALLED_APPS,
                "staticflatpages app not installed.")
    def test_sitemap_staticflatpages(self):
        """Test that sitesmaps exist for installed staticflatpges"""
        url = reverse('sitemap_section', args=['staticflatpages'])
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
