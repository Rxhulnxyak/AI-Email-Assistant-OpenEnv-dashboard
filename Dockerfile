FROM python:3.10-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all code
COPY . .

# Set PYTHONPATH to root so 'from server.models' works
ENV PYTHONPATH=/app

# Expose port 8000 (Mandatory for Scaler Portal)
EXPOSE 8000

# CMD to start the server using uvicorn on port 8000
CMD ["uvicorn", "server.server:app", "--host", "0.0.0.0", "--port", "8000"]
