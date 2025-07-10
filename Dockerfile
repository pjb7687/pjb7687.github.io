FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
        python3 \
        python3-pip \
        git \
        npm \
        nodejs && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip and install Python dependencies
RUN python3 -m pip install --upgrade pip && \
    pip3 install sphinx && \
    pip3 install git+https://github.com/pjb7687/scholarly.git@sortbydate

# Install Node.js dependencies
WORKDIR /app
COPY package.json package-lock.json /app/
RUN npm install

#RUN git clone https://github.com/pjb7687/pjb7687.github.io /app
COPY . /app

# Run main script
CMD ["bash", ".ci/run.sh"]