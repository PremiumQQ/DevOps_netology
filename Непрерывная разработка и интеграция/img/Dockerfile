FROM centos:7

ENV PYTHON_VER=3.8.7 \
    PYTHON_MINOR=3.8 \
    PORT=5290

RUN yum -y install wget make gcc openssl-devel bzip2-devel libffi-devel && \
    cd /tmp/ && \
    wget https://www.python.org/ftp/python/3.8.7/Python-3.8.7.tgz && \
    tar xzf Python-3.8.7.tgz && \
    cd Python-3.8.7 && \
    ./configure --enable-optimizations && \
    make altinstall && \
    ln -sfn /usr/local/bin/python3.8 /usr/bin/python3.8 && \
    ln -sfn /usr/local/bin/pip3.8 /usr/bin/pip3.8 && \
    python3.8 -m pip install --upgrade pip
RUN pip3.8 install flask flask-restful flask-jsonpify

COPY python-api.py /python_api/python-api.py
CMD ["python3.8", "/python_api/python-api.py"]

