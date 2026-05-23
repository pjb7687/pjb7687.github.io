FROM node:22-bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive \
    PATH="/root/.local/bin:${PATH}" \
    PNPM_HOME="/root/.local/share/pnpm" \
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
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Pre-install the scholarly fork into a venv so it's cached in the image layer.
RUN uv venv /opt/scholarly-venv && \
    uv pip install --python /opt/scholarly-venv/bin/python "scholarly @ git+https://github.com/pjb7687/scholarly.git@sortbydate"
ENV PATH="/opt/scholarly-venv/bin:${PATH}"

# pnpm via corepack
RUN corepack enable && corepack prepare pnpm@latest --activate
ENV PATH="${PNPM_HOME}:${PATH}"

WORKDIR /app
COPY . .
RUN chmod +x build.sh entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["build"]
