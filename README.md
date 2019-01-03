django-staticflatpages
======================

[![Current Release](http://img.shields.io/pypi/v/django-staticflatpages.svg?style=flat-square)](https://pypi.python.org/pypi/django-staticflatpages/)
[![License](http://img.shields.io/pypi/l/django-staticflatpages.svg?style=flat-square)](https://pypi.python.org/pypi/django-staticflatpages/)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg?style=flat-square)](https://github.com/bradmontgomery/django-staticflatpages/releases)

**It's like flatpages, but with templates**

This is like Django's built-in `contrib.flatpages` app, but without the database.
It's just static html documents served from your filesystem.

## Motivation

I've been using the `flatpages` app for a long time, but somewhere along the
line I started keeping my flatpage content (snippets of html) in the git repo
with the rest of my project. Any time I made a change to a flatpage, I'd edit
the file locally, commit the changes, then copy and paste the new content into
the relevant flatpage.

Why not just serve these from my templates directory?

That's what `staticflatpages` does.

## Installation

Install the latest release with pip:

    pip install django-staticflatpages


## Compatibility

The most recent version of this app targets Django 2.1+ and Python 3.6+. Download a
[previous release](https://github.com/bradmontgomery/django-staticflatpages/releases/tag/0.5.0)
for older versions of Django.

You can run the test suite with `python manage.py test staticflatpages`, and open an
[Issue on Github](https://github.com/bradmontgomery/django-staticflatpages/issues)
if you run into any problems.


## Configuration

1. Add `staticflatpages` to your `INSTALLED_APPS`.
2. Add `staticflatpages.middleware.StaticFlatpageFallbackMiddleware` to your
   `MIDDLEWARE` settings.
3. Create a `staticflatpages` template directory. This should be a
   subdirectory of one of the templates in your `TEMPLATES` setting. Any
   templates you include here (except for a `base.html`) will get served as
   a static page.

For example, assuming your project-level template directory is named
"templates", then:

* The url `/about/` will render `templates/staticflatpages/about.html`
* The url `/about/team/` will render `templates/staticflatpages/about/team.html`
* If you include an index template (`templates/staticflatpages/index.html`), and
  no other url maps to `/`, it will get used as your index.


## Sitemaps

This app also supports sitemaps for staticflatpages. To enable these, you'll
need to have `django.contrib.sitemaps` listed in your `INSTALLED_APPS` setting.
Then, set up a sitemap (e.g. in your Root URLconf):

    from staticflatpages.sitemaps import StaticFlatpageSitemap

    sitemaps = {
        'staticflatpages': StaticFlatpageSitemap,
    }

Don't forget to include your sitemaps urls as normal, e.g.:


    path(
        'sitemap-<section>.xml',
        sitemaps_views.sitemap,
        {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'
    ),
    path(
        'sitemap.xml',
        sitemaps_views.index,
        {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'
    ),


*NOTE*: The `sitemaps` framework also requires the `sites` framework so you'll
need that installed, and you'll also need to define a `SITE_ID`.


## Settings

If you use the sitemaps feature, you may also want to include the following
settings:

* `STATICFLATPAGES_CHANGEFREQ`: Corresponds to the `Sitemap.changefreq`
  attribute (defaults to `never`).
* `STATICFLATPAGES_PRIORITY`: Corresponds to the `Sitemap.priority`
  attribute (defaults to 0.5).


## Misc

This app could work with with [django-dirtyedit](https://github.com/synw/django-dirtyedit),
which allows you to edit files from the admin (if you're so inclined).

License
-------

This code is distributed under the terms of the MIT license. See the
`LICENSE` file.

