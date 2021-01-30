FROM python:3.8-slim

RUN set -ex; \
    python -m pip install setuptools wheel twine

COPY . /src
RUN set -ex; \
    python -m pip install -r /src/requirements.txt
