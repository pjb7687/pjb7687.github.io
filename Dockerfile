FROM node:22-bookworm-slim

# Everything the builder needs lives under /usr/local or /opt so it stays readable
# once the container drops to the unprivileged `node` user (uid/gid 1000).
ENV DEBIAN_FRONTEND=noninteractive \
    PNPM_HOME="/usr/local/share/pnpm" \
    COREPACK_HOME="/usr/local/share/corepack" \
    TZ="Asia/Seoul"

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        git \
        cron \
        tzdata \
        openssh-client \
        python3 \
        python3-venv \
    && rm -rf /var/lib/apt/lists/* && \
    ln -snf "/usr/share/zoneinfo/${TZ}" /etc/localtime && echo "${TZ}" > /etc/timezone

# uv (Astral) — manages Python deps for the citation script.
RUN curl -LsSf https://astral.sh/uv/install.sh | UV_INSTALL_DIR=/usr/local/bin sh

# Pre-install the scholarly fork into a venv so it's cached in the image layer.
RUN uv venv /opt/scholarly-venv && \
    uv pip install --python /opt/scholarly-venv/bin/python "scholarly @ git+https://github.com/pjb7687/scholarly.git@sortbydate" && \
    chmod -R a+rX /opt/scholarly-venv
ENV PATH="/opt/scholarly-venv/bin:${PNPM_HOME}:${PATH}"

# pnpm via corepack. Both homes are owned by `node`: pnpm lazily fetches a native
# addon into COREPACK_HOME on first run, so read-only is not enough.
RUN mkdir -p "${PNPM_HOME}" "${COREPACK_HOME}" && \
    corepack enable && corepack prepare pnpm@latest --activate && \
    chown -R node:node "${PNPM_HOME}" "${COREPACK_HOME}"

WORKDIR /app
COPY . .
# node_modules must exist and be node-owned in the image: the named volume that
# compose mounts there inherits this ownership when it is first created.
RUN chmod +x build.sh entrypoint.sh && \
    mkdir -p /app/node_modules && \
    chown -R node:node /app

# Run as uid/gid 1000 — same as the host user — so the bind-mounted repo does not
# collect root-owned files in .git/, build/ and .svelte-kit/ on every build.
USER node

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["build"]
