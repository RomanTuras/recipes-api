FROM python:3.11-slim

RUN pip install poetry \
    && poetry self add poetry-plugin-export

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN poetry export -f requirements.txt --without-hashes --output requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 80

ENTRYPOINT ["python", "entry.py"]