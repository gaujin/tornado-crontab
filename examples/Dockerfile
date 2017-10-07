FROM python:2-alpine
LABEL maintainer "tornado-crontab@gaujin.jp"

RUN set -x && \
    adduser -S spam-ham && \
    easy_install -U tornado-crontab supervisor

COPY ["decorator_style_task_app.py", "supervisord.conf", "/home/spam-ham/"]

CMD ["/usr/local/bin/supervisord", "-c", "/home/spam-ham/supervisord.conf"]
