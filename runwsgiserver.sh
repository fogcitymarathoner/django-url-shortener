#!/bin/bash
#
# Runs the WSGI server.
#
uwsgi --uwsgi localhost:8087 --pidfile=pid.txt --touch-reload=reload --wsgi-file /home/marc/python_apps/tinyurl_sfdjango/wsgi.py
#while [ true ] ; do
#done

