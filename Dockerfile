# https://medium.com/@albertazzir/blazing-fast-python-docker-builds-with-poetry-a78a66f5aed0
# The builder image, used to build the virtual environment
FROM python:3.12-slim as builder

WORKDIR /code

ENV YOUR_ENV=${YOUR_ENV} \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.8.2 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    NODE_VERSION=20.12.2

RUN apt update \
    && apt install -y libxml2-dev libxslt-dev python3-setuptools curl \
    && apt clean

# Install dependencies
RUN pip install "poetry==$POETRY_VERSION"
COPY poetry.lock pyproject.toml /code/
RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --without dev --no-root


# BUILD FRONTEND
# RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
# ENV NVM_DIR=/root/.nvm
# RUN . "$NVM_DIR/nvm.sh" && nvm install ${NODE_VERSION}
# RUN . "$NVM_DIR/nvm.sh" && nvm use v${NODE_VERSION}
# RUN . "$NVM_DIR/nvm.sh" && nvm alias default v${NODE_VERSION}
# ENV PATH="/root/.nvm/versions/node/v${NODE_VERSION}/bin/:${PATH}"
# RUN node --version
# RUN npm --version

# WORKDIR /code/frontend
# RUN node run build


# The runtime image, used to just run the code provided its virtual environment
FROM python:3.12-slim as runtime

RUN apt update \
    && apt install -y supervisor \
    && apt clean

ENV YOUR_ENV=${YOUR_ENV} \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONHASHSEED=random \
    VIRTUAL_ENV_SRC=/code/.venv \
    VIRTUAL_ENV_DST=/code/.venv \
    PATH="/code/.venv/bin:$PATH"

WORKDIR /code
COPY . /code
COPY --from=builder ${VIRTUAL_ENV_SRC} ${VIRTUAL_ENV_DST}
# COPY deploy/supervisord/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
