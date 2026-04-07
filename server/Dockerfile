FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose port 7860 for HF Spaces
EXPOSE 7860

# CMD to run the FastAPI app
CMD ["python", "app.py"]
