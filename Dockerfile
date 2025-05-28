# Use slim base to reduce image size
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install required system packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    tesseract-ocr \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY server.py .

# Expose port
EXPOSE 8000

# Start server
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
