FROM ubuntu:24.04
LABEL authors="brian"
USER root

# Set environment variables to non-interactive (no prompts during installation)
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies required for Miniconda
RUN apt-get update && apt-get install -y \
    wget \
    bzip2 \
    curl \
    ca-certificates \
    git \
    rsync \ 
    && rm -rf /var/lib/apt/lists/*

# Download and install Miniconda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh \
    && bash /tmp/miniconda.sh -b -p /opt/miniconda \
    && rm /tmp/miniconda.sh

# Add Miniconda to PATH
ENV PATH="/opt/miniconda/bin:$PATH"

# Update conda and install any dependencies you want (optional)
RUN conda update -y conda

# Set work directory
RUN mkdir /app
WORKDIR /app

# Copy project
COPY . /app/

# Install dependencies
RUN pip install --upgrade pip
RUN pip install .

# Create user
#RUN useradd -ms /bin/bash brian
#RUN usermod -aG sudo brian
#USER brian
