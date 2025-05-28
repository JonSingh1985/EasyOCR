# Use a minimal base image
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Install only necessary system packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Copy requirement file
COPY requirements.txt .

# Install Python dependencies without pip cache
RUN pip install --no-cache-dir -r requirements.txt

# Copy the server code
COPY server.py .

# Expose the FastAPI port
EXPOSE 8000

# Run the FastAPI app
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]

