FROM python:3.10-slim

ENV PYTHONUNBUFFERED True
ENV APP_HOME /app
# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN apt-get update && apt-get install -y libpq-dev

RUN apt-get update && apt-get install -y build-essential
# Upgrade pip to the latest version
RUN pip install --no-cache-dir --upgrade pip

# Clean up the build environment
RUN rm -rf build/ dist/ *.egg-info/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements_local.txt

# Expose port 5000 for the Flask app
EXPOSE 8000

#CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "--threads", "16", "--timeout", "120", "wsgi:app"]

CMD exec gunicorn --bind :8000 --workers 3 --threads 6 --timeout 0 wsgi:app