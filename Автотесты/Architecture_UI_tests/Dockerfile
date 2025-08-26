FROM python:3.12-slim-bookworm

RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    libpq-dev \
    build-essential \
    && apt-get clean
RUN pip install poetry
WORKDIR 
COPY pyproject.toml poetry.lock ./
RUN poetry install

COPY . .
RUN poetry run python src/config/replace_visibility_check.py

CMD ["poetry", "run", "python", "-m", "run_tests"]
