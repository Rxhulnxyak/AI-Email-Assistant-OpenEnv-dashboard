FROM python:3.10-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all code (Now all in the root)
COPY . .

# Set PYTHONPATH to root /app
ENV PYTHONPATH=/app

# Expose port 8000 (Mandatory for Scaler Portal)
EXPOSE 8000

# CMD to start the server from the root directory
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
