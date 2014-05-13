django-url-shortener
====================

django-url-shortener

uses env 'tiny'

based on https://github.com/nileshk/url-shortener
which broke on Django 1.4 with the deprecation of generic views.

still in clean up mode. not ready for public consumption.

Install virtualenvwrapper
Make specialized environment for tinyurl 'tiny'
  mkvirtualenv tiny
  workon tiny
  pip install -r shortener/requirements.txt

  python manage.py runserver 0.0.0.0:8000
