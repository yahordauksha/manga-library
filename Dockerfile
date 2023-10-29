FROM python:3.11

WORKDIR /manga_project

# Copy the Pipfile and Pipfile.lock into the container
COPY Pipfile Pipfile.lock /manga_project/

# Install dependencies using pip from the Pipfile.lock
RUN pip install -U pipenv
#RUN pipenv sync
RUN pipenv install --system


COPY . /manga_project/

ENV PYTHONUNBUFFERED 1

EXPOSE 8000

# Create a start script to run both Django and Celery
RUN echo '#!/bin/sh' > start.sh
RUN echo 'pipenv run python manage.py runserver 0.0.0.0:8000 &' >> start.sh
RUN echo 'pipenv run celery -A manga_project worker --loglevel=info' >> start.sh
RUN chmod +x start.sh

# Define the command to start the script
CMD ["./start.sh"]
