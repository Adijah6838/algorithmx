FROM python:3.11-slim

WORKDIR /app

# Install system dependencies needed for psycopg2 and compiling code
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    g++ \
    default-jdk \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend code
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
