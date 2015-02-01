.. image:: https://travis-ci.org/benemery/pictour.svg?branch=master
    :target: https://travis-ci.org/benemery/pictour


Pic Tour
========

A self-guided photo tour of London.

Created by `Ben Emery <https://github.com/benemery>`_, `Ollie Bennett <https://github.com/olliebennett>`_, `Shlomie Liberow <https://github.com/shlib92>`_ and `Krishan Patel <https://github.com/krishan711>`_ during the `London Dropbox Hackathon <https://www.dropbox.com/developers/blog/117/london-dropbox-hackathon>`_.

Setup
-----

.. code-block:: console

    $ cd pictour

Install requirements

.. code-block:: console

    $ pip install -r droptour/requirements.txt

Run tests

.. code-block:: console

    $ ./manage.py test photo_geoip

Configure secret vars in a `droptoup/settings_local.py` file, as documented in `settings.py`.

Create database (follow prompts to create a superuser)

.. code-block:: console

    $ ./manage.py syncdb

Run server

.. code-block:: console

    $ ./manage.py runserver

Visit admin panel at `http://127.0.0.1:8000/admin/ <http://127.0.0.1:8000/admin/>`_!

Set up a tunnel to localhost:8000 (eg. using `Ngrok <https://ngrok.com/>`_).

.. code-block:: console

    $ ./ngrok 8000

Create a Dropbox app `here <https://www.dropbox.com/developers/apps/create>`_. Options:

- App type: 'Dropbox API app'
- Data types: 'Files and datastores'
- Limit to folder: No (need files already on Dropbox)
- File access: Specific file type: 'Images'.
- Name: whatever!

Use `Dropbox Console <https://www.dropbox.com/developers/app>`_ to configure your app's webhook to

.. code-block:: console

    http://your-random-subdomain.ngrok.com/webhook

Introspect incoming requests at  `http://localhost:4040 <http://localhost:4040>`_.

Sync a :code:`.jpg` into your Dropbox (via Camera Upload) and the server should be hit!
