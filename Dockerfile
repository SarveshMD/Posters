# Start with a base Linux system that has Python 3.10 installed
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

RUN apt-get update && apt-get install -y ca-certificates && update-ca-certificates
# Copy your requirements file first (for caching speed)
COPY requirements.txt .

# Install dependencies inside the container
RUN pip install --upgrade pip && \
    pip install --default-timeout=100 --no-cache-dir -r requirements.txt

# Copy the rest of your code
COPY . .

# Tell Docker this container listens on port 1989
EXPOSE 1989

# The command to run when the container starts
CMD ["python3", "app.py"]