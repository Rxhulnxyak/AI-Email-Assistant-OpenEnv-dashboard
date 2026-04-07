FROM python:3.10-slim

WORKDIR /app

# Copy requirements from root and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project (including 'server/' package)
COPY . .

# Set PYTHONPATH to the root /app so 'import server.models' works
ENV PYTHONPATH=/app

# Expose port 7860 for HF Spaces
EXPOSE 7860

# CMD to run the FastAPI app located in the server subdirectory
CMD ["python", "server/app.py"]
