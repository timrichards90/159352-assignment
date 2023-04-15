FROM python:latest
WORKDIR /src
COPY . .

RUN pip install requests
RUN rm -r venv/

CMD python server.py 8080