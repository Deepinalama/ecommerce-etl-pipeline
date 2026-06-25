from python:3.10-slim

workdir /app

#Install system dependencies required 
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements list and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project folders (data, scripts, etc.) into the container
COPY . .

EXPOSE 8501

# Start the Streamlit dashboard pointing to the scripts folder
CMD ["streamlit", "run", "scripts/dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]

