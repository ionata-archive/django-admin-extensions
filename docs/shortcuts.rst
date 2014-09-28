.. _shortcuts:

=========================
adminextensions.shortcuts
=========================

.. _shortcuts.register:

``register``
============

This is a class decorator that makes registering ``ModelAdmin`` classes cleaner.
Instead of defining your class and then registering it later, it can all be
done in one step::

    # in app/admin.py

    from app.models import Book

    from adminextensions import ExtendedModelAdmin
    from admineasierextensions.shortcuts import register

    @register(Book)
    class BookAdmin(ExtendedModelAdmin):
        pass

Usage of this decorator is optional. The traditional ``admin.site.register`` is
still supported — this decorator is just a cleaner wrapper around it.

.. _shortcuts.link_field:

``link_field``
==============

Used in ``list_display`` to create a link to another model. For example::

    # in app/admin.py

    from app.models import Book, Author

    from adminextensions import ExtendedModelAdmin
    from adminextensions.shortcuts import link_field, register
    from django.contrib import admin

    @register(Book)
    class BookAdmin(ExtendedModelAdmin):
        list_display = ('title', link_field('author'))

    admin.site.register(Author)

By default, links from ``link_field`` point to the ``'change'`` action on the
destination model. You can change this by providing the name of another action
as the ``action`` kwarg.

The destination model is displayed using its ``__str__`` method by default.
This can be overridden by supplying a callable as the ``formatter`` kwarg. This
should accept a single argument, which is the model instance::

    class BookAdmin(ExtendedModelAdmin):
        list_display = (
            'title',
            link_field('author', formatter=lambda a: a.full_name)
        )

A short_description parameter is automatically generated based on the linked
field name. To override this, use the ``short_description`` parameter.

.. _shortcuts.model_link:

``model_link``
==============

Used in ``object_tools`` to create a link to another model. For example::

    # in app/admin.py

    from app.models import Book, Author

    from adminextensions import ExtendedModelAdmin
    from adminextensions.shortcuts import model_link, register
    from django.contrib import admin

    @register(Book)
    class BookAdmin(ExtendedModelAdmin):
        object_tools = {
            'change': [
                model_link('View author', Author, lambda book: book.author.pk),
            ]
        }


    admin.site.register(Author)

The arguments to ``model_link`` are, in order:

*  The text of the link

*  The Model class that will be linked to

*  A callable that, given an instance of the primary model (``Book``, in the
   example) will return the primary key of the related model.

By default, links from ``model_link`` point to the ``'change'`` action on the
destination model. You can change this by providing the name of another action
as the ``action`` kwarg.

If the primary key getter returns ``None``, the link is not printed.

.. _shortcuts.model_search:

``model_search``
================

Used in ``object_tools`` to create a link to the change list of another model. For
example, to link from the change view of an Author to a change list of all
Books by that Author::

    # in app/admin.py

    from app.models import Book, Author

    from adminextensions import ExtendedModelAdmin
    from adminextensions.shortcuts import model_search, register
    from django.contrib import admin

    @register(Author)
    class AuthorAdmin(ExtendedModelAdmin):
        object_tools = {
            'change': [
                model_search('Find books', Book, lambda author: {'author__pk': author.pk}),
            ]
        }

    admin.site.register(Book)

The arguments to ``model_link`` are, in order:

*  The text of the link

*  The Model class that will be linked to

*  A callable that, given an instance of the primary model (``Author``, in the
   example) will a dict of querystring parameters to use in the change list
   filter.

In the example above, where books are filtered on ``'author__pk'``,
``'author'`` would have to be added to the ``valid_lookups`` list on the
``BookAdmin``. See the :ref:`valid_lookups` documentation for more information.

.. _shortcuts.model_add:

``model_add``
=============

Used in ``object_tools`` to create a link to the add form for a model, possibly
with some defaults::

    # in app/admin.py

    from app.models import Book, Author

    from adminextensions import ExtendedModelAdmin
    from adminextensions.shortcuts import model_add, register
    from django.contrib import admin

    @register(Author)
    class AuthorAdmin(ExtendedModelAdmin):
        object_tools = {
            'change': [
                model_add('Add book', Book,
                           lambda author: {'author': author.pk}),
            ]
        }

    admin.site.register(Book)

The arguments to ``model_add`` are, in order:

*  The text of the link

*  The Model class that will be linked to

*  A callable that, given an instance of the primary model (``Author``, in the
   example) will return a ``dict`` of default values for the new instance (a
   ``Book`` in the example).

.. _shortcuts.serialized_many_to_many_field:

``serialized_many_to_many_field``
=================================

The ``serialized_many_to_many_field`` shows the contents of a many-to-many
relation inline in the admin change list::

    # in app/admin.py

    from app.models import Author, Genre

    from adminextensions import ExtendedModelAdmin
    from adminextensions.shortcuts import serialized_many_to_many_field
    from django.contrib import admin

    class AuthorAdmin(ExtendedModelAdmin):
        list_display = (
            'given_name', 'family_name',
            serialized_many_to_many_field('genre')
        )

    admin.site.register(Author, AuthorAdmin)
    admin.site.register(Genre)

The list of models is just plain text by default. Links to the models can be
printed instead, by supplying ``linked=True`` to
``serialized_many_to_many_field``.

The destination models are displayed using their ``__str__`` method by
default.  This can be overridden by supplying a callable as the ``formatter``
kwarg. This should accept a single argument, which is the model instance::

    class AuthorAdmin(ExtendedModelAdmin):
        list_display = (
            'given_name', 'family_name',
            serialized_many_to_many_field('genre',
                                          formatter=lambda g: g.name)
        )

Items in the list are joined by ``', '`` by default. This can be overridden
using the ``joiner`` kwarg.

A short_description parameter is automatically generated based on the linked
field name. To override this, use the ``short_description`` parameter::

    class AuthorAdmin(ExtendedModelAdmin):
        list_display = (
            'given_name', 'family_name',
            serialized_many_to_many_field('genre', short_description='writes')
        )

.. _shortcuts.related_field:

``related_field``
===================

The ``related_field`` shows a field on a related model in the change list.
This is used to display extra data on a related model when the default of
using the ``__str__`` method on the model does not suffice.  It can take
three arguments, with ``field`` being the only required argument.

``field`` is the double-underscore-delimited path to the field to display,
such as ``'author__name'``.

``formatter`` takes the value and formats it for display. The default is to
just return the value. The Django admin is fairly sensible at formatting
things.

``short_description`` is used as the column header. It defaults to ``field``

Example::

    # in app/admin.py

    from app.models import Author, Genre

    from adminextensions import ExtendedModelAdmin
    from adminextensions.shortcuts import related_field
    from django.contrib import admin

    class BookAdmin(ExtendedModelAdmin):
        list_display = (
            'title',
            related_field('author__name'),
        )

    admin.site.register(Book, BookAdmin)

.. _shortcuts.truncated_field:

``truncated_field``
===================

The ``truncated_field`` shows a truncated version of a field. Use this on
content fields that may have a lot of data. The data is truncated after
``length`` words. ``length`` defaults to 20::

    # in app/admin.py

    from app.models import Author, Genre

    from adminextensions import ExtendedModelAdmin
    from adminextensions.shortcuts import truncated_field
    from django.contrib import admin

    class BookAdmin(ExtendedModelAdmin):
        list_display = (
            'title', truncated_field('content', length=15),
        )

    admin.site.register(Book, BookAdmin)

A short_description parameter is automatically generated based on the linked
field name. To override this, use the ``short_description`` parameter.

If the field contains HTML, pass ``strip_html=True`` to the function to strip
it out.
