# Use the official Python runtime image
FROM python:3.13

# Create the app directory
RUN mkdir /app
WORKDIR /app

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install required tools + Microsoft SQL ODBC driver
RUN apt-get update && apt-get install -y curl gnupg2 apt-transport-https unixodbc && \
    mkdir -p /etc/apt/keyrings && \
    curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /etc/apt/keyrings/microsoft.gpg && \
    echo "deb [signed-by=/etc/apt/keyrings/microsoft.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql18 unixodbc-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

EXPOSE 8000

HEALTHCHECK --interval=5m --timeout=3s CMD curl -f http://localhost:8000/ || exit 1

CMD ["sh", "docker-entrypoint.sh"]
