FROM python:3.6

ADD requirements.txt /var/tmp/
RUN pip install -r /var/tmp/requirements.txt
ADD entrypoint.sh /var/tmp/entrypoint.sh

WORKDIR /opt/src/

ENTRYPOINT ["/var/tmp/entrypoint.sh"]
