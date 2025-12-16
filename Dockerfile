# Use an official lightweight Python image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose ports for API (8000) and Streamlit (8501)
EXPOSE 8000
EXPOSE 8501

# Default command (overridden by docker-compose)
CMD ["bash"]