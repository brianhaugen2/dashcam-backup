FROM python:3.11
LABEL authors="brian"
USER root

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
RUN mkdir /app
WORKDIR /app

# Create user
RUN useradd -ms /bin/bash brian
USER brian

# Install dependencies
RUN pip install --upgrade pip
RUN pip install .

# Copy project
COPY . /app/
