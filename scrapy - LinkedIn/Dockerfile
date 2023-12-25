# `python-base` sets up all our shared environment variables
FROM python:3.10.11-slim as python-base

ENV CONTAINER_IP_ADDRESS 172.18.0.2

    # python
ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # make poetry create the virtual environment in the project's root
    # it gets named `.venv`
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    \
    # paths
    # this is where our requirements + virtual environment will live
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"


ENV PATH="/root/.local/bin:${PATH}"

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        # deps for installing poetry
        curl \
        # deps for building python deps
        build-essential


RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && apt-get -y install procps \
    && apt-get -y install postgresql-client \
    && apt-get -y install bash \
    && apt-get install -y \
    libglib2.0-0 \
    libxml2-dev \
    libxslt-dev \
    libffi-dev \
    libcairo2-dev \
    libpango1.0-0 \
    libgdk-pixbuf2.0-dev \
    libssl-dev \
    libreoffice \
    libreoffice-writer \
    libreoffice-calc \
    libcurl4-openssl-dev \
    && pip install psycopg2 \
    && pip install --upgrade pip \
    && pip install pipx \
    && rm -rf /var/lib/apt/lists/*

RUN pipx install poetry

RUN pipx upgrade poetry

# install poetry - respects $POETRY_VERSION & $POETRY_HOME
#RUN curl -sSL https://install.python-poetry.org | python3 -


RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        # Deps for installing poetry
        gnupg \
        gnupg2 \
        gnupg1 \
        # Deps for building Python dependencies
        # Additional dependencies for ChromeDriver
        wget \
        unzip \
        libnss3 \
        libgconf-2-4 \
        libfontconfig1 \
        libxss1

# Install Chrome browser
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get -y install google-chrome-stable

# copy project requirement files here to ensure they will be cached.
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

WORKDIR /app

ENV PYTHONPATH=/app

COPY . /app/

RUN poetry lock

RUN bash chromedriver.sh

RUN poetry install

CMD ["tail", "-f", "/dev/null"]

# CMD ["poetry", "run", "scrapy", "crawl", "entrypoint"]