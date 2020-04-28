FROM centos:7

ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV PIPENV_PIPFILE /data/web/rewards/api/Pipfile
ENV PIPENV_VENV_IN_PROJECT true

WORKDIR /data/web/rewards

RUN yum -y update && \
    yum -y install gcc httpd-devel python36-devel && \
    yum clean all

RUN ln -sf /proc/self/fd/1 /var/log/httpd/access_log && \
    ln -sd /proc/self/fd/1 /var/log/httpd/error_log

RUN python3.6 -m pip install mod_wsgi pipenv && \
    mod_wsgi-express install-module > /etc/httpd/conf.modules.d/02-wsgi.conf

#RUN python3.6 -m venv /data/web/rewards/venv && \
#    /data/web/rewards/venv/bin/python -m pip install django mysql-connector-python

COPY httpd/rewards.conf /etc/httpd/conf.d/

COPY httpd/rewards.wsgi /usr/local/www/wsgi-scripts/

COPY api /data/web/rewards/api

COPY ui/dist /data/web/rewards/ui/dist

RUN pipenv install --python python3.6

RUN ln -s /data/web/rewards/api/.venv /data/web/rewards/venv

EXPOSE 80

CMD ["/usr/sbin/httpd", "-D", "FOREGROUND"]
