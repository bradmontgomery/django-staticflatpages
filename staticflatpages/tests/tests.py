import os
from django.conf import settings
from django.test import TestCase

from staticflatpages import util


class StaticFlatpageTests(TestCase):

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

    def tearDown(self):
        settings.MIDDLEWARE_CLASSES = self.old_MIDDLEWARE_CLASSES
        settings.TEMPLATE_DIRS = self.old_TEMPLATE_DIRS

    def test_staticflatpage(self):
        """A staticflatpage will be served by the fallback middleware"""
        response = self.client.get('/default/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<p>hello world</p>")

    def test_non_existent_staticflatpage(self):
        """A non-existent staticflatpage raises a 404."""
        response = self.client.get('/no_such_page/')
        self.assertEqual(response.status_code, 404)

    def test_csrftoken_in_staticflatpage(self):
        """A non-existent staticflatpage raises a 404."""
        response = self.client.get('/some_form/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "csrfmiddlewaretoken")


class StaticFlatpageUtilTests(TestCase):
    def setUp(self):
        self.TEMPLATE_DIRS = (
            os.path.join(
                os.path.dirname(__file__),
                'templates'
            ),
        )
    
    def test__format_as_url(self):
        """Make sure a list of paths are formatted as absolute URLs."""
        input_urls = ['foo', '/bar', 'baz/', 'wooo/boy', 'yippe/kai/aye']
        output_urls = []
        for url in input_urls:
            output_urls.append(util._format_as_url(url))
        self.assertIn('/foo/', output_urls)
        self.assertIn('/bar/', output_urls)
        self.assertIn('/baz/', output_urls)
        self.assertIn('/wooo/boy/', output_urls)
        self.assertIn('/yippe/kai/aye/', output_urls)

    def test_urls_from_file_tree(self):
        urls = []
        for directory in self.TEMPLATE_DIRS:
            urls += util.urls_from_file_tree(directory)
        self.assertIn("/default/", urls)
        self.assertIn("/some_form/", urls)
        self.assertIn("/about/foo/", urls)
        self.assertIn("/about/bar/", urls)
        self.assertIn("/about/bar/baz/", urls)
