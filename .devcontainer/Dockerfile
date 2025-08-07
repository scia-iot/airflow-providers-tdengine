FROM apache/airflow:slim-3.0.2-python3.12

# Install TDengine client
USER root
ARG TDENGINE_CLIENT_VERSION=3.3.6.6-Linux-arm64
WORKDIR /opt/tdengine
RUN curl -s https://www.taosdata.com/assets-download/3.0/TDengine-client-${TDENGINE_CLIENT_VERSION}.tar.gz --output tdengine-client.tar.gz
RUN tar -xf tdengine-client.tar.gz --directory . --strip-components=1 && rm tdengine-client.tar.gz
RUN ./install_client.sh

# Install dependencies of TDengine provider
USER airflow
ADD requirements.txt ./tdengine-provider-requirements.txt
RUN pip install -r tdengine-provider-requirements.txt
RUN pip install build

# Init & start airflow
RUN airflow db migrate
ENTRYPOINT ["airflow standalone"]
