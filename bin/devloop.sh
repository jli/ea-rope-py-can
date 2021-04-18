#!/bin/sh

fswatch -o -e .mypy_cache . | while read _; do clear; date;./bin/typecheck.sh; ./bin/test.sh; done
