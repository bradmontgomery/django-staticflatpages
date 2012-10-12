django-staticflatpages
======================

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

Install this app with pip:

``pip install django-staticflatpages``

Or install it directly from this repo:

``pip install -e git+git://github.com/bradmontgomery/django-staticflatpages.git#egg=django-staticflatpages``

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
"templates", the url ``/about/`` will point to
``templates/staticflatpages/about.html``. Likewise, the url ``/about/team/``
will point to ``templates/staticflatpages/about/team.html``.

License
-------

This code is distributed under the terms of the MIT license. See the
``LICENSE`` file.

