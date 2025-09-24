# Use a slim Python base image
FROM python:3.10-slim

# Install system dependencies: Tesseract OCR + Poppler
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    poppler-utils \
 && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first (for caching layers)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Expose the port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
