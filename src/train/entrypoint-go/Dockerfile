# golang:1.22.0-alpine3.19
FROM golang@sha256:8e96e6cff6a388c2f70f5f662b64120941fcd7d4b89d62fec87520323a316bd9 AS builder

ARG GITLAB_TOKEN
ARG SERVER_HOST

# environment variables
ENV CGO_ENABLED=0  \
    GOOS=linux     \
    GOARCH=amd64   \
    GOPRIVATE=true \
    GO111MODULE=on

RUN apk add --no-cache git=2.43.6-r0 && \
    echo "machine ${SERVER_HOST} login dummy password ${GITLAB_TOKEN}" > ~/.netrc

WORKDIR /app

# copy source code
COPY . .

# download dependencies with cache mount for better performance
RUN --mount=type=cache,target=/go/pkg/mod    \
    go mod download                       && \
    go mod verify

# -ldflags="-s -w -extldflags '-static'": Optimizes binary size by removing debug info
# and ensures all C dependencies are included in the binary for better portability
# -trimpath: Removes build system paths to improve security and reproducibility
RUN go build \
    -ldflags="-s -w -extldflags '-static'" \
    -trimpath \
    -o process

# final image
# alpine:3.19.0
FROM alpine@sha256:51b67269f354137895d43f3b3d810bfacd3945438e94dc5ac55fdac340352f48

LABEL maintainer="Intelygenz - Konstellation Team"

ARG USER=kai
ARG UID=10001
ARG GID=10001
ENV HOME=/home/${USER}

# security updates, dependencies and user setup
# hadolint ignore=DL3018
RUN apk update                     && \
    apk upgrade                    && \
    apk add --no-cache                \
      ca-certificates=20241121-r1     \
      libcap=2.69-r1               && \
    rm -rf /var/cache/apk/*        && \
    # create non-root user
    addgroup -g ${GID} ${USER}     && \
    adduser -D -g "" -h "${HOME}"     \
      -s "/sbin/nologin" -u ${UID}    \
      -G ${USER} ${USER}           && \
    # setup app directories with proper permissions
    mkdir -p /app /var/log/app     && \
    chown -R ${UID}:${GID} /app /var/log/app

WORKDIR /app

# copy binaries and config files
COPY --from=builder --chown=${UID}:${GID} /app/process .
COPY --chown=${UID}:${GID} app.yaml .

# switch to non-root user
USER ${USER}

CMD ["/app/process"]
