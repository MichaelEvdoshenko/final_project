FROM python:3.11

ENV PYTHONPATH=/app/src:$PYTHONPATH
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["pytest", "tests/core/", "tests/ai/", "-v"]