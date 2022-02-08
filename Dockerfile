FROM python:3.9.10-buster

COPY . /app
RUN /bin/bash -c "echo 'Installing requirements...'"
RUN /bin/bash -c "pip install -r /app/setup/requirements.txt"

ENTRYPOINT /bin/bash -c "python /app/main.py"

EXPOSE 4000
