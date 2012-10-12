import os
from django.conf import settings
from django.test import TestCase


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
