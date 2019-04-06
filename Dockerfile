FROM python:3

ENV PYTHONUNBUFFERED 1
RUN mkdir /webadmin
WORKDIR /webadmin
COPY . /webadmin/
RUN pip install -r requirements.txt


