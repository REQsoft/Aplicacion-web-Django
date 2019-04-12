FROM python:3

ENV PYTHONUNBUFFERED 1
RUN mkdir /webadmin
WORKDIR /webadmin
COPY . /webadmin/
RUN pip freeze
RUN cat requirements.txt
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y libsasl2-dev python-dev libldap2-dev libssl-dev python-django-auth-ldap python-ldap && pip install python-ldap==3.2.0
RUN apt-get update && apt-get install -y libsasl2-dev python-dev libldap2-dev libssl-dev python-django-auth-ldap python-ldap && pip install django-auth-ldap==1.7.0
RUN pip freeze