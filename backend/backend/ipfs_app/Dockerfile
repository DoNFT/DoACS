FROM python:3.8

ENV POETRY_VERSION=1.1.11
ENV ENVIRONMENT=DEV
# Installing packages
RUN DEBIAN_FRONTEND=noninteractive apt-get update -y && apt-get install -y ffmpeg

RUN pip install "poetry==$POETRY_VERSION"

# Defining working directory and adding source code
WORKDIR /backend
COPY  ./ipfs_app/poetry.lock ./ipfs_app/pyproject.toml  /backend/

# Install API dependencies
RUN poetry config virtualenvs.create false
RUN poetry install -vvv

COPY . /backend

# Start app
CMD ["python", "main.py"]