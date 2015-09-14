import os
from django.conf import settings
from django.test import TestCase

from staticflatpages import util


class StaticFlatpageTests(TestCase):
    urls = 'staticflatpages.tests.urls'

    def _test_template_dir(self):
        return os.path.join(os.path.dirname(__file__), 'templates')

    def setUp(self):
        self.old_MIDDLEWARE_CLASSES = settings.MIDDLEWARE_CLASSES
        m = 'staticflatpages.middleware.StaticFlatpageFallbackMiddleware'
        if m not in settings.MIDDLEWARE_CLASSES:
            settings.MIDDLEWARE_CLASSES += (m)

        # Check for new-style template settings.
        if hasattr(settings, 'TEMPLATES'):
            for template_settings in settings.TEMPLATES:
                template_settings['DIRS'].append(self._test_template_dir())
        else:
            self.old_TEMPLATE_DIRS = settings.TEMPLATE_DIRS
            settings.TEMPLATE_DIRS = (self._test_template_dir(), )

    def tearDown(self):
        settings.MIDDLEWARE_CLASSES = self.old_MIDDLEWARE_CLASSES
        if hasattr(settings, 'TEMPLATES'):
            for template_settings in settings.TEMPLATES:
                template_settings['DIRS'].remove(self._test_template_dir())
        else:
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
        """You should be able to include a CSRF token in a template."""
        response = self.client.get('/some_form/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "csrfmiddlewaretoken")


class StaticFlatpageUtilTests(TestCase):
    urls = 'staticflatpages.tests.urls'

    def setUp(self):
        self.TEMPLATE_DIRS = (
            os.path.join(
                os.path.dirname(__file__),
                'templates'
            ),
        )
        if hasattr(settings, 'TEMPLATES'):
            self._original_templates = settings.TEMPLATES
        if hasattr(settings, 'TEMPLATE_DIRS'):
            self._original_template_dirs = settings.TEMPLATE_DIRS

    def tearDown(self):
        """replace altered settings."""
        if hasattr(self, '_original_templates'):
            settings.TEMPLATES = self._original_templates
        if hasattr(self, '_original_template_dirs'):
            settings.TEMPLATE_DIRS = self._original_template_dirs

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

    def test_get_template_directories_with_template_dirs(self):
        """Should return the value of TEMPLATE_DIRS if it exists and is not empty"""
        settings.TEMPLATE_DIRS = ['templates']
        self.assertEqual(util.get_template_directories(), {'templates'})

    def test_get_template_directories_with_empty_template_dirs(self):
        """Should return an empty set if TEMPLATE_DIRS is empty, but TEMPLATES
        is not defined"""
        if hasattr(settings, 'TEMPLATES'):
            del settings.TEMPLATES
        self.TEMPLATE_DIRS = ()
        settings.TEMPLATE_DIRS = ()
        self.assertEqual(util.get_template_directories(), set())

    def test_get_template_directories_with_templates(self):
        """Should return a set of DIRS from TEMPLATES if those are defined."""
        self.TEMPLATE_DIRS = ()
        if hasattr(settings, 'TEMPLATE_DIRS'):
            del settings.TEMPLATE_DIRS
        settings.TEMPLATES = [{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': ["other_templates"],
        }]
        self.assertEqual(util.get_template_directories(), {'other_templates'})
