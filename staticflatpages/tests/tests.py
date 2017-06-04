import os
from django.conf import settings
from django.test import TestCase, modify_settings, override_settings

from staticflatpages import util


def _test_template_dir():
    return os.path.join(os.path.dirname(__file__), 'templates')


# Test values for settings.TEMPATES
TEST_TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [_test_template_dir()],
        'APP_DIRS': True,  # required for sitemaps
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


@override_settings(TEMPLATES=TEST_TEMPLATES)
@modify_settings(MIDDELWARE={
    'append': 'staticflatpages.middleware.StaticFlatpageFallbackMiddleware'
})
class StaticFlatpageTests(TestCase):
    urls = 'staticflatpages.tests.urls'

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


@override_settings(TEMPLATES=TEST_TEMPLATES)
@modify_settings(MIDDELWARE={
    'append': 'staticflatpages.middleware.StaticFlatpageFallbackMiddleware'
})
class StaticFlatpageUtilTests(TestCase):

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
        for template_config in settings.TEMPLATES:
            for directory in template_config['DIRS']:
                urls += util.urls_from_file_tree(directory)
        self.assertIn("/default/", urls)
        self.assertIn("/some_form/", urls)
        self.assertIn("/about/foo/", urls)
        self.assertIn("/about/bar/", urls)
        self.assertIn("/about/bar/baz/", urls)

    @override_settings(TEMPLATES=[{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ["templates"],
    }])
    def test_get_template_directories_with_template_dirs(self):
        """Should return the value of TEMPLATES if it exists and is not empty"""
        self.assertEqual(util.get_template_directories(), {'templates'})

    @override_settings(TEMPLATES=[])
    def test_get_template_directories_with_empty_template_dirs(self):
        """Should return an empty set if TEMPLATES is empty, but TEMPLATES
        is not defined"""
        self.assertEqual(util.get_template_directories(), set())

    @override_settings(TEMPLATES=[{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ["other_templates"],
    }])
    def test_get_template_directories_with_templates(self):
        """Should return a set of DIRS from TEMPLATES if those are defined."""
        self.assertEqual(util.get_template_directories(), {'other_templates'})
