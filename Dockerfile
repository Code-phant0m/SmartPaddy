FROM python:3.10-slim

# Set up working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy source code
COPY . .

# Expose the port for Cloud Run
EXPOSE 8080

# Set the default command
CMD ["python", "run.py"]
