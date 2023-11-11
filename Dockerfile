FROM python:latest
WORKDIR /app
COPY requirements.txt /app

RUN pip install -r requirements.txt
COPY . /app
# Set environment variables
ENV DJANGO_SETTINGS_MODULE=card_backend.settings


# Define the command to run the application
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "card_backend.asgi:application"]

# Expose port 8000 to the outside world
EXPOSE 8000