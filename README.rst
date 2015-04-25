django-staticflatpages
======================

|version| |license|

*like flatpages, but with templates*

This is like Django's ``contrib.flatpages``, but without the database. It's
just static html documents served from your filesystem.

Motivation
----------

I've been using the ``flatpages`` app for a long time, but somewhere along the
line I started keeping my flatpage content (snippets of html) in the git repo
with the rest of my project. Any time I made a change to a flatpage, I'd edit
the file locally, commit the changes, then copy and paste the new content into
the relevant flatpage.

Why not just serve these from my templates directory?

That's what ``staticflatpages`` does.

Installation
------------

Install the latest release with pip:

``pip install django-staticflatpages``


Configuration
-------------

1. Add ``staticflatpages`` to your ``INSTALLED_APPS``.
2. Add ``staticflatpages.middleware.StaticFlatpageFallbackMiddleware`` to your
   ``MIDDLEWARE_CLASSES``
3. Create a ``staticflatpages`` template directory. This should be a
   subdirectory of one of the templates in your ``TEMPLATE_DIRS``. Any
   templates you include here (except for a ``base.html``) will get served as
   a static page.

For example, assuming your project-level template directory is named
"templates", then:

* The url ``/about/`` will render ``templates/staticflatpages/about.html``
* The url ``/about/team/`` will render ``templates/staticflatpages/about/team.html``


Sitemaps
--------
This app also supports sitemaps for staticflatpages. To enable these, you'll
need to have ``django.contrib.sitemaps`` listed in your INSTALLED_APPS. Then,
just set up a sitemap (e.g. in your Root URLconf)::

    from staticflatpages.sitemaps import StaticFlatpageSitemap

    sitemaps = {
        'staticflatpages': StaticFlatpageSitemap,
    }

Then include your sitemaps urls as normal::

    urlpatterns += patterns('django.contrib.sitemaps.views',
        url(r'^sitemap\.xml$', 'index', {'sitemaps': sitemaps}),
        url(r'^sitemap-(?P<section>.+)\.xml$',
            'sitemap',
            {'sitemaps': sitemaps}
        ),
    )


Settings
--------

If you use the sitemaps feature, you may also want to include the following
settings:

* ``STATICFLATPAGES_CHANGEFREQ``: Corresponds to the ``Sitemap.changefreq``
  attribute (defaults to ``never``).
* ``STATICFLATPAGES_PRIORITY``: Corresponds to the ``Sitemap.priority``
  attribute (defaults to 0.5).


License
-------

This code is distributed under the terms of the MIT license. See the
``LICENSE`` file.


.. |version| image:: http://img.shields.io/pypi/v/django-staticflatpages.svg?style=flat-square
    :alt: Current Release
    :target: https://pypi.python.org/pypi/django-staticflatpages/

.. |license| image:: http://img.shields.io/pypi/l/django-staticflatpages.svg?style=flat-square
    :alt: License
    :target: https://pypi.python.org/pypi/django-staticflatpages/
