FROM python:3.8-slim

RUN set -ex; \
    python -m pip install setuptools wheel twine
