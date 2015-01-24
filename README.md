# Pic Tour

A self-guided photo tour of London.

Created by [Ben Emery](https://github.com/benemery), [Ollie Bennett](https://github.com/olliebennett), [Shlomie Liberow](https://twitter.com/shlibness) and [Krishan Patel](https://github.com/krishan711) during the [London Dropbox Hackathon](https://www.dropbox.com/developers/blog/117/london-dropbox-hackathon).

## Setup

    cd pictour

Install requirements

    pip install -r droptour/requirements.txt

Run tests

    ./manage.py test photo_geoip

Configure secret vars in a `droptoup/settings_local.py` file, as documented in `settings.py`.

Create database (follow prompts to create a superuser)

    ./manage.py syncdb

Run server

    ./manage.py runserver

Visit admin panel at [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)!

Set up a tunnel to localhost:8000 (eg. using [Ngrok](https://ngrok.com/)).

    ./ngrok 8000

Use [Dropbox Console](https://www.dropbox.com/developers/apps) to configure your app's webhook to

    http://your-random-subdomain.ngrok.com/webhook

Introspect incoming requests at  [http://localhost:4040](http://localhost:4040).

Sync a `.jpg` into your Dropbox (via Camera Upload) and the server should be hit!
