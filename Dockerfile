# Use the official Python image
FROM python:3.11

# Set the working directory
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Start the training script
CMD ["python", "jpp.py"]