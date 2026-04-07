FROM python:3.10-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all code
COPY . .

# Set PYTHONPATH
ENV PYTHONPATH=/app

# Expose port 8000
EXPOSE 8000

# CMD to start the server from the root directory
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
