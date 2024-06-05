FROM ubuntu:22.04 as builder

ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies required for Pyenv
RUN apt-get update && apt-get install -y --no-install-recommends \
    make \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    wget \
    curl \
    llvm \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libxml2-dev \
    libxmlsec1-dev \
    libffi-dev \
    liblzma-dev \
	ca-certificates \
	git

# Install Pyenv
RUN curl https://pyenv.run | bash

## Set environment variables for Pyenv
ENV HOME=/root
ENV PYENV_ROOT=$HOME/.pyenv
ENV PATH="$PYENV_ROOT/bin:$PATH"

RUN pyenv install 3.11.2

# for the location of pip
ENV PATH="$PYENV_ROOT/versions/3.11.2/bin:$PATH"
# to get rid of annoying error for using pip as root
# see https://stackoverflow.com/questions/68673221/warning-running-pip-as-the-root-user
ENV PIP_ROOT_USER_ACTION=ignore

# Install Poetry
RUN pip install poetry==1.7

## Copy application to container
COPY . /app
WORKDIR /app

# Build the project using Poetry
#RUN poetry build

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --no-root --without test --with prod

# Stage 2: Run environment with Distroless Python image
# I chose this image because its hosted on gcr.io and is viewable on Github
# Its the only distroless on gcr.io with python pre-installed
# The python version it uses can be found at https://github.com/GoogleContainerTools/distroless/blob/main/python3/testdata/debian12.yaml
# python version is 3.11.2 as off 29-dec-23
FROM gcr.io/distroless/python3-debian12:latest

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

# Copy app folder and dependencies to distroless
COPY --from=builder /app /app

# Set the path to the virtual environment's site-packages in the distroless image
ENV PYTHONPATH=/app/.venv/lib/python3.11/site-packages

# Set the working directory in the distroless image
WORKDIR /app

# Default command to run the app
CMD ["gunicorn_standalone.py"]
