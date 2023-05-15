FROM python:3.9.13

# Setup pipx and poetry
ENV POETRY_VERSION=1.3.2
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

# Install poetry separated from system interpreter
RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# Add `poetry` to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

# Poetry setup
COPY pyproject.toml /tienda-amiga-playground/pyproject.toml
COPY poetry.lock /tienda-amiga-playground/poetry.lock
WORKDIR /tienda-amiga-playground
RUN poetry install --no-root
COPY . /tienda-amiga-playground/
RUN poetry install --no-interaction
