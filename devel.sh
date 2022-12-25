#!/bin/bash
set -e

flask --app urlshortner.__main__:app --debug run
