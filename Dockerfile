# Grab the Nginx base image using Alpine Linux
FROM nginx:stable-alpine

# Install application dependencies and build tools
RUN apk add --no-cache \
    python3 \
    python3-dev \
    py3-pip \
    mariadb-dev \
    gcc \
    musl-dev

# Move into the backend application directory
WORKDIR /app

# Create a python virtual environment
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Copy and install the requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask/Gunicorn application files
COPY app.py .
COPY gunicorn.conf.py .

# Replaces the local nginx configuration with the image filesystem
COPY nginx.conf /etc/nginx/nginx.conf

# Copy static website files to Nginx web root
COPY *.html /usr/share/nginx/html/
COPY css /usr/share/nginx/html/css
COPY js /usr/share/nginx/html/js
COPY json/templates /usr/share/nginx/html/templates
COPY favicon.ico /usr/share/nginx/html/

# Copy startup script and make it executable
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Start Gunicorn and Nginx
CMD ["/start.sh"]
