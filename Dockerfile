FROM python:3.9.10-buster

COPY . /app
RUN echo 'Installing requirements...'
RUN pip install -r /app/setup/requirements.txt

ENTRYPOINT /app/setup/startup.sh

EXPOSE 4000
