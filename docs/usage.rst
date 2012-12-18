.. _usage:

=====
Usage
=====

To enable extended functionality in your Django admin, your admin class needs
to extend ``ExtendedModelAdmin``, like so::

    # in app/admin.py

    from app.models import Book

    from adminextensions import ExtendedModelAdmin
    from django.contrib import admin

    class BookAdmin(ExtendedModelAdmin):
        pass

    admin.site.register(Book, BookAdmin)

Everything else in this documentation will assume that you are using the
``ExtendedModelAdmin`` base class.

.. _object_tools:

Extending the Object Tools list
===============================

The buttons to the top-right of every Django admin screen are called object
tools. ``django-admin-extensions`` allows you to easily add new links to the
object tools, with out having to extend and override the admin templates::

    # in app/admin.py

    from app.models import Author

    from adminextensions import ExtendedModelAdmin
    from django.contrib import admin

    class AuthorAdmin(ExtendedModelAdmin):

        object_tools = {
            'add': [...],
            'change': [...],
            'changelist': [...],
        }

    admin.site.register(Author, AuthorAdmin)

The ``'add'``, ``'change'``, and ``'changelist'`` lists should be populated
with callables. These callables will be called with the template context as
their only argument. They should return a string, which will be wrapped in a
``<li>`` tag and printed to the screen as an object tool. To duplicate the
'View on site' object tool, you could do the following::

    def absolute_url(context):
        object = content['original']
        if not hasattr(object, 'get_absolute_url'):
            return ''

        return '<a href="{0}">{1}</a>'.format(
            original.get_absolute_url(), 'View on site')

    class AuthorAdmin(ExtendedModelAdmin):

        object_tools = {
            'change': [ absolute_url ],
        }

The most common use case is adding links to related models on the ``'change'``
view. This can be achived using the folloing code::

    class AuthorAdmin(ExtendedModelAdmin):
        object_tools = {
            'change': [
                model_search('Find books', Book,
                    lambda author: {'book__author__pk': author.pk}),

                model_link('View publisher', Publisher,
                    lambda book: author.publisher.pk),
            ]
        }

Here, a link is created to the ``changelist`` showing all books written by the
current author, and a link is created to the change view of the authors
publisher. These make use of the :ref:`shortcuts.model_search` and
:ref:`shortcuts.model_link` shortcuts.

.. _valid_lookups:

``valid_lookups``
=================

By default, the Django admin does not allow filtering via GET parameters on
related models. This is for securiry reasons - filtering on related models is a
potentially expensive operation, and a denial of service attack could be
constructed by abusing this.

Some times though, these kind of look ups are exatly what we want.
``valid_lookups`` is a whitelist of related model lookups that should be
allowed by the admin. Use it like this::

    class BookAdmin(ExtendedModelAdmin):

        valid_lookups = (
            'author__pk'
        )

This allows for lookups on a Book's Author's primary key - and nothing more.
You will likely have to add a related fields primary key to this list every
time you use :ref:`shortcuts.model_search` in the ``object_tools``.
