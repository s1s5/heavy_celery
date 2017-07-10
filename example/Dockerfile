FROM ubuntu:16.04
ENV PYTHONUNBUFFERED 1
ENV LANG ja_JP.UTF-8
RUN apt-get update && \
    apt-get install -y python3 libpq-dev libffi-dev libssl-dev && \
    apt-get install -y git python3-pip locales language-pack-ja && \
    apt-get install -y cron && \
    dpkg-reconfigure -f noninteractive locales && \
    update-locale LANG=${LANG} && \
    apt-get upgrade -y && \
    apt-get clean && \
    rm -rf /var/cache/apt/archives/* /var/lib/apt/lists/*
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 10
RUN pip3 install --upgrade pip
RUN pip3 install setuptools virtualenvwrapper

ENV STATIC_ROOT /data/static
ENV MEDIA_ROOT /data/media
ENV LOG_ROOT /data/log

RUN mkdir /app

COPY example/requirements.txt /app/package/tmp/
COPY example/manage.py /app/manage.py
COPY requirements_test.txt /app/package/
COPY setup.cfg /app/package/
COPY setup.py /app/package/
COPY README.rst /app/package/
COPY HISTORY.rst /app/package/
COPY heavy_celery /app/package/heavy_celery

WORKDIR /app/package/tmp/
RUN pip3 install -U -r requirements.txt

WORKDIR /
RUN useradd app
RUN mkdir -p /data/media
RUN mkdir -p /data/static
RUN mkdir -p /data/log
RUN mkdir -p /data/tmp
RUN chown -R app:app /app
RUN chown -R app:app /data/media
RUN chown -R app:app /data/static
RUN chown -R app:app /data/log
RUN chown -R app:app /data/tmp

COPY example/example /app/example

VOLUME /data/static
VOLUME /data/media
VOLUME /data/log
VOLUME /data/tmp

USER app
WORKDIR /app
CMD bash -c "sleep 5; python manage.py migrate; python manage.py runserver 0.0.0.0:8000"
EXPOSE 8000
