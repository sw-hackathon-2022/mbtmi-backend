FROM python:3.9

ARG API
ARG STATIC
ARG SRC

# Set working directory
RUN mkdir -p $API
RUN mkdir -p $SRC
WORKDIR ${API}

# Copy Requirements
COPY ./api/requirements.txt ./requirements.txt

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy project
COPY ./api .

# Copy environment variables
COPY .env .

ENV PYTHONPATH=${API}

# Expose port for running the application
EXPOSE 8000
