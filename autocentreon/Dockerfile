FROM python:3.9-alpine
WORKDIR /src
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY /src /src
CMD ["python", "main.py", "-p", "-c"]