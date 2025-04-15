FROM python:3.13-alpine3.19 AS builder

ARG GITLAB_TOKEN
ARG SERVER_HOST

# environment variables
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_NO_INTERACTION=1

RUN apk add --no-cache git=2.43.6-r0 && \
    (cp /kaniko/.netrc/.netrc ~/.netrc || echo "machine ${SERVER_HOST} login dummy password ${GITLAB_TOKEN}" > ~/.netrc)

WORKDIR /app

RUN apk add --no-cache    \
    curl=8.12.1-r0    \
    git=2.43.6-r0  && \
    curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR="/usr/local/bin" sh

COPY pyproject.toml uv.lock ./

# download dependencies with .lock for better performance
RUN uv sync

COPY *.py process/

# final image
FROM python:3.13-alpine3.19

LABEL maintainer="Intelygenz - Konstellation Team"

ARG USER=kai
ARG UID=10001
ARG GID=10001
ENV HOME=/home/${USER}
ENV PYTHONUNBUFFERED=1

# security updates, dependencies and user setup
# hadolint ignore=DL3018
RUN addgroup -g ${GID} ${USER}      && \
    adduser -D -g "" -h "${HOME}"      \
    -s "/sbin/nologin" -u ${UID}     \
    -G ${USER} ${USER}            && \
    # setup app directories with proper permissions
    mkdir -p /app /var/log/app      && \
    chown -R ${UID}:${GID} /app /var/log/app

WORKDIR /app

# copy binaries and config files
COPY --from=builder --chown=${UID}:${GID} /app/process ./process
COPY --from=builder --chown=${UID}:${GID} /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages

# switch to non-root user
USER ${USER}

CMD ["python", "/app/process/main.py"]
