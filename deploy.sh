#!/bin/bash
set -e

gunicorn --bind 0.0.0.0:5000 urlshortner.__main__:app
