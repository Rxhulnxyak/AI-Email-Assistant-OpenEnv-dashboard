FROM python:3.10-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all code (includes server/ directory)
COPY . .

# Set PYTHONPATH to root so 'from server.models' works
ENV PYTHONPATH=/app

# Expose port 7860
EXPOSE 7860

# CMD to start the server using uvicorn (industry standard for stability)
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
